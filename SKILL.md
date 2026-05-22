---
name: bigscreen-asset-slicer
description: Convert a supplied big-screen dashboard/cockpit screenshot into frontend-ready, reference-guided UI assets, slice manifests, and Vue rebuilds. Use when a page needs AI-generated or image-edited raster materials such as backgrounds, panel frames, title decorations, borders, icons, state badges, glows, or texture layers that should closely match a reference while keeping text/data live in frontend.
---

# Bigscreen Asset Slicer

## Purpose

Use this skill to turn reference images or generated big-screen visual artwork into a reusable frontend asset package. The goal is not to bake a whole page into one image; keep live data, text, charts, tables, and interactions in Vue/CSS, and use generated or image-edited assets only for static visual surfaces that are hard to reproduce with CSS.

When the user provides a finished dashboard screenshot, default to screenshot-guided reconstruction: preserve the reference layout, geometry, rhythm, colors, and UI component shapes as closely as possible, but regenerate or edit the material so text, numbers, chart data, labels, and table content are removed or reserved for DOM. Cropping the source image is a guidance step for image generation/editing, not a shortcut to use text-bearing screenshot crops as final frontend assets.

When the screenshot is non-standard size, still decide the production canvas before implementation, usually `1920x1080`, but map the reference composition proportionally instead of redesigning it. The non-standard image can guide layout coordinates and asset geometry; the final assets should be regenerated or normalized for the production canvas.

When the user asks for high restoration, 85%+ fidelity, or says the current rebuild is obviously wrong, switch to high-fidelity mode before generating or implementing anything. Read `references/high-fidelity-rebuild.md`, create an asset coverage matrix, and treat missing high-impact assets as blockers instead of filling them with generic CSS or reused icons.

## Workflow

### Asset-Only Mode

Use this mode when the user asks to split a reference image into components, generate reusable UI assets, or validate the asset pipeline without building the full Vue page.

Asset-only mode stops before frontend implementation. The deliverable is an asset package next to the source image or in the user-specified directory:

- `*-asset-regions.json`: source-image component decomposition and crop boxes.
- `reference-crops/`: focused source crops and a contact sheet for strict visual locking.
- `asset-generation-plan.md`: the required generated UI assets, each tied to the closest crop, with prompts and rejection rules.
- `generated/`: accepted image-generated or image-edited UI assets. Text/data/chart-bearing source crops are not accepted as final assets.
- `manifest.json` or `asset-manifest.json`: coordinates, safe zones, semantic slots, title/action slots, and state anchors needed by Vue/CSS later.
- `asset-coverage-matrix.json`: high-impact component coverage, source strategy, status, crop-input proof, and blockers.
- `asset-audit/`: contact sheets, side-by-side checks, and notes explaining which assets still need regeneration.

Asset-only mode rules:

