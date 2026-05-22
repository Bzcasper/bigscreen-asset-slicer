# High-Fidelity Bigscreen Rebuild

Use this reference when the user asks for high restoration, 85%+ fidelity, pixel-near reconstruction, or says the current rebuild "does not look right".

## Goal

High fidelity means the candidate is recognizable as the same dashboard before reading any data:

- Same major region proportions, spacing rhythm, and visual hierarchy.
- Same chrome ownership: no duplicated header/footer/panel rails.
- Same component family for header, KPI strip, side panels, central scene controls, right metric blocks, and bottom navigation.
- Same icon semantic families. Do not swap KPI, nav, quality, energy, brand, weather, and status icons just because they share a cyan badge style.
- Chart interiors may differ when they will be rendered by ECharts, but their containers, title bands, controls, and safe zones must match.

## Mandatory Workflow

1. Lock target canvas.
   - Default to `1920x1080` for production, even when the source screenshot is non-standard.
   - Map the reference composition proportionally; do not redesign the page to fill extra space.

2. Build a region inventory before implementation.
   - Header and brand/weather slots.
   - KPI strip and per-KPI icon/rate slots.
   - Left column panels.
   - Central scene, tabs, 3D button, callout cards, and bottom status strip.
   - Bottom chart-row containers only; chart lines/bars are ECharts-owned.
   - Right safety card, equipment table, quality metrics, energy metrics.
   - Bottom navigation base, active halo, per-slot icon/text anchors.

3. Build an asset coverage matrix.
   - For every non-chart visual component, mark `generated-accepted`, `generated-draft`, `css-faithful`, `css-approximation`, `missing`, or `blocked-needs-image-edit-input`.
   - `css-approximation` and `missing` are not acceptable for high-fidelity icons, logos, header ornaments, bottom nav bases, active halos, irregular frames, or metric badges.
   - If a high-impact component is `missing`, stop and generate/review that asset before claiming high fidelity.

4. Use crop-guided image editing for precision assets.
   - A prompt naming a crop file is not enough; the actual crop image must be provided to the image-edit tool.
   - For built-in `image_gen`, local crop files can be used by opening them with `view_image` first so they are visible in the conversation, then asking the image tool to redraw the visible crop/reference.
   - If the crop cannot be made visible to the image tool, or the task needs explicit masks/direct file-path editing that the current tool path does not expose, mark the asset `blocked-needs-image-edit-input`. Do not pretend it is crop-guided.
   - Text-to-image is not acceptable for header beams, nav bases, KPI icons, right metric icons, brand marks, active halos, or exact frame chrome.

5. Implement only after the asset coverage matrix has no high-impact gaps.
   - The Vue page may use CSS for straight lines, fills, simple masks, layout, text, tables, and ECharts containers.
   - Do not use CSS-only approximations for complex icon badges, logo marks, active halos, title ornaments, or nav bases unless the reference component is truly regular and CSS-identical.

6. Review by local regions first, then the whole page.
   - Generate a side-by-side region sheet with `scripts/compare_region_pairs.py`.
   - Review local region failures even if the full screenshot feels close.
   - Do not claim `85%` if two or more high-impact regions still read as a different component family.

## 85% Acceptance Gate

All must be true:

- `asset-review.md` has no hard-fail conditions.
- Region comparison shows the same layout identity for header, KPI strip, central scene, right column, left column, and bottom navigation.
- No high-impact component is `css-approximation` or `missing` in the coverage matrix.
- Source crops were used as actual image-edit inputs for every generated precision asset.
- The candidate works at `1920x1080` and at least one scaled viewport without offset/cropping.

Do not use phrases like "basically 85%" or "close enough" when these gates fail. Call it `high-fidelity draft` and list the remaining asset gaps.

## Common Failure Modes

- KPI strip rebuilt as isolated cards when the reference uses a continuous band.
- Safety card duplicated inside the KPI strip instead of remaining a right-side module.
- Right column content order changed from safety/table/quality/energy to generic plan/quality/energy/rank blocks.
- Bottom navigation laid out as equal flex columns when the reference uses measured segmented slots.
- Header band delivered as an obvious opaque rectangle or shortened wings.
- Brand cube, weather icon, KPI icons, quality icons, and energy icons replaced by generic CSS or reused nav icons.
- Precision icons generated from the correct crop but enlarged into glossy standalone emblems instead of retaining the source crop's tiny UI footprint.
- Central scene missing the tab rail, 3D button, status strip, or callout anchor rhythm.
- Chart interiors over-optimized while non-chart chrome remains wrong.

## Required Review Files

For a high-fidelity task, leave these artifacts next to the source image:

- `asset-coverage-matrix.json`
- `asset-audit/page-region-compare-<canvas>.png`
- Updated `asset-audit/asset-audit.md` with the 85% gate result.
- A list of missing or blocked image-edit assets if the gate fails.
