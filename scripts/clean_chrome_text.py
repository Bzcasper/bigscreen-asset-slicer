#!/usr/bin/env python3
"""Remove bright text/data from a dashboard chrome crop with local inpainting.

This is for precision chrome where the source crop already has the correct
geometry and style, such as title beams, nav bases, and panel frame examples.
It intentionally avoids text-to-image redraws that can drift away from the
reference style.
"""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    import cv2
    import numpy as np
except ImportError as exc:  # pragma: no cover - depends on local environment
    raise SystemExit(
        "OpenCV and numpy are required. Install them with: python -m pip install opencv-python numpy"
    ) from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Input crop path")
    parser.add_argument("--out", required=True, help="Output cleaned image path")
    parser.add_argument("--sat-max", type=int, default=90, help="Maximum HSV saturation for white/gray text")
    parser.add_argument("--value-min", type=int, default=150, help="Minimum HSV value for bright text")
    parser.add_argument("--dilate", type=int, default=3, help="Mask dilation size in pixels")
    parser.add_argument("--radius", type=float, default=3.0, help="Inpaint radius")
    parser.add_argument(
        "--mask-out",
        help="Optional debug mask output path",
    )
    args = parser.parse_args()

    source = Path(args.source).resolve()
    out = Path(args.out).resolve()
    image = cv2.imread(str(source), cv2.IMREAD_COLOR)
    if image is None:
        raise SystemExit(f"Could not read source image: {source}")

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]

    # The dashboard text is mostly bright white/gray with low saturation.
    # Cyan rails have much higher saturation, so they are preserved.
    mask = ((saturation <= args.sat_max) & (value >= args.value_min)).astype("uint8") * 255

    if args.dilate > 0:
        kernel_size = max(1, args.dilate)
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)

    cleaned = cv2.inpaint(image, mask, args.radius, cv2.INPAINT_TELEA)
    out.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out), cleaned)

    if args.mask_out:
        mask_path = Path(args.mask_out).resolve()
        mask_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(mask_path), mask)

    print(f"Wrote {out}")
    if args.mask_out:
        print(f"Mask: {Path(args.mask_out).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