- Do not create a page, route, preview route, or Vue component unless the user explicitly asks for the rebuild.
- Keep the reference image's native canvas when the request is about proving component splitting for that exact image. Normalize to `1920x1080` only when the user asks for production assets.
- Always split the full screenshot into layout crops before generating assets. Use the nearest crop, not the whole dashboard, as the primary visual lock for each prompt.
- Write a `style-lock.md` before any generation. It must summarize palette, lighting, texture density, frame geometry, border thickness, corner cuts, icon badge language, and the CSS-vs-raster rule for repeated frames. Every prompt must quote or reference this style lock plus the nearest crop.
- Write a per-asset `fidelity brief` before generation. It must state what the crop actually looks like: prominence, line weight, glow strength, opacity, UI slot size, and which details are weaker/subtler than image-model defaults. Every prompt must include this brief so the model does not "improve" the asset into a different style.
- Write a `chrome-ownership` plan before any generation. Decide whether page background, header, bottom navigation, panel borders, and state overlays are owned by the background, separate PNG assets, or CSS. Do not generate two assets that own the same visible rail, border, glow, or nav base.
- Background assets must declare whether they include or exclude top/header and bottom/footer chrome. If top or bottom chrome will be separate assets, the background prompt must explicitly exclude title beams, top rails, bottom navigation bars, panel frames, and footer glow.
- Header assets must declare whether they are a transparent title-beam overlay, an opaque full-width header band, or small side ornaments. Do not deliver an opaque rectangular crop as `title-beam` unless the manifest says that asset owns the full covered header band. A transparent title-beam overlay must have clean alpha outside the beam/rails and documented `titleAnchor`, `subtitleAnchor`, and optional logo/weather/status slots.
- For high-fidelity reconstruction, choose an opaque header band when the reference title beam is visually fused with the dark header background and cannot be separated cleanly without changing style. Transparent overlays are only appropriate when the ornament has a clear separable silhouette. If a transparent-overlay attempt turns into an armored/bottom-nav-like plate, reject it and switch to an opaque no-text header band.
- Header title/brand text should be DOM unless the user explicitly asks to bake it. Removing glyphs must preserve the title safe zone, subtitle safe zone, center alignment, and any beam/rail structure behind the text.
- Component crops for frames must include the full outer border, top title/header band, action/control slot area when present, and a small amount of surrounding glow. Do not crop only the content interior when the output asset is a container. If the crop or generated asset loses the border, title reservation, action-slot reservation, or corner glow, reject it and regenerate or adjust the crop.
- Bottom navigation crops must be treated as a measured footer slot system. Preserve the full-width low-profile footer base, item-slot rhythm, separator positions, top/bottom hairlines, and weak glow from the crop. Remove icon glyphs, labels, subtitles, and active/click glow from the neutral base; generate active/click effects as separate overlays. Reject a neutral base that turns into a heavy standalone bar, a centered chevron plate, or a new segmented shape that does not match the crop's slot geometry.
- Bottom navigation active overlays must preserve the crop's actual layered light structure, such as outer ring, inner glow, lower bright arc, and tiny broken highlights. If the selected halo looks flat after import, regenerate or reprocess the overlay asset; CSS should only position, size, and mildly tune opacity, not invent extra rings, badges, or glow geometry.
- Write a CSS-vs-image decision for every component. Generate raster only for hard-to-reproduce material: title beams, irregular panel corners/notches, glow nodes, icon badges, active halos, central scene material, and complex semantic icons.
- Decide `crop-guided-redraw`, `masked-image-edit`, or `text-to-image` for every raster asset. Use `crop-guided-redraw` by default for screenshot components. Use `masked-image-edit` when dirty text/data must be removed while preserving the crop's geometry. Use `text-to-image` only for ambient backgrounds, missing assets, icon families, or scenes where exact geometry drift is acceptable.
- Source crops are reference inputs only in generated-asset workflows. Do not deliver locally cleaned or directly cropped source pixels as final UI assets unless the user explicitly authorizes source-derived fallback assets.
- Do not use text-to-image generation for precision chrome such as title beams, bottom navigation bases, and reusable frame parts. Pure prompt generation is likely to change line weight, geometry, and border grammar even when the palette is similar.
- For screenshot reconstruction, `image-edit` means the actual cropped component image must be provided as an image input/reference for redraw. Naming a crop in the prompt is not enough. With the built-in `image_gen` path, a local crop can be used as image input by first opening it with `view_image` so it is visible in the conversation, then prompting `image_gen` to redraw the visible crop/reference. Only mark `blocked-needs-image-edit-input` when the crop cannot be made visible to the image tool, or when the task requires explicit masks/direct file-path editing that the current tool path does not expose.
- When the user says "基于剪裁素材重绘", treat this as crop-guided redraw/edit, not text-to-image style prompting and not local source cleanup. Preserve the crop's measured silhouette, edge positions, line weight, border ownership, and anchor geometry; only remove or regenerate dirty text/data regions.
- Local post-processing may crop, resize, remove chroma-key, split sheets, and audit image-generated outputs. It must not turn the original crop into a final asset unless explicitly allowed.
- For generated assets, keep DOM content out: no baked Chinese or English text, numbers, chart lines, axes, legends, tables, callouts, or sample data.
- Save project-bound generated files into the requested output directory before finishing. Built-in image generation may create temporary files under Codex home; copy accepted assets into the workspace.
- If an asset has a selected/active/running/warning state, generate the neutral base and state overlay separately, and record the state anchor.
- If an asset is only a prompt target and has not been generated yet, mark it as `status: planned`; do not pretend it is a final asset.
- Every generated asset must pass two gates before it can be `accepted` or `draft-usable`:
  - UI asset gate: transparent or intentionally opaque, clean edges, no baked DOM content, meaningful standalone part boundaries, documented anchors/safe zones/title slots/action slots, and directly importable by frontend.
  - Style gate: compare against the nearest reference crop for line weight, glow strength, shape grammar, icon base material, semantic colors, scale, and density. If it reads as a different design system, mark `rejected`, not `draft`.
- If the reference style is subtle, low-contrast, or CSS-like, use subtractive prompt language: "barely visible", "do not improve", "do not make standalone decorative", "no glow nodes", "do not thicken", and "keep weaker than normal UI asset defaults". Do not use generic words like "premium", "high-detail", "cinematic", "futuristic", or "glowing" unless the crop itself is clearly that strong.
- When a generated asset fails style because it is over-amplified, do not keep iterating with vague "closer to reference" prompts. Update the fidelity brief with the exact failure, for example `rim 2x too thick`, `glow too bright`, `badge too large`, or `extra notch added`, then regenerate with those explicit corrections. If the same failure repeats twice, change strategy: smaller crop, single-part redraw, full-frame redraw, or fixed-ratio asset.

