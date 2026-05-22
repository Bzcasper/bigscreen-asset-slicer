#!/usr/bin/env python3
"""Compare two images and print simple visual-difference metrics."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageStat
except ImportError as exc:  # pragma: no cover - depends on local environment
    raise SystemExit(
        "Pillow is required. Install it with: python -m pip install pillow"
    ) from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expected", help="Expected/source image")
    parser.add_argument("actual", help="Actual/rebuilt screenshot image")
    parser.add_argument("--resize-second", action="store_true", help="Resize actual image to expected dimensions")
    parser.add_argument("--diff", help="Optional diff image output path")
    parser.add_argument("--threshold", type=float, default=None, help="Fail when normalized MAE is above threshold")
    args = parser.parse_args()

    expected_path = Path(args.expected).resolve()
    actual_path = Path(args.actual).resolve()
    expected = Image.open(expected_path).convert("RGB")
    actual = Image.open(actual_path).convert("RGB")

    if expected.size != actual.size:
        if not args.resize_second:
            raise SystemExit(
                f"Size mismatch: expected {expected.size}, actual {actual.size}. "
                "Use --resize-second to compare scaled screenshots."
            )
        actual = actual.resize(expected.size, Image.Resampling.LANCZOS)

    diff = ImageChops.difference(expected, actual)
    stat = ImageStat.Stat(diff)
    channel_means = stat.mean
    mae = sum(channel_means) / len(channel_means)
    normalized_mae = mae / 255
    rms = math.sqrt(sum(value * value for value in stat.rms) / len(stat.rms)) / 255
    max_diff = max(channel[1] for channel in diff.getextrema()) / 255

    print(f"size: {expected.width}x{expected.height}")
    print(f"mae: {mae:.4f}")
    print(f"normalized_mae: {normalized_mae:.6f}")
    print(f"rms: {rms:.6f}")
    print(f"max_diff: {max_diff:.6f}")

    if args.diff:
        diff_path = Path(args.diff).resolve()
        diff_path.parent.mkdir(parents=True, exist_ok=True)
        diff.save(diff_path)
        print(f"diff: {diff_path}")

    if args.threshold is not None and normalized_mae > args.threshold:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
