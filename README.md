# Bigscreen Asset Slicer Skill

Codex skill for rebuilding big-screen dashboards/cockpits from screenshots into frontend-ready assets and route/page implementations.

The skill is designed for high-fidelity dashboard reconstruction:

- split a supplied screenshot into strict reference crops;
- decide which parts should be CSS/DOM/ECharts and which parts need raster assets;
- generate or image-edit clean UI assets without baked text/data;
- maintain an asset coverage matrix for high-impact chrome, icons, frames, glows, and state overlays;
- validate generated assets and rendered pages with local visual audits.

## Install

Copy this folder into a Codex skills directory, for example:

```text
<CODEX_HOME>/skills/bigscreen-asset-slicer/
```

or keep it in a project-local skills directory if your Codex setup loads project skills.

The required skill entrypoint is:

```text
SKILL.md
```

## Contents

```text
bigscreen-asset-slicer-skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── asset-review.md
│   ├── frontend-integration.md
│   ├── high-fidelity-rebuild.md
│   ├── imagegen-prompts.md
│   └── slice-spec.md
└── scripts/
    ├── audit_assets.py
    ├── clean_chrome_text.py
    ├── compare_images.py
    ├── compare_region_pairs.py
    ├── crop_reference_regions.py
    ├── make_preview.py
    └── slice_assets.py
```

## Typical Workflow

1. Provide a dashboard screenshot/reference image.
2. Crop layout regions with `scripts/crop_reference_regions.py`.
3. Build an asset coverage matrix before frontend implementation.
4. Use `view_image` to load local crops before image generation when doing crop-guided redraws.
5. Generate clean raster assets for high-impact chrome/icons/frames instead of shipping screenshot crops.
6. Integrate generated assets into the host app's normal asset/page directories.
7. Capture the real route and run visual audits before calling the rebuild complete.

## Notes

- The skill is framework-aware but not tied to a specific repository. Paths use placeholders such as `<app>/src/assets/bigscreen/<page-name>/`.
- Generated outputs such as `generated/`, `reference-crops/`, and `asset-audit/` are intentionally ignored by Git.
- Do not commit user screenshots, generated customer assets, API keys, or local machine paths.