### High-Fidelity Mode

Use this mode when the user cares more about restoration than asset reuse, for example `85%`, `高度还原`, `不像原图`, or `不要重新设计`.

- Read `references/high-fidelity-rebuild.md` before planning page or asset work.
- Create `asset-coverage-matrix.json` before implementation. List every non-chart visual component: header band, brand mark, weather/status icons, KPI strip, KPI icons, panel frames, central scene chrome, tabs/buttons/callouts, right metric icons, bottom nav base, active halo, and per-slot nav icons.
- Mark each item as `generated-accepted`, `generated-draft`, `css-faithful`, `css-approximation`, `missing`, or `blocked-needs-image-edit-input`.
- Treat `missing`, `css-approximation`, and `blocked-needs-image-edit-input` as hard blockers for high-impact precision assets: brand/logo, weather icon, KPI icons, right-side metric icons, title/header chrome, bottom navigation base, active halo, irregular frame chrome, and complex badges.
- Do not mark a high-impact crop as blocked merely because it is stored on disk. First load the crop or contact sheet with `view_image`; if it is visible to the model, use it as the reference input for built-in `image_gen` and record the proof as `visible-crop-input` in the asset coverage matrix.
- Do not claim 85% or final acceptance while any high-impact component is blocked or approximated. Call the result `high-fidelity draft` and list the remaining asset gaps.
- Generate a region comparison sheet with `scripts/compare_region_pairs.py` after each serious rebuild screenshot. Review header, KPI strip, center scene, left column, right column, and bottom navigation as separate local regions before judging the full page.

1. Lock the target canvas and reference role.
   - Decide the design canvas before any image generation. Default to `1920x1080` unless the user gives another production size.
   - Do not inherit the reference image dimensions when the reference is only a style sample.
   - Record the target canvas, page regions, and required asset sizes/aspect ratios in the spec or notes.
   - Identify content safe zones before generation: title bands, title text anchors, action/control slots, KPI value blocks, chart interiors, table rows, legend columns, icon slots, bottom-nav label slots, and central-scene callout margins.
   - Treat ECharts or other component-rendered chart interiors as dynamic frontend content unless the user explicitly asks to reproduce chart graphics as image assets. Do not generate chart lines, bars, axes, legends, or data labels as static image assets.
   - For bottom navigation, extract the actual slot boxes and icon/text anchors from the reference crop. Do not assume `repeat(6, 1fr)` or any equal distribution unless the reference slots prove it.
   - For bottom navigation base assets, record whether the PNG owns only the neutral footer base or also decorative slot plates. The active state must have its own overlay anchor and must not be baked into the neutral base.

2. Extract a strict reconstruction lock from the reference.
   - Summarize the reference palette, lighting, panel geometry, corner cuts, border thickness, glow strength, icon language, texture density, and typography scale.
   - Extract a style lock before prompting. Use it as a contract, not a descriptive afterthought: every generated asset must preserve the same panel grammar, icon material, glow strength, and line weight unless the crop proves a component uses a different family.
   - Extract a fidelity brief for every asset before prompting:
     - `prominence`: barely visible / subtle / medium / high.
     - `lineWeight`: hairline / 1px / 2px / thick.
     - `glow`: none / faint / local / strong.
     - `material`: CSS-like line, dark glass fill, icon badge, opaque scene, etc.
     - `scale`: expected frontend slot size.
     - `doNotAmplify`: exact features the model tends to overdo, such as glow, rim thickness, badge size, bevels, title notches, frame armor, and decorative nodes.
   - Extract chrome ownership before prompting. For every visible top rail, title beam, page background line, bottom rail, nav base, panel border, and state glow, choose exactly one owner: background, separate image asset, or CSS. Record duplicated-chrome risks and remove the duplicate from the prompt or manifest.
   - For background-no-chrome assets, run a top/bottom zone ownership check before accepting. If the first header band or last footer band contains recognizable title beams, header rails, nav slot boxes, selected halos, or footer bases that are planned as separate assets, reject or regenerate the background. Generic faint circuit texture is allowed; component-shaped chrome is not.
   - For each container crop, include the complete outer frame. Expand the crop box when needed so the border, clipped corners, corner glows, title/header band, and action/control slot area are all visible. Content-only crops are reference crops for layout, not final frame references.
   - Before prompting or comparing assets, split the reference by content layout into focused crops: header, left panels, KPI strip, central scene, chart panels, right tables/metrics, bottom navigation, and icon/status families. Treat this as a divide-and-conquer step, not optional polish.
   - Crop small reference examples by category when useful: background, title beam, panel frame, icon/base, state icon, bottom nav, central scene.
   - Use `scripts/crop_reference_regions.py` with a `regions[]` JSON spec to produce these layout crops and a contact sheet:

