#!/usr/bin/env python3
"""Crop a dashboard reference image into reviewable layout regions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageDraw
except ImportError as exc:  # pragma: no cover - depends on local environment
    raise SystemExit(
        "Pillow is required. Install it with: python -m pip install pillow"
    ) from exc


def parse_box(region: dict[str, Any]) -> tuple[int, int, int, int]:
    box = region.get("box")
    if isinstance(box, list) and len(box) == 4:
        x, y, w, h = box
        return int(x), int(y), int(w), int(h)
    if isinstance(box, dict):
        if {"x", "y", "w", "h"} <= box.keys():
            return int(box["x"]), int(box["y"]), int(box["w"]), int(box["h"])
        if {"left", "top", "right", "bottom"} <= box.keys():
            left = int(box["left"])
            top = int(box["top"])
            return left, top, int(box["right"]) - left, int(box["bottom"]) - top
    raise ValueError(f"Invalid box for region {region.get('name')!r}")


def safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in value).strip("-")


def make_contact_sheet(crops: list[tuple[dict[str, Any], Path]], out_path: Path) -> None:
    if not crops:
        return
    tile_w = 300
    tile_h = 190
    label_h = 38
    cols = min(4, len(crops))
    rows = (len(crops) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * tile_w, rows * (tile_h + label_h)), (8, 14, 28))
    draw = ImageDraw.Draw(canvas)
    for index, (region, path) in enumerate(crops):
        col = index % cols
        row = index // cols
        x = col * tile_w
        y = row * (tile_h + label_h)
        image = Image.open(path).convert("RGB")
        image.thumbnail((tile_w - 16, tile_h - 16), Image.Resampling.LANCZOS)
        canvas.paste(image, (x + (tile_w - image.width) // 2, y + 8))
        label = f"{region.get('name', path.stem)} | {region.get('role', '')}"
        draw.text((x + 8, y + tile_h + 8), label[:42], fill=(218, 238, 255))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path)


def write_notes(
    source: Path,
    out_dir: Path,
    crops: list[tuple[dict[str, Any], Path]],
) -> None:
    lines = [
        "# Reference Layout Crops",
        "",
        f"- Source: {source}",
        f"- Output: {out_dir}",
        "",
        "| Crop | Role | Review Scope | Preserve | Remove |",
        "| --- | --- | --- | --- | --- |",
    ]
    for region, path in crops:
        preserve = ", ".join(region.get("preserve", []))
        remove = ", ".join(region.get("remove", []))
        review_scope = region.get("reviewScope", "")
        lines.append(
            f"| `{path.name}` | {region.get('role', '')} | {review_scope} | {preserve} | {remove} |"
        )
    (out_dir / "layout-crops.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Reference image path")
    parser.add_argument("--spec", required=True, help="JSON spec with regions[] or referenceCrops[]")
    parser.add_argument("--out", required=True, help="Output directory for cropped regions")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    spec_path = Path(args.spec).resolve()
    out_dir = Path(args.out).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    regions = spec.get("regions") or spec.get("referenceCrops") or []
    if not regions:
        raise SystemExit("Spec must contain a non-empty regions[] or referenceCrops[] array")

    image = Image.open(source).convert("RGBA")
    out_dir.mkdir(parents=True, exist_ok=True)
    crops: list[tuple[dict[str, Any], Path]] = []
    for region in regions:
        x, y, w, h = parse_box(region)
        crop = image.crop((x, y, x + w, y + h))
        name = safe_name(str(region.get("name") or region.get("role") or f"crop-{len(crops)+1}"))
        path = out_dir / f"{name}.png"
        crop.save(path)
        crops.append((region, path))

    make_contact_sheet(crops, out_dir / "layout-contact-sheet.png")
    write_notes(source, out_dir, crops)
    print(f"wrote {len(crops)} crops to {out_dir}")
    print(f"contact_sheet: {out_dir / 'layout-contact-sheet.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
