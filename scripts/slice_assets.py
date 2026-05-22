#!/usr/bin/env python3
"""Slice generated dashboard artwork into frontend-ready assets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageChops
except ImportError as exc:  # pragma: no cover - depends on local environment
    raise SystemExit(
        "Pillow is required. Install it with: python -m pip install pillow"
    ) from exc


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip()).strip("-")
    return slug.lower() or "asset"


def resolve_path(raw: str | None, base: Path, fallback: Path | None = None) -> Path:
    if raw:
        path = Path(raw)
        return path if path.is_absolute() else (base / path).resolve()
    if fallback is None:
        raise ValueError("Missing path")
    return fallback.resolve()


def parse_box(box: Any) -> tuple[int, int, int, int]:
    if isinstance(box, list) and len(box) == 4:
        x, y, w, h = box
        return int(x), int(y), int(w), int(h)
    if isinstance(box, dict):
        if {"x", "y", "w", "h"} <= set(box):
            return int(box["x"]), int(box["y"]), int(box["w"]), int(box["h"])
        if {"left", "top", "right", "bottom"} <= set(box):
            left = int(box["left"])
            top = int(box["top"])
            right = int(box["right"])
            bottom = int(box["bottom"])
            return left, top, right - left, bottom - top
        if {"l", "t", "r", "b"} <= set(box):
            left = int(box["l"])
            top = int(box["t"])
            right = int(box["r"])
            bottom = int(box["b"])
            return left, top, right - left, bottom - top
    raise ValueError(f"Unsupported box format: {box!r}")


def clamp_box(x: int, y: int, w: int, h: int, image: Image.Image) -> tuple[int, int, int, int]:
    left = max(0, x)
    top = max(0, y)
    right = min(image.width, x + w)
    bottom = min(image.height, y + h)
    if right <= left or bottom <= top:
        raise ValueError(f"Crop outside image bounds: {(x, y, w, h)}")
    return left, top, right, bottom


def expand_box(
    bbox: tuple[int, int, int, int],
    padding: int,
    width: int,
    height: int,
) -> tuple[int, int, int, int]:
    left, top, right, bottom = bbox
    return (
        max(0, left - padding),
        max(0, top - padding),
        min(width, right + padding),
        min(height, bottom + padding),
    )


def trim_alpha(image: Image.Image) -> tuple[Image.Image, tuple[int, int, int, int]]:
    if "A" not in image.getbands():
        return image, (0, 0, image.width, image.height)
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        return image, (0, 0, image.width, image.height)
    return image.crop(bbox), bbox


def trim_solid(
    image: Image.Image,
    tolerance: int,
) -> tuple[Image.Image, tuple[int, int, int, int]]:
    working = image.convert("RGBA")
    bg = Image.new("RGBA", working.size, working.getpixel((0, 0)))
    diff = ImageChops.difference(working, bg)
    if tolerance > 0:
        diff = diff.convert("L").point(lambda value: 0 if value <= tolerance else 255)
    bbox = diff.getbbox()
    if bbox is None:
        return image, (0, 0, image.width, image.height)
    return image.crop(bbox), bbox


def save_image(image: Image.Image, path: Path, fmt: str, quality: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = fmt.lower()
    if normalized in {"jpg", "jpeg", "webp"} and image.mode in {"RGBA", "LA"}:
        background = Image.new("RGB", image.size, (0, 0, 0))
        background.paste(image, mask=image.getchannel("A"))
        image = background
    if normalized in {"jpg", "jpeg"}:
        image.save(path, "JPEG", quality=quality, optimize=True)
    elif normalized == "webp":
        image.save(path, "WEBP", quality=quality, method=6)
    else:
        image.save(path, "PNG", optimize=True)


def posix_relative(path: Path, base: Path) -> str:
    return path.relative_to(base).as_posix()


def css_hints(x: int, y: int, w: int, h: int, base_w: int, base_h: int) -> dict[str, str]:
    return {
        "position": "absolute",
        "left": f"{x}px",
        "top": f"{y}px",
        "width": f"{w}px",
        "height": f"{h}px",
        "leftPercent": f"{x / base_w * 100:.6f}%",
        "topPercent": f"{y / base_h * 100:.6f}%",
        "widthPercent": f"{w / base_w * 100:.6f}%",
        "heightPercent": f"{h / base_h * 100:.6f}%",
    }


def copy_optional_fields(source: dict[str, Any], target: dict[str, Any], fields: tuple[str, ...]) -> None:
    for field in fields:
        if field in source:
            target[field] = source[field]


def build_manifest(spec: dict[str, Any], spec_path: Path, manifest_override: str | None) -> dict[str, Any]:
    spec_dir = spec_path.parent.resolve()
    source_path = resolve_path(spec.get("source"), spec_dir)
    if not source_path.exists():
        raise FileNotFoundError(f"Source image not found: {source_path}")

    output_dir = resolve_path(
        spec.get("outputDir"),
        spec_dir,
        source_path.with_name(f"{source_path.stem}-assets"),
    )
    manifest_path = resolve_path(
        manifest_override or spec.get("manifest"),
        spec_dir,
        output_dir / "manifest.json",
    )

    source = Image.open(source_path)
    base_w = int(spec.get("baseWidth") or source.width)
    base_h = int(spec.get("baseHeight") or source.height)

    manifest_assets: list[dict[str, Any]] = []
    for index, asset in enumerate(spec.get("assets", [])):
        name = str(asset.get("name") or f"asset-{index + 1}")
        safe_name = slugify(name)
        category = str(asset.get("category") or "misc")
        role = str(asset.get("role") or category)
        fmt = str(asset.get("format") or "png").lower()
        ext = "jpg" if fmt == "jpeg" else fmt
        quality = int(asset.get("quality") or spec.get("quality") or 92)
        x, y, w, h = parse_box(asset.get("box"))
        left, top, right, bottom = clamp_box(x, y, w, h, source)
        crop = source.crop((left, top, right, bottom))

        trim_info = {"left": 0, "top": 0, "right": crop.width, "bottom": crop.height}
        final_x = left
        final_y = top
        if asset.get("trim"):
            trim_mode = str(asset.get("trimMode") or "alpha").lower()
            if trim_mode == "solid":
                crop, bbox = trim_solid(crop, int(asset.get("trimTolerance") or 8))
            else:
                crop, bbox = trim_alpha(crop)
            if asset.get("padding"):
                padded = expand_box(
                    bbox,
                    int(asset.get("padding") or 0),
                    right - left,
                    bottom - top,
                )
                crop = source.crop((left + padded[0], top + padded[1], left + padded[2], top + padded[3]))
                bbox = padded
            trim_info = {"left": bbox[0], "top": bbox[1], "right": bbox[2], "bottom": bbox[3]}
            final_x = left + bbox[0]
            final_y = top + bbox[1]

        file_value = asset.get("file")
        if file_value:
            output_path = output_dir / str(file_value)
        else:
            output_path = output_dir / slugify(category) / f"{safe_name}.{ext}"
        save_image(crop, output_path, fmt, quality)

        width = crop.width
        height = crop.height
        entry = {
            "name": name,
            "category": category,
            "role": role,
            "file": posix_relative(output_path.resolve(), output_dir.resolve()),
            "x": final_x,
            "y": final_y,
            "width": width,
            "height": height,
            "zIndex": int(asset.get("zIndex", index)),
            "opacity": asset.get("opacity", 1),
            "repeat": asset.get("repeat", "no-repeat"),
            "originalBox": {"x": x, "y": y, "width": w, "height": h},
            "trim": trim_info,
            "css": css_hints(final_x, final_y, width, height, base_w, base_h),
        }
        copy_optional_fields(
            asset,
            entry,
            (
                "contentInsets",
                "safeZone",
                "safeZones",
                "targetSize",
                "styleNotes",
                "usageNotes",
            ),
        )
        manifest_assets.append(entry)

    manifest = {
        "version": 1,
        "source": str(source_path),
        "baseWidth": base_w,
        "baseHeight": base_h,
        "outputDir": str(output_dir),
        "assets": sorted(manifest_assets, key=lambda item: item["zIndex"]),
    }
    copy_optional_fields(
        spec,
        manifest,
        (
            "targetCanvas",
            "referenceImage",
            "styleNotes",
            "contentPlan",
            "safeZones",
        ),
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(manifest_assets)} assets")
    print(f"Manifest: {manifest_path}")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, help="Path to slice spec JSON")
    parser.add_argument("--manifest", help="Optional manifest output path")
    args = parser.parse_args()

    spec_path = Path(args.spec).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8-sig"))
    build_manifest(spec, spec_path, args.manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