```bash
python .agents/skills/bigscreen-asset-slicer/scripts/crop_reference_regions.py --source reference.png --spec path/to/layout-regions.json --out path/to/reference-crops/layout
```

   - Use these crops and notes as strict visual constraints for image generation or image editing. They are not final frontend assets unless the crop is already text-free and passes the asset review gate.
   - For each crop, write what must be preserved and what must be removed: preserve frame geometry/glow/icon shape/background texture, title/header reservation, action/control slot reservation, and content safe-zone rhythm; remove title text glyphs, values, labels, fake chart marks, table rows, and callout copy. Mark chart regions as component-driven when their lines, bars, axes, legends, or labels will be rendered by ECharts.
   - Reject any generated asset that reads as a different design system, even if it is visually polished.

3. Choose the source strategy.
   - Decide CSS versus image assets by shape complexity. CSS is appropriate for regular fills, straight connector lines, simple gradients, simple clipping, and layout-only spacing. Image-generated assets are required for irregular frame corners, asymmetric notches, beveled caps, glow nodes, bright dots, small highlight sparks, complex icon badges, and any non-rule-based ornament that CSS cannot reproduce faithfully.
   - If using built-in image generation for a local crop, first call `view_image` on the exact crop or a small contact sheet so it becomes a visible image input, then call `image_gen` using language such as `redraw the visible reference image`. This is valid crop-guided generation even though the tool does not accept a filesystem path argument.
   - If using built-in image generation for a local crop, verify the result is a true edit/reference-guided reconstruction. If the output canvas, geometry, or line weight is freely invented, reject it and retry with the crop visible immediately before the image call, a tighter prompt, or a smaller component crop. Do not silently replace the generated asset with a cleaned source crop.
   - For crop-guided redraw, open or attach the cropped reference image immediately before the edit call. The prompt must say `edit/redraw the provided visible crop`, not merely `match crop <name>`. After generation, compare the source crop and candidate crop by silhouette/edge position before accepting style.
   - Do not draw the same frame feature twice. In adaptive frames, CSS should only draw the scalable straight connectors and shaped fill/mask; raster parts should own the corners, notches, caps, nodes, and local highlights.
   - If a CSS-only reconstruction visibly changes the reference style, simplifies important geometry, or loses local highlight details, switch that component to crop-guided image generation or split-frame PNG parts.
   - Best for screenshot reconstruction: crop the matching reference component, then use image generation/editing to create the same UI material without baked text/data and with the correct frontend safe zones, title text anchors, and action/control slots.
   - Better for precision chrome: use the matching source crop as image input for redraw/edit, or generate only a missing/dirty subpart while preserving the source crop's measured geometry. Do not ask a text-to-image model to recreate a thin title rail, nav base, or frame system from prose when the crop already contains the exact ornament.
   - Good: generate one frontend-ready asset per prompt from a specific crop reference, such as background, panel frame, title ornament, icon base, state badge, complex icon, clean factory scene, glow, or divider.
   - Good: generate a same-kind asset sheet only for small decorations such as complex icons, state badges, icon bases, corner marks, and dividers, then slice it.
   - Best for reusable panel frames: split scalable frames into corner/cap/notch/node raster parts, and draw straight horizontal/vertical connectors with CSS. Use full-size frame images only when the panel shape cannot be decomposed or will never resize.
   - For same-type panel frames, create one reusable frame system instead of generating many full-size frame bitmaps. Width and height changes should be handled by CSS connector lengths and clipped fills, not by a separate rendered frame for every panel.
   - For repeated angular frames, prefer one adaptive frame system: PNG owns only non-scalable corners, notches, caps, glow nodes, and short highlights; CSS owns straight top/right/bottom/left connector lines and the clipped fill. Generate a full panel frame only for a unique, complex shape that cannot share the frame system.
   - Do not force adaptive splitting when the reference frame is not actually connector-friendly. If a source frame's style depends on subtle full-border rhythm, continuous glass fill, irregular line density, or details that become wrong after splitting, generate a full same-ratio empty frame instead. Style fidelity beats theoretical reusability.
   - Full-frame redraw is valid when the frame will be used at a fixed or limited set of ratios, or when adaptive reconstruction would require changing the visual language. In that case the full PNG owns the complete border, title/header band, corner glow, and glass fill; CSS owns DOM text, controls, charts, and content placement inside recorded title/action/body safe zones.
   - A usable adaptive frame sheet must contain small connector-ready parts, not large L-shaped frame fragments. Each corner/cap/node must have a tight part box, transparent or keyed empty gutters, and recorded connector anchors where CSS lines enter/exit.
   - Reject frame sheets that include large panel fill chunks, long straight edges, incomplete connector endpoints, inconsistent line thickness, or parts that cannot be described as `corner-tl`, `corner-tr`, `corner-bl`, `corner-br`, `title-cap`, `node`, and `spark`.
   - For generated adaptive frame parts, create a `frame-kit-manifest.json` or manifest entry listing each part box, fixed output size, connector baseline (`topY`, `bottomY`, `leftX`, `rightX`), and CSS ownership. Without these anchors, the sheet is not frontend-ready.
   - Before calling image generation, run a prompt preflight: remove phrases that invite beautification beyond the crop, such as "premium", "high-detail", "cinematic", "futuristic", "strong glow", "polished badge", or "sci-fi", unless the crop itself is clearly that strong. Replace them with measured fidelity constraints from the fidelity brief.
   - Acceptable: slice a final flat dashboard image only as a QA/reference crop, coordinate guide, or temporary fallback.
   - Avoid: slicing text, numbers, chart marks, or data labels into images.
   - Read `references/imagegen-prompts.md` before generating any new raster assets.

