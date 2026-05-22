#!/usr/bin/env python3
"""Create an HTML rebuild preview from a bigscreen asset manifest."""

from __future__ import annotations

import argparse
import html
import json
import os
from pathlib import Path
from typing import Any


def rel_for_html(path: Path, out_dir: Path) -> str:
    return Path(os.path.relpath(path.resolve(), out_dir.resolve())).as_posix()


def percent(value: float) -> str:
    return f"{value:.6f}%"


def asset_img(asset: dict[str, Any], manifest_dir: Path, out_dir: Path, base_w: int, base_h: int) -> str:
    asset_path = manifest_dir / asset["file"]
    src = html.escape(rel_for_html(asset_path, out_dir))
    left = percent(asset["x"] / base_w * 100)
    top = percent(asset["y"] / base_h * 100)
    width = percent(asset["width"] / base_w * 100)
    height = percent(asset["height"] / base_h * 100)
    z = int(asset.get("zIndex", 0))
    opacity = asset.get("opacity", 1)
    name = html.escape(str(asset.get("name", "")))
    return (
        f'<img class="asset" src="{src}" alt="" data-name="{name}" '
        f'style="left:{left};top:{top};width:{width};height:{height};'
        f'z-index:{z};opacity:{opacity};" />'
    )


def build_html(manifest: dict[str, Any], manifest_path: Path, source: Path | None, out_path: Path, title: str) -> str:
    manifest_dir = manifest_path.parent.resolve()
    out_dir = out_path.parent.resolve()
    base_w = int(manifest["baseWidth"])
    base_h = int(manifest["baseHeight"])
    stage = "\n".join(
        asset_img(asset, manifest_dir, out_dir, base_w, base_h)
        for asset in manifest.get("assets", [])
    )
    source_panel = ""
    if source and source.exists():
        src = html.escape(rel_for_html(source, out_dir))
        source_panel = f"""
        <section class="panel">
          <header>Source</header>
          <img class="source-image" src="{src}" alt="" />
        </section>
        """
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: #10141f;
      color: #d8e1ef;
      font-family: Arial, sans-serif;
    }}
    main {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 16px;
      padding: 16px;
    }}
    .panel {{
      min-width: 0;
    }}
    header {{
      height: 28px;
      color: #96a3b6;
      font-size: 13px;
      line-height: 28px;
    }}
    .source-image,
    .stage {{
      display: block;
      width: 100%;
      aspect-ratio: {base_w} / {base_h};
      background: #020712;
      box-shadow: 0 0 0 1px rgba(255,255,255,.08);
    }}
    .source-image {{
      height: auto;
      object-fit: contain;
    }}
    .stage {{
      position: relative;
      overflow: hidden;
    }}
    .asset {{
      position: absolute;
      object-fit: fill;
      pointer-events: none;
    }}
  </style>
</head>
<body>
  <main>
    {source_panel}
    <section class="panel">
      <header>Rebuild</header>
      <div class="stage">
        {stage}
      </div>
    </section>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Path to generated manifest.json")
    parser.add_argument("--source", help="Optional original source image")
    parser.add_argument("--out", help="Preview HTML path. Defaults to manifest directory/preview.html")
    parser.add_argument("--title", default="Bigscreen Asset Preview")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    out_path = Path(args.out).resolve() if args.out else manifest_path.with_name("preview.html")
    source_raw = args.source or manifest.get("source")
    source = Path(source_raw).resolve() if source_raw else None
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        build_html(manifest, manifest_path, source, out_path, args.title),
        encoding="utf-8",
    )
    print(f"Preview: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
