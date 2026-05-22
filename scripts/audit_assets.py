#!/usr/bin/env python3
"""Create an asset audit report for generated bigscreen assets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image, ImageChops, ImageDraw, ImageStat
except ImportError as exc:  # pragma: no cover - depends on local environment
    raise SystemExit(
        "Pillow is required. Install it with: python -m pip install pillow"
    ) from exc


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def load_rgb(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")


def normalized_mae(expected: Image.Image, actual: Image.Image) -> float:
    diff = ImageChops.difference(expected, actual)
    stat = ImageStat.Stat(diff)
    return (sum(stat.mean) / len(stat.mean)) / 255


def make_side_by_side(reference: Image.Image, candidate: Image.Image, out_path: Path) -> None:
    height = min(720, max(reference.height, candidate.height))
    ref = reference.resize((round(reference.width * height / reference.height), height), Image.Resampling.LANCZOS)
    cand = candidate.resize((round(candidate.width * height / candidate.height), height), Image.Resampling.LANCZOS)
    gutter = 28
    label_h = 38
    canvas = Image.new("RGB", (ref.width + cand.width + gutter, height + label_h), (8, 14, 28))
    draw = ImageDraw.Draw(canvas)
    canvas.paste(ref, (0, label_h))
    canvas.paste(cand, (ref.width + gutter, label_h))
    draw.text((10, 10), "Reference", fill=(220, 240, 255))
    draw.text((ref.width + gutter + 10, 10), "Candidate", fill=(220, 240, 255))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path)


def make_diff(reference: Image.Image, candidate: Image.Image, out_path: Path) -> float:
    cand = candidate
    if reference.size != candidate.size:
      cand = candidate.resize(reference.size, Image.Resampling.LANCZOS)
    diff = ImageChops.difference(reference, cand)
    score = normalized_mae(reference, cand)
    enhanced = diff.point(lambda value: min(255, value * 4))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    enhanced.save(out_path)
    return score


def iter_asset_files(assets_dir: Path) -> Iterable[Path]:
    for path in sorted(assets_dir.rglob("*")):
        relative_parts = set(path.relative_to(assets_dir).parts[:-1])
        if relative_parts & {"audit", "source"}:
            continue
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            if path.name.startswith("preview-screenshot"):
                continue
            yield path


def make_contact_sheet(assets_dir: Path, out_path: Path) -> int:
    files = list(iter_asset_files(assets_dir))
    if not files:
        return 0
    tile_w = 220
    tile_h = 170
    label_h = 34
    cols = min(4, max(1, len(files)))
    rows = (len(files) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * tile_w, rows * (tile_h + label_h)), (8, 14, 28))
    draw = ImageDraw.Draw(canvas)
    for index, path in enumerate(files):
        col = index % cols
        row = index // cols
        x = col * tile_w
        y = row * (tile_h + label_h)
        thumb = Image.open(path).convert("RGBA")
        thumb.thumbnail((tile_w - 20, tile_h - 20), Image.Resampling.LANCZOS)
        bg = Image.new("RGBA", (tile_w, tile_h), (10, 28, 58, 255))
        bg.alpha_composite(thumb, ((tile_w - thumb.width) // 2, (tile_h - thumb.height) // 2))
        canvas.paste(bg.convert("RGB"), (x, y))
        label = path.relative_to(assets_dir).as_posix()
        draw.text((x + 8, y + tile_h + 8), label[:32], fill=(210, 232, 255))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path)
    return len(files)


def manifest_summary(path: Path | None) -> str:
    if not path or not path.exists():
        return "Manifest: not provided"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    assets = manifest.get("assets", [])
    categories = sorted({str(item.get("category", "misc")) for item in assets})
    safe_assets = sum(
        1
        for item in assets
        if item.get("safeZone") or item.get("safeZones") or item.get("contentInsets")
    )
    return (
        f"Manifest: {len(assets)} assets, canvas "
        f"{manifest.get('baseWidth')}x{manifest.get('baseHeight')}, "
        f"categories: {', '.join(categories)}, "
        f"assets with safe zones: {safe_assets}"
    )


def write_report(
    out_path: Path,
    reference: Path | None,
    candidate: Path | None,
    assets_dir: Path | None,
    manifest: Path | None,
    mae: float | None,
    asset_count: int,
) -> None:
    lines = [
        "# Bigscreen Asset Audit",
        "",
        "## Inputs",
        "",
        f"- Reference: {reference if reference else 'not provided'}",
        f"- Candidate: {candidate if candidate else 'not provided'}",
        f"- Assets directory: {assets_dir if assets_dir else 'not provided'}",
        f"- {manifest_summary(manifest)}",
        "",
        "## Metrics",
        "",
        f"- Normalized MAE: {mae:.6f}" if mae is not None else "- Normalized MAE: not computed",
        f"- Contact sheet assets: {asset_count}",
        "",
        "## Manual Review Checklist",
        "",
        "- [ ] Overall composition matches the reference at a glance.",
        "- [ ] Target canvas and asset dimensions follow the production plan, not accidental reference-image dimensions.",
        "- [ ] Generated assets match the reference style lock instead of a generic dashboard theme.",
        "- [ ] Header beam, title treatment, clock/weather, and brand block match the reference density.",
        "- [ ] Panel borders, corner cuts, title bands, and glow treatment match the reference.",
        "- [ ] Central scene matches the reference's machinery style, perspective, lighting, and detail level.",
        "- [ ] KPI strip icons, separators, and number spacing match the reference.",
        "- [ ] Left column donuts, legends, progress bars, and equipment summary match the reference.",
        "- [ ] Right column table, quality block, and energy block match the reference.",
        "- [ ] Bottom value bar icon treatment, separators, and vertical alignment match the reference.",
        "- [ ] Panel interiors, title bands, KPI areas, nav slots, table/list areas, and scene overlays reserve clean DOM content space.",
        "- [ ] Decorative assets do not contain live text, data values, charts, or table content.",
        "- [ ] All image assets load and remain reusable in the frontend.",
        "",
        "## Gate",
        "",
        "Reject the assets when the reference composition cannot be recognized from the candidate screenshot at a glance, when the candidate looks like a free redesign, when the target canvas/safe zones are wrong, or when the central scene uses a different visual style.",
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", help="Reference image path")
    parser.add_argument("--candidate", help="Candidate screenshot path")
    parser.add_argument("--assets-dir", help="Directory containing sliced/generated assets")
    parser.add_argument("--manifest", help="Optional manifest.json path")
    parser.add_argument("--out", required=True, help="Audit output directory")
    args = parser.parse_args()

    out_dir = Path(args.out).resolve()
    reference_path = Path(args.reference).resolve() if args.reference else None
    candidate_path = Path(args.candidate).resolve() if args.candidate else None
    assets_dir = Path(args.assets_dir).resolve() if args.assets_dir else None
    manifest_path = Path(args.manifest).resolve() if args.manifest else None

    mae: float | None = None
    if reference_path and candidate_path:
        reference = load_rgb(reference_path)
        candidate = load_rgb(candidate_path)
        make_side_by_side(reference, candidate, out_dir / "side-by-side.png")
        mae = make_diff(reference, candidate, out_dir / "diff.png")

    asset_count = 0
    if assets_dir and assets_dir.exists():
        asset_count = make_contact_sheet(assets_dir, out_dir / "asset-contact-sheet.png")

    report_path = out_dir / "asset-audit.md"
    write_report(
        report_path,
        reference_path,
        candidate_path,
        assets_dir,
        manifest_path,
        mae,
        asset_count,
    )
    print(f"Audit report: {report_path}")
    if mae is not None:
        print(f"normalized_mae: {mae:.6f}")
    print(f"asset_count: {asset_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