4. Review generated assets before slicing.
   - Reject assets that include text, charts, sample data, labels, shadows on chroma-key backgrounds, or a different visual style than the reference.
   - Review each generated material against its nearest layout crop before judging the full page. Whole-screen similarity is not enough because local frame geometry, icon hue, slot alignment, and text safe zones can be wrong while the overall composition still looks close.
   - The asset should already look directly usable by frontend before `slice_assets.py` runs. The slicer should crop/package, not rescue a bad generation.
   - Reject assets that are merely source screenshot crops with text/data still visible when a regenerated clean asset was required.
   - Reject any generated container asset that is missing its outer border, clipped corner, title notch, or local glow when the reference component has one.
   - Reject any asset package where two layers own the same top rail, title beam, bottom rail, nav base, active glow, or panel border. Fix by changing ownership, not by lowering opacity.
   - Reject header/title-beam assets that are RGB/opaque rectangles while the manifest calls them transparent overlays. Either regenerate with alpha outside the ornament, or rename/reclassify the asset as an opaque full-header/header-band layer with exact placement and ownership.
   - Reject transparent header-overlay attempts that invent a heavy armored plate, bottom-navigation-like rail, or solid decorative block instead of preserving the subtle reference header. For such references, prefer an opaque header-band redraw with the text removed.
   - Reject background-no-chrome assets that contain visible top title-beam geometry, bottom navigation geometry, panel borders, or state glows that will also be separate PNG/CSS layers.
   - Reject any adaptive frame sheet whose parts cannot be connected by CSS without overlapping large raster fill areas or guessing connector positions.
   - Reject any frame kit whose generated line weight, glow intensity, or corner grammar reads heavier than the nearest frame crop. A connector-ready sheet can still fail the style gate.
   - If group-level frame-kit generation drifts in style, switch to single-frame-part crop-guided redraw. Crop one source corner/cap/node, use that exact crop as image input, generate one part, then audit it at the intended CSS assembly size before repeating for the rest of the kit.
   - If single-frame-part redraw still changes the style, stop decomposing that frame family and use full-frame crop-guided redraw for the needed ratios. Do not keep forcing a connector kit that changes the design system.
   - Reject any icon sheet whose badge size, rim thickness, glow intensity, color saturation, or pictogram style visibly differs from the nearest icon crop. Icon assets should preserve the reference's small dense dashboard scale; oversized glossy badges are a different style.
   - Never accept directly sliced KPI/metric icon crops as final assets unless the user explicitly asks for source-derived fallback. Screenshot crops usually include card offsets, text remnants, background fragments, and non-centered glow. Use the crop/contact sheet as the visible image reference for generation, then chroma-key/remove background, slice into centered transparent PNGs, and validate alpha bounds plus rendered slot alignment.
   - If group-level icon generation drifts in style, switch to single-icon crop-guided redraw. Crop one source badge, use that exact crop as image input, generate one icon, then audit it at the original UI slot size before repeating for the rest of the family.
   - Reject frame/header/KPI/nav assets that keep dirty edge pixels from the source screenshot, including tiny title remnants, status dots, tab marks, table rows, chart points, callout text, or scene fragments. Full-frame material must be regenerated or cleaned so only reusable chrome remains.
   - Reject assets that were generated at the reference image's odd dimensions when the target canvas is a standard big-screen canvas.
   - Reject panel, title, card, nav, and scene assets that leave no clean space for DOM text, values, charts, tables, legends, or callouts.
   - Reject frame/container assets that remove the title/header reservation while cleaning the title text. Removing glyphs is correct; collapsing the title band, starting the chart/body safe zone at the top edge, or omitting the top-right action/control slot when the reference has one is a failed reconstruction.
   - For cleaned central scenes with DOM callout overlays, verify that every source callout/card is fully removed or covered by a blank material card. Do not leave partial source text behind the new DOM layer.
   - When using blank callout cards as part of a scene asset, record their anchors and sizes, then position Vue text to those same anchors. A blank card that is much larger than the source callout or shifted away from it is a failed reconstruction.
   - Identify state visuals before accepting an asset. Selected, clicked, hover, active, warning, running, paused, disabled, and focus effects must be separate overlay/state assets, not baked into a shared base image.
   - For divided bottom navigation bars, verify that every icon/text group is inside its corresponding visual slot from the reference. Redrawing or detecting separator lines is not enough; placement must use the slot box anchors.
   - Reject neutral bottom navigation bases that are brighter, taller, more angular, or more decorative than the crop, including generated center-heavy hex bars, thick beveled rails, oversized separators, or baked first-item active halos.
   - Build a semantic icon map before accepting icons. Each slot must use the same kind of glyph as the reference, such as brand cube, production monitor, quality shield, equipment gear, energy cycle, report clipboard, weather, leaf, flame, droplet, or status symbol. Do not reuse a nearby-looking KPI icon when the reference uses a different navigation or metric glyph.
   - Validate semantic icon colors after import into the real page. Green leaf/safety/running icons, amber idle icons, red alarm icons, and weather/brand accents must still match the reference hue in the rendered screenshot; regenerate or recolor when chroma-key removal or CSS styling mutes them.
   - Do not use chroma-key removal or slicing for a single opaque asset such as a background or factory scene. Copy the generated WebP/PNG into the workspace and import it directly.
   - Use chroma-key removal only when the asset must have transparency and the image generator did not return clean transparency.
   - If the asset itself contains green semantic color, such as leaf, safety, running, or success indicators, do not use a green chroma key. Use magenta, or remove the green key without despill and validate color preservation against the source.
   - Use slicing only when the source intentionally contains multiple reusable assets or when the user asks to decompose a fixed dashboard mockup.

