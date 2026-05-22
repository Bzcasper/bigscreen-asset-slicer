#!/usr/bin/env python3
"""Create side-by-side region comparison sheets for high-fidelity dashboard QA."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


def parse_box(value: Iterable[int]) -> tuple[int, int, int, int]:
    box = tuple(int(v) for v in value)
    if len(box) != 4:
        raise ValueError(f"box must have four integers, got {value!r}")
    return box  # type: ignore[return-value]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", required=True, help="Reference screenshot path")
    parser.add_argument("--candidate", required=True, help="Candidate screenshot path")
    parser.add_argument("--spec", required=True, help="JSON spec with region pairs")
    parser.add_argument("--out", required=True, help="Output comparison PNG")
    parser.add_argument("--column-width", type=int, default=760)
    args = parser.parse_args()

    reference = Image.open(args.reference).convert("RGB")
    candidate = Image.open(args.candidate).convert("RGB")
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    regions = spec.get("regions", [])
    if not regions:
        raise SystemExit("spec must contain regions[]")

    font = ImageFont.load_default()
    label_h = 24
    gap = 18
    col_w = args.column_width
    rows: list[Image.Image] = []

    for region in regions:
        name = region["name"]
        max_h = int(region.get("height", 220))
        ref_crop = reference.crop(parse_box(region["referenceBox"]))
        cand_crop = candidate.crop(parse_box(region["candidateBox"]))
        ref_crop.thumbnail((col_w, max_h), Image.Resampling.LANCZOS)
        cand_crop.thumbnail((col_w, max_h), Image.Resampling.LANCZOS)

        row_h = label_h + max(ref_crop.height, cand_crop.height) + gap
        row = Image.new("RGB", (col_w * 2 + gap, row_h), (6, 12, 24))
        draw = ImageDraw.Draw(row)
        draw.text((0, 4), f"REF  {name}", fill=(210, 238, 250), font=font)
        draw.text((col_w + gap, 4), f"CURRENT  {name}", fill=(210, 238, 250), font=font)
        row.paste(ref_crop, (0, label_h))
        row.paste(cand_crop, (col_w + gap, label_h))
        rows.append(row)

    sheet_h = sum(row.height for row in rows) + gap * (len(rows) - 1)
    sheet = Image.new("RGB", (col_w * 2 + gap, sheet_h), (3, 8, 18))
    y = 0
    for row in rows:
        sheet.paste(row, (0, y))
        y += row.height + gap

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()