5. Create a slice spec JSON.
   - Use `baseWidth` and `baseHeight` that match the intended design canvas, usually `1920x1080`.
   - Define each asset with a stable `name`, `category`, `role`, `box`, and `zIndex`.
   - Include `contentInsets`, `safeZone`, `safeZones`, `titleBand`, `titleAnchor`, and `actionSlot` for assets that must hold DOM title text, controls, or body content. Do not use one generic body safe zone when the crop clearly has a separate title/header area.
   - Read `references/slice-spec.md` when writing or adjusting the spec.

6. Run the slicer.

```bash
python .agents/skills/bigscreen-asset-slicer/scripts/slice_assets.py --spec path/to/slice-spec.json
```

7. Generate a preview rebuild.

```bash
python .agents/skills/bigscreen-asset-slicer/scripts/make_preview.py --manifest path/to/output/manifest.json --source path/to/source.png
```

8. Run the asset review gate before frontend implementation.
   - Compare the reference image, rebuilt preview screenshot, and sliced asset contact sheet.
   - Compare locally by layout crop first, then compare the full page. Use the local crops to inspect fine details: KPI card safe zones, panel corner cuts, table density, energy icon hue, and bottom-nav slot placement. For component-driven charts, inspect the panel chrome and content safe zone only, not exact line/bar/axis rendering.
   - In high-fidelity mode, run the asset coverage matrix gate before moving to frontend implementation. No high-impact item may remain `missing`, `css-approximation`, or `blocked-needs-image-edit-input`.
   - Read `references/asset-review.md` before accepting assets.
   - Reject and regenerate assets when the main scene style, panel borders, icon language, title beam, layout scale, safe zones, or color/lighting treatment does not match the reference and target canvas requirements.

```bash
python .agents/skills/bigscreen-asset-slicer/scripts/audit_assets.py --reference reference.png --candidate rebuild.png --assets-dir path/to/output --out path/to/output/audit
```

9. Validate visually.
   - Open the generated `preview.html` only as a QA artifact, not as the final deliverable.
   - If a screenshot of the rebuilt page exists, compare it to the source:

```bash
python .agents/skills/bigscreen-asset-slicer/scripts/compare_images.py source.png rebuild.png --resize-second
```

   - In asset-only mode, stop here after the asset audit and final file list. Do not continue to step 10.

10. Integrate into the frontend.
   - Put generated assets under the host app's static/source asset directory, for example `<app>/src/assets/bigscreen/<page-name>/` or another user-provided asset root.
   - Follow the host app's component naming convention and route organization.
   - Build a route/page component in the host app's normal page directory when the user asks for a usable big-screen page.
   - For direct validation routes, register the page using the host app's established route pattern. Do not deliver a standalone `preview.html` as the final page unless the user explicitly asks for an asset-only preview.
   - Use the existing dev server when it is already running; do not start an extra port just to view a generated preview.
   - Read `references/frontend-integration.md` before implementing the page shell.
   - Capture the final route in the browser after implementation. Check for framework or app chrome that leaks into fullscreen screenshots, such as loading masks, default watermarks, headers, sidebars, or hidden-but-visible loading titles, and explicitly hide them for the big-screen route.
   - Capture the exact route and port the user will open, using the host app's dev URL, not only a standalone preview or a stale screenshot file. Add a cache-busting query when auditing, then also verify the clean URL.
   - Inspect browser computed styles for high-impact imported assets after rendering. A CSS rule may request a larger icon, but global `img { max-width: 100% }`, a narrow grid column, or a smaller wrapper can silently shrink it. Fix the slot/wrapper size or set `max-width: none` on decorative UI assets before judging fidelity.
   - For bottom navigation or other selected states, verify the overlay is anchored to the reference slot, usually the icon center rather than the whole text item. Record or inspect the rendered bounding boxes when the position is subtle.
   - If the bottom navigation base image already contains segmented boxes, position DOM nav items by recorded slot coordinates or per-item styles. Do not use a uniform flex/grid layout just because the item count is regular.

## Script Outputs

`slice_assets.py` writes:

- Cropped image files grouped by category.
- `manifest.json` with asset file paths, canvas coordinates, dimensions, layer order, and CSS hints.

`crop_reference_regions.py` writes:

- One focused reference crop per `regions[]` or `referenceCrops[]` entry.
- `layout-contact-sheet.png` for quick local comparison across regions.
- `layout-crops.md` listing each crop, box, role, preserve notes, and removal notes.

`make_preview.py` writes:

- `preview.html`, an absolute-positioned reconstruction of the image layers for quick browser QA.

`compare_images.py` writes:

- Numeric difference metrics, and optionally a diff image.

`compare_region_pairs.py` writes:

- A side-by-side region comparison sheet from separate reference/candidate crop boxes.
- Use it for high-fidelity rebuild review when the reference screenshot and production canvas have different sizes or aspect ratios.

`audit_assets.py` writes:

- `asset-audit.md` with review checklist, image metrics, and pass/fail guidance.
- `side-by-side.png`, `diff.png`, and `asset-contact-sheet.png` when inputs are provided.

## Practical Rules

- Prefer direct single-file assets over sliced sheets whenever possible.
- Prefer transparent PNG for panel frames, corners, glows, dividers, and overlays.
- Prefer WebP or JPEG for full-screen opaque backgrounds.
- Prefer crop-guided regeneration over loose style prompting. A prompt should name the exact crop category it is matching and say which visual details must be preserved.
- Directly sliced source crops are allowed as reference inputs and audit evidence. In generated-asset workflows, they are not final assets unless the user explicitly authorizes source-derived fallback assets.
- Generate asset-only images without words, business data, chart labels, or sample numbers.
- Frame assets must be edge-clean. If a reference crop contains useful border geometry plus nearby text/data, use it only as an imggen/editing guide; the final frame cannot contain ghost text, partial numbers, scene slivers, colored status dots, tab leftovers, or chart marks along the edge.
- Generate clean main scenes without embedded UI labels unless the user explicitly asks for baked callouts.
- If the reference scene contains callout boxes, either remove them completely and render callout boxes in Vue/CSS, or regenerate blank callout cards at the exact same anchors and render text in Vue over those anchors. Never leave source callout text partially visible behind DOM text.
- Use a chroma key that does not collide with asset colors. Green icons, safety shields, leaves, running lights, or success badges must use magenta keying or a no-despill removal path; otherwise semantic greens will be darkened or removed.
- Treat a supplied reference image as a strict style contract. Do not freely invent a new dashboard theme, panel geometry, color palette, icon system, or glow treatment.
- For high-fidelity rebuilds, do not let page implementation hide asset gaps. If the brand mark, KPI icons, right metric icons, weather icon, title chrome, bottom nav, or active state is only approximated, mark it in the coverage matrix and regenerate the asset rather than styling around it.
- Standardize output to the production canvas and frontend component sizes. A non-standard reference image can guide style, but not asset dimensions, unless the user requests exact slicing.
- Prompt every generated asset with its intended frontend size/aspect ratio and required safe content area.
- Leave usable negative space for DOM text, values, units, charts, legends, tables, and callouts. Empty interiors are a feature, not a flaw.
- Generate complex dashboard icons as real raster assets when the reference uses beveled pictograms, shield emblems, machinery badges, energy symbols, or bottom navigation icons that CSS clip-paths cannot match.
- Generate or edit icons by exact UI meaning, not by broad visual category. Header brand, KPI icons, right-panel metric icons, bottom navigation icons, weather icons, and status icons are separate semantic families even when they share the same glass badge style.
- Keep icon assets text-free. A generated icon may include the pictogram and its glass badge/base, but labels, values, units, percentages, and status words must remain DOM text.
- Keep panel/frame assets empty inside; content, title text, chart marks, and tables must remain DOM. The empty container must still preserve the title/header band and control-slot reservation from the reference crop.
- Prefer adaptive split-frame assets for panel systems that appear in multiple widths/heights. Generate raster parts for non-scalable geometry only: clipped corners, title notches, beveled caps, corner highlights, glow nodes, special joints, and active/state ornaments. Draw straight top/bottom/left/right connector lines in CSS with gradients and shadows so the same frame system can resize without stretching corner artwork.
- For adaptive split frames, define connector anchors before slicing or prompting, such as `top connector y=4px`, `left connector x=2px`, `corner cut=36px`. Crop every corner, notch, spark, and cap from the same connector baseline so CSS changes only the line length, not the surrounding style.
- The panel fill/background layer must be clipped to the same corner geometry as the frame. Do not leave a rectangular background behind diagonal clipped corners; use CSS `clip-path`, a mask, or an equivalent shaped fill layer.
- Corner/cap/notch PNG parts must be alpha-clean in clipped-out areas. Do not include the panel fill, page background, or any rectangular background color inside a corner part; draw fills separately with the same `clip-path`/mask as the frame.
- Do not stretch a single raster frame across unrelated panel ratios. If a frame must support both horizontal and vertical layouts, either generate separate frame ratios or use adaptive split-frame parts plus CSS connectors.
- Split interactive states from base assets. For example, a bottom navigation bar base should not bake in the active click ring; export the active halo/ring as a separate overlay asset and let frontend position it for the active item.
- Position state overlays against the visual element they belong to. For a bottom navigation active halo, center it under the icon unless the reference clearly anchors it to the whole item. Validate in a rendered screenshot, not only in the asset contact sheet.
- For bottom navigation with visible segmented boxes, treat the boxes as layout slots. Extract each slot's left/width and icon/text anchor from the reference crop, then place frontend elements into those slots. Separator lines are only visual evidence; they are not a substitute for slot placement.
- Bottom navigation base generation must be full-width and crop-locked. Preserve the reference footer's weak transparency and slot rhythm; remove icon/text/active-state pixels but keep the subtle visual landing zones for each item. Do not generate a new ornate nav shape just because the crop is cyber-styled.
- Treat obvious selection/click effects as state assets even when the user only provides a screenshot crop. If one menu item, tab, card, or badge is visually brighter than its siblings, extract or regenerate that highlight separately and keep the common base neutral.
- Keep repeated panel styles as reusable slices instead of exporting many nearly identical panels.
- Avoid duplicated chrome. If the background asset already includes header rails, outer frames, or bottom rails from the reference, do not overlay a second generated title beam/frame in the same place.
- For header chrome, decide the layer type before generation: transparent title beam overlay, opaque header band, logo/brand ornament, or DOM-only title text. The asset name, alpha behavior, and manifest ownership must agree.
- Use CSS layout for responsive placement; use image assets for visual treatment.
- Use CSS only where it can faithfully represent the reference. Straight lines and regular geometry can be CSS; irregular luminous frame details, asymmetric cuts, node highlights, and complex badge materials must be generated as image assets.
- In split-frame implementations, avoid duplicate chrome: CSS connectors must stop before image corners/caps, and CSS must not also redraw diagonal corner lines already present in the PNG parts.
- Re-run the preview after every coordinate or crop change.
- Do not continue to frontend page work until the asset audit passes. A structurally similar page with mismatched visual assets is a failed result.
