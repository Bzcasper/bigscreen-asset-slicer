# Image Generation Prompts For Frontend-Ready Bigscreen Assets

Use these prompt templates when generating raster assets for big-screen pages. The goal is to produce assets that frontend can use directly after light cropping or chroma-key removal. For screenshot reconstruction tasks, prompts should be driven by cropped reference components, not loose style descriptions.

## Core Rules

- Prefer one asset per generation prompt for important assets. If the result is a single usable file, save it directly and do not run slicer.
- Use asset sheets only for same-kind small parts, such as icon bases, corner accents, or divider lines.
- Set the target canvas before prompting. Default to `1920x1080` for big-screen pages unless the user specifies another production size.
- Treat non-standard reference images as layout and component-geometry references, not as final asset dimensions. Normalize regenerated assets to the target canvas or frontend slot.
- Crop the source image into reference components before generating: header/title rail, background rail, panel frames, KPI cards, state icons, nav base, active state, chart panel frames, and central scene. Use these crops as strict input references for imggen/editing.
- For full-dashboard screenshots, create layout-level crops before prompting any detailed asset. At minimum isolate the header, KPI strip, left column panels, central scene, chart row, right status/quality/energy panels, bottom navigation, and icon/status families. Prompt from the nearest crop first; the full screenshot is secondary context only.
- Every prompt for a crop-guided reconstruction must name the exact layout crop or component crop it is matching, such as `layout crop: right-energy` or `component crop: bottom-nav active halo`. Do not ask the model to infer small icons, frame corners, text spacing, or target positions from the whole image alone.
- Direct source crops are not final assets when they contain text, numbers, labels, table rows, chart marks, or callout copy. Use them to regenerate a clean no-text/no-data material.
- Inspect every generated frame/header/nav asset edge before accepting it. Reject ghost text, partial digits, tab remnants, tiny status dots, chart marks, scene slivers, or copied callout fragments on the border.
- State the intended frontend asset size or aspect ratio in every prompt.
- Reserve explicit empty safe zones for DOM title text, action controls, values, charts, legends, table rows, labels, icon slots, and callouts.
- Treat ECharts and similar chart interiors as component-rendered frontend content unless explicitly requested otherwise. Generate only the chart panel frame/background/title chrome and leave the plot area clean; do not generate lines, bars, axes, legends, tooltips, or labels as static UI assets.
- Use the supplied reference as a strict style lock, not loose inspiration. Do not invent unrelated sci-fi panels, different palettes, oversized glow, or new ornament systems.
- Before generation, write a style lock from the original image and reuse it in every prompt. Prompts must combine `Style lock` + nearest `Layout crop` + exact `Asset ownership`; a crop alone is not enough, and a loose style paragraph is not enough.
- Before text-to-image generation, pass the source-strategy gate. If the crop already has the exact chrome and only text/data need removal, prefer crop-guided redraw or masked image edit. Use text-to-image only when geometry drift is acceptable or the asset is missing/too dirty to redraw from a crop.
- Crop-guided redraw requires a real image input. The prompt must refer to "the provided crop image" and preserve its silhouette/anchors. A prompt that only names a local file or crop id is still text-to-image and must not be accepted as crop-guided reconstruction.
- Source crop pixels are reference only. Do not ship locally cleaned source crops as final UI assets unless the user explicitly allows source-derived fallback assets. Local post-processing is allowed on generated outputs for key removal, cropping, resizing, sheet splitting, and audit.
- For precision chrome such as title beams, bottom navigation bases, active halos, and adaptive frame parts, free text-to-image output is not acceptable unless it matches the crop's silhouette, line weight, and anchor geometry. Otherwise reject it even if the color palette is close.
- UI asset gate: generated output must be directly usable by frontend after light post-processing. It needs transparent or intentionally opaque background, clean edges, separable part boundaries, documented anchors/safe zones/title slots/action slots, no baked text/data, and no style-only mockup composition that cannot be imported as assets.
- Style audit gate: compare each generated output with its nearest crop before accepting. Check line weight, glow intensity, badge size, border radius/corner cuts, semantic colors, material density, and scale. If the generated asset looks like a different dashboard/icon system, reject it even if it is polished.
- Fidelity brief gate: before each generation, write and include a crop-specific brief with `prominence`, `lineWeight`, `glow`, `opacity`, `material`, `scale`, and `doNotAmplify`. This brief is more important than generic style language.
- Prompt preflight: remove words that commonly make the model beautify the asset beyond the crop, such as `premium`, `cinematic`, `high-detail`, `futuristic`, `strong glow`, `polished`, `armored`, and `sci-fi`, unless the crop itself clearly has those traits. Use measured crop facts instead.
- Subtle UI chrome needs subtractive prompts. Say `barely visible`, `CSS-like hairline`, `low opacity`, `do not improve visibility`, `do not thicken`, and `do not add glow nodes` when that is what the crop shows.
- Preserve the crop's geometry. If a crop has a specific clipped corner, icon badge, separator, title rail, or state icon shape, the generated asset must keep that shape instead of substituting a generic dashboard part.
- Prevent duplicate chrome. If a background crop already contains header rails or page edge frames, do not also generate a separate overlapping title beam for that same area.
- Prompts must say which layer owns top and bottom chrome. If header/footer are separate assets, background prompts must explicitly exclude header rails, title beams, bottom navigation bases, footer glow, and panel borders.
- Header/title prompts must choose the layer type explicitly: `transparent title-beam overlay`, `opaque full-width header band`, or `small header ornament`. A transparent overlay requires alpha outside the beam/rails after key removal; an opaque band must be full-width or have an exact placement box and must not pretend to be a free-floating transparent asset.
- Prefer an opaque no-text header band when the crop's title beam is blended into the dark header background. Do not force a transparent overlay if separation would create a new armored plate or bottom-navigation-like object.
- For frame/container generation, the prompt must state `outer border required` and name the specific border details to preserve. It must also state `title/header reservation required` when the crop contains title text, a title band, or a top-right control. Do not accept a clean interior surface with missing rim, corner cuts, title/header reservation, or action/control slot reservation.
- Keep all live content out of generated assets: no titles, no labels, no numbers, no charts, no tables, no business data.
- Use a flat chroma-key background for transparent assets. Default to `#00ff00`; use magenta when the asset itself contains green, including leaf, safety, running, success, or energy-saving icons.
- When removing a green chroma key from an asset that accidentally contains green semantic elements, do not use despill; despill can darken or erase the actual green icon color. Prefer regenerating on magenta.
- Require generous empty padding around the asset so it can be cropped safely.
- Ask for no cast shadow, no floor plane, no reflections, and no background variation when using chroma key.
- Ask for the asset to be horizontally and vertically centered when it is a single asset.
- Ask for edge quality: crisp antialiased edges, no green spill, no glow clipped by image borders.
- Reject assets that contain text-like noise, fake UI data, clipped glow, wrong style, wrong canvas, no usable title/action/body safe zones, or color loss after chroma-key removal.
- Detect and separate state visuals. If a reference shows selected, clicked, hover, active, warning, running, paused, disabled, or focus effects, generate the neutral base and the state overlay as separate assets.
- Create icons from a slot-by-slot semantic list. Brand, KPI, status, quality, energy, weather, and bottom-navigation icons may share style, but they must not be swapped or reused when their glyph meaning differs from the reference.
- After key removal/import, compare semantic icon colors in the rendered page. Green leaf/safety/running icons and amber/red status icons must not be darkened by green-key despill or CSS filters.
- In high-fidelity tasks, generate precision icons one at a time from individual source crops. Mixed icon sheets are allowed only after a single-icon proof shows the same badge size, rim thickness, glow strength, and pictogram grammar at the actual UI slot size.
- Do not reuse an accepted navigation icon as a KPI, quality, energy, brand, weather, or status icon unless the reference uses the same glyph in that exact slot. Similar glass material is not enough; semantic slot identity matters.
- For tiny header, KPI, metric, and footer icons, constrain visual occupancy explicitly. If the crop is a compact 48-72px UI mark, ask for a small centered icon with generous chroma-key padding and state that the visible icon should not become a large standalone emblem. This prevents the model from turning dashboard glyphs into glossy app icons.
- When the first precision icon output is over-beautified, reject it and retry with sharper negative wording: `line-art UI mark`, `not a 3D object`, `not a glossy emblem`, `thin 1-2px-looking strokes at UI size`, `occupies only the same small visual footprint as the crop`.
- For bottom navigation, prompt and spec the segmented base and the item placement separately. The base may contain dividers/boxes, but Vue must place icons and labels using measured slot anchors from the reference crop rather than equal columns.
- Bottom navigation base prompts must preserve the crop's actual full-width footer slot system. Do not let the model replace a quiet transparent footer with a centered chevron plate, thick rail, heavy trapezoid, or unrelated segmented bar. Neutral base means no icons, no labels, no subtitles, and no active/click halo.
- For panel systems that need multiple widths or heights, prefer adaptive split-frame prompts: generate only non-scalable raster parts such as clipped corners, title notches, bevel caps, glow nodes, and special joints. Let frontend CSS draw the straight horizontal and vertical connector lines.
- Adaptive split-frame sheets must be connector-ready. Generate small separated parts with clear connector stubs and empty gutters, not large L-shaped chunks of a full frame. If CSS cannot connect the parts by drawing straight 1px or 2px lines to known anchors, reject the sheet.
- Connector-ready is not enough. Run the style audit gate against the nearest frame crop: line weight, glow strength, corner cut size, glass fill density, and title-band grammar must match. If a generated kit is heavier or brighter, reject it even if it can technically be assembled.
- If a same-kind frame kit still drifts, do not keep iterating the sheet. Switch to single-frame-part crop-guided redraw: one source corner/cap crop as image input, one generated frame part output, then crop/resize the generated result to the intended frontend part size and audit in an assembly preview.
- If the original frame is not connector-friendly or decomposition changes the style, stop trying to make a kit. Generate a full same-ratio empty frame from the complete crop. Full-frame redraw is acceptable for fixed-size panels and for frame families where style fidelity matters more than adaptive reuse.
- Use a CSS/image decision before prompting. CSS may handle regular fills, masks, simple clipping, and straight connectors. Generate image assets for irregular luminous details, asymmetric cuts, bright nodes, bevel caps, short sparks, complex badges, and any ornament whose style depends on raster lighting.
- Avoid duplicate frame rendering. If PNG parts contain a corner, notch, cap, node, or highlight, the CSS layer must not redraw that same feature; CSS connectors should start and end at the recorded PNG part anchors.

## Direct-Use Decision

Use the generated file directly when all are true:

- It contains exactly one asset.
- The asset is opaque, such as a background texture or factory scene, or it already has a clean alpha channel.
- The edges are not clipped and no cleanup is needed.
- The frontend can import it as a single file.
- It matches the reference style lock and target canvas plan.

Run chroma-key removal only when a transparent asset was generated on a flat key background. Run slicing only when the image intentionally contains multiple assets or when decomposing a fixed full-dashboard mockup.

## Fidelity Brief Template

Write this before every crop-guided generation and paste it into the prompt.

```text
Fidelity brief:
- Source crop: <crop file/name>.
- UI slot: <final frontend size and role>.
- Prominence: <barely visible | subtle | medium | high>.
- Line weight: <hairline | 1px | 2px | thick>.
- Glow strength: <none | faint | local | strong>.
- Opacity/contrast: <almost blends into background | low | medium | high>.
- Material: <CSS-like hairline | dark glass fill | compact icon badge | opaque scene | etc>.
- Shape grammar: <simple rounded rectangle | clipped corner | segmented nav base | circular badge | etc>.
- Do not amplify: <rim thickness, glow, bevel, badge size, corner armor, title notch, highlight nodes, saturation, etc>.
- Must preserve: <measured silhouette, title band, title anchor, action slot, body safe zone, connector baseline, icon hue, etc>.
- Must remove: <text/data/chart/table/callout leftovers>.
```

If the brief says `prominence: barely visible` or `line weight: hairline/1px`, the prompt must explicitly say the generated result should stay low-contrast and should not be improved into a decorative standalone asset.

## Crop-Guided Reconstruction Clause

Add this clause when a source screenshot crop is available:

```text
Layout crop: <header | kpi-strip | left-production | center-scene | right-energy | bottom-nav | icon-family>.
Component crop role: <header/title rail | panel frame | status icon | nav base | active state | KPI card | central scene>.
Style lock: <paste the concise style-lock.md summary: palette, glass material, line weight, glow strength, corner grammar, icon badge language>.
Asset ownership: <background excludes header/footer | header owns top beam | bottom-nav owns footer base | frame parts own corners only and CSS owns straight connectors>.
Fidelity brief: <prominence, lineWeight, glow, opacity, material, scale, doNotAmplify>.
Use this crop as the primary visual lock. The whole dashboard reference is only secondary context. Preserve this crop's local geometry, border thickness, glow placement, color balance, corner cuts, separator density, icon silhouette, title/header reservation, action/control reservation, and text/content spacing rhythm. Regenerate a clean frontend material from it: remove all source text glyphs, numbers, labels, table data, chart marks, and callout copy. Keep only the reusable UI surface/background/icon material and reserve empty safe zones for DOM title text, controls, and body content.
For container/frame assets, outer border required: include the full rim, clipped corners, title/header band area, action/control slot area, inner line, and local glow visible in the crop unless the ownership plan assigns that detail to CSS connector lines.
Do not amplify: do not make the asset more decorative, thicker, brighter, glossier, or more standalone than the provided crop.
```

Use crop-guided reconstruction before free generation. A free generation is acceptable only when the crop is missing or unusable.

## Layout-Crop Prompt Clause

Add this clause when the reference is a full dashboard screenshot and the current asset belongs to one layout region:

```text
Divide-and-conquer reference: use the supplied `<region-name>` layout crop as the nearest style and geometry source for this asset. Match only the visual language visible in this region: local frame cuts, connector baselines, icon hue, content safe-zone spacing, line density, and glow intensity. Do not borrow unrelated ornaments from other regions. Do not redesign from the whole dashboard. Output a frontend-ready clean asset for the target slot with no baked text/data.
```

Use this clause together with the crop-guided clause for KPI cards, right-side metric blocks, central callout cards, bottom navigation slots, state icons, and any asset whose small details were previously missed in a whole-image audit.

## Shared Style Clause

Append this clause to every prompt when matching the carton-factory dashboard reference:

```text
Style reference: use the provided reference image as a strict visual lock, not loose inspiration. Match only what is actually visible in the crop: deep navy surfaces, measured cyan rim strength, measured emerald/amber semantic accents, exact corner grammar, exact inner stroke weight, compact dense enterprise layout, and the crop's real material density. Do not make the result more premium, more futuristic, more glowing, more beveled, or more decorative than the crop. Do not introduce unrelated ornaments, purple gradients, cartoon/vector simplification, oversized bloom, random geometry, or a different icon/panel system.
```

## Standard Canvas And Safe-Zone Clause

Add this clause whenever the reference image is not already the final target canvas:

```text
Target canvas: design for <1920x1080 or user-specified canvas>; the supplied reference image dimensions are style input only. Target asset size/aspect: <frontend asset width x height or ratio>. Content safe zones: leave clean empty usable space for DOM-rendered <title/value/chart/table/legend/callout/label> with <insets or band sizes>. For containers with title text or top-right controls in the crop, define separate titleBand, titleAnchor, actionSlot, and bodySafeZone. Do not fill the safe zone with decorative clutter, fake text, charts, labels, numbers, or baked UI data.
```

## Panel Frame Prompt

Use for large, medium, and tall panel frames.

```text
Use case: productivity-visual
Asset type: frontend-ready transparent panel frame
Primary request: Generate one empty dashboard panel frame only.
Shape: <describe the exact crop shape; do not invent cuts/notches>. Preserve the crop's measured border and fill. If the crop is a simple quiet rounded rectangle, keep it simple and quiet.
Style reference: append the Shared Style Clause and match the supplied panel/frame crop when available.
Fidelity brief: <prominence: barely visible/subtle/etc; lineWeight: hairline/1px/etc; glow: none/faint/local/etc; opacity/material; scale; doNotAmplify>.
Target canvas: design for <1920x1080 or user-specified canvas>; the reference image dimensions are style input only.
Target asset size/aspect: <frontend panel width x height or ratio>.
Title/header reservation required: preserve the crop's top title/header band even after removing the title glyphs. Keep a clean left titleAnchor and, when present in the crop, a clean top-right actionSlot/control capsule area. Do not let the chart/body area begin at the top edge.
Content safe zones: reserve an empty top title band of <height>, a titleAnchor box of <x/y/width/height>, an actionSlot box of <x/y/width/height or none>, and an empty inner chart/table/content bodySafeZone with <left/right/top/bottom> padding. Keep the center readable and low-clutter.
Background: perfectly flat solid #00ff00 chroma-key background.
Composition: single centered asset, generous padding on all sides, no clipping, glow fully visible.
Frontend constraints: empty interior, no title text glyphs, no dropdown text, no icons, no numbers, no charts, no table rows, no sample content.
Avoid: collapsing the title/header band, placing body content in the title band, deleting the top-right action/control reservation when the crop has one, text, data, watermark, random glyphs, copied edge pixels, ghost digits, tab remnants, status dots, scene fragments, cast shadow, floor plane, reflection, gradient/texture in the green background, green inside the asset, clipped glow, thicker rim than crop, stronger glow than crop, extra decorative nodes, extra notches, armored corners.
```

## Full Fixed Frame Redraw Prompt

Use this when a reference frame is not suitable for adaptive splitting or when decomposition changes the original style.

```text
Use case: productivity-visual
Asset type: frontend-ready transparent full dashboard panel frame
Primary request: Redraw one complete empty dashboard panel frame from the provided crop. Preserve the crop's full-frame style exactly: border rhythm, thin cyan rim, dark navy glass fill, rounded/clipped corners, title/header band, top-right action/control reservation when present, local glow, and subtle line density. Remove all text glyphs, numbers, charts, axes, legends, labels, table rows, and sample content.
Source strategy: crop-guided redraw from the actual full panel crop, not text-to-image. The source crop is reference input only; final pixels must be generated/redrawn.
Fidelity brief: <paste crop facts, for example: prominence=subtle, lineWeight=1px, glow=faint local, material=almost-CSS hairline over dark glass, scale=304x224, doNotAmplify=rim/glow/corner nodes/title notch>.
Ownership: this PNG owns the full panel background, border, title/header band surface, corners, local glow, and glass fill for this ratio. CSS/Vue owns DOM title text, top-right controls, charts, tables, and content placement inside the recorded title/action/body safe zones.
Target asset size/aspect: <same as the frontend panel slot, e.g. 304x224>.
Title/header reservation required: preserve the empty title/header band height from the crop. Remove the title text itself, but keep the top-left titleAnchor as clean negative space and keep the top-right actionSlot/control capsule reservation if the reference crop has one. Do not flatten the frame into a generic empty box.
Content safe zones: define titleBand, titleAnchor, actionSlot, and bodySafeZone with explicit coordinates/insets. BodySafeZone begins below the title/header band.
Background: perfectly flat solid #00ff00 chroma-key background, or generated transparent background if available.
Composition: one full frame centered, complete outer edge visible, no clipping.
Frontend constraints: empty title and content zones, no title glyphs, no dropdown text, no icons, no numbers, no charts, no axes, no labels, no table rows, no watermark.
Style audit: must match the source crop's subtle line weight, low glow, title/header spacing, action-slot placement, and body-safe-zone start at the final UI size. Reject if the frame becomes thicker, brighter, more armored, more visible as a standalone asset, collapses title space, removes the action/control slot reservation, or changes into a different style. Do not add title notches, glow nodes, bevel caps, or decorative corners unless they are clearly visible in the crop.
```

## Adaptive Split-Frame Prompt

Use this instead of a full panel-frame prompt when the same frame style must support horizontal and vertical resizing. The generated output should be a small part sheet, not a complete box. Frontend should assemble the frame with PNG corner/cap assets plus CSS connector lines.

```text
Use case: productivity-visual
Asset type: frontend-ready transparent adaptive split-frame part sheet
Primary request: Generate a clean UI asset sheet containing only the non-scalable parts of one dashboard panel frame system.
Reference crop role: panel frame / KPI card frame / chart panel frame. Use the supplied crop as a strict reconstruction guide.
Parts to generate: top-left clipped corner, top-right clipped corner, bottom-left clipped corner, bottom-right clipped corner, title notch/cap, small edge glow node, optional short highlight spark. Do not generate the long straight top/bottom/left/right lines; those will be drawn by CSS.
Shape and style: preserve the reference crop's angular corner cuts, bevel caps, cyan rim glow, thin inner strokes, line thickness, dark navy glass material, and restrained light density. Each part must align cleanly with 1px or 2px CSS connector lines.
Connector anchors: before generation or slicing, define exact connector baselines such as `top connector y=4px`, `bottom connector y=<height-4px>`, `left connector x=2px`, and `corner cut=36px`. Every corner, title notch, short highlight, cap, and glow node must be cropped from the same connector baseline so only the CSS line length changes at runtime.
Connector-ready structure: each corner should be a small tile, for example 72x72 or 96x96, containing only the local corner stroke/glow and short connector stubs that exit the tile exactly on the top/bottom/left/right baselines. Do not include large panel fill blocks, long edge segments, or a full L-shaped quadrant. Keep the inside of the corner transparent or minimal; CSS will draw the clipped fill separately.
Target canvas: design for <1920x1080 or user-specified canvas>; the reference image dimensions are style input only.
Target asset sizes: each corner/cap should fit the intended frontend fixed part size, for example 96x64, 116x78, or user-specified dimensions. Keep straight connector endpoints clean and horizontal/vertical.
Background: perfectly flat solid #00ff00 chroma-key background, or clean alpha if supported.
Composition: arrange parts in a simple labeled-free grid with large gutters. Every part must be fully separated, fully visible, and include enough padding for glow.
Frontend assembly: corners and notches remain fixed-size PNGs; CSS will draw horizontal and vertical connector lines with linear-gradient and box-shadow. The panel fill/background must be a separate shaped layer clipped or masked to the same corner-cut polygon; never leave a rectangular fill behind diagonal corners. The final frame must work at multiple widths and heights without stretching raster corners.
Duplicate-chrome rule: CSS must draw only the long straight connectors between PNG anchors. Do not redraw diagonal corner lines, local notches, bright dots, bevel caps, or short highlight sparks in CSS when those details are present in the generated part sheet.
Frontend constraints: no full rectangle frame, no center fill content, no title text, no labels, no numbers, no charts, no table rows, no icons, no watermark.
Avoid: generating a single full panel box, baked sample content, random glyphs, mismatched connector baselines, rectangular corner fill, thick sci-fi borders, clipped glow, cast shadow, floor plane, non-uniform chroma background, green inside the asset.
```

CSS assembly guidance for the frontend:

```css
.adaptive-frame {
  position: relative;
}

.adaptive-frame::before {
  position: absolute;
  inset: 0;
  content: '';
  clip-path: polygon(
    var(--cut) 0,
    calc(100% - var(--cut)) 0,
    100% var(--cut),
    100% calc(100% - var(--cut)),
    calc(100% - var(--cut)) 100%,
    var(--cut) 100%,
    0 calc(100% - var(--cut)),
    0 var(--cut)
  );
}

.corner-tl,
.corner-tr,
.corner-bl,
.corner-br,
.title-notch {
  position: absolute;
  pointer-events: none;
}

.edge-top,
.edge-bottom {
  position: absolute;
  right: var(--corner-w);
  left: var(--corner-w);
  height: 1px;
  background: linear-gradient(90deg, transparent, rgb(80 235 255 / 90%), transparent);
  box-shadow: 0 0 10px rgb(0 200 255 / 35%);
}

.edge-left,
.edge-right {
  position: absolute;
  top: var(--corner-h);
  bottom: var(--corner-h);
  width: 1px;
  background: linear-gradient(180deg, transparent, rgb(18 207 255 / 64%), transparent);
}
```

## Title Beam Prompt

```text
Use case: productivity-visual
Asset type: frontend-ready transparent title beam ornament
Primary request: Generate one top header title beam ornament only, without text. This is a transparent overlay, not a full rectangular header screenshot.
Shape: preserve the provided header/title crop's measured beam geometry, symmetric left/right wings, central title-safe opening, subtitle rail, thin cyan light strip, dark navy glass plates, circuit-line detailing, bevels, and angular cut ends. Do not invent extra side rails or change the beam into a generic background texture strip.
Style reference: append the Shared Style Clause and match the supplied title/header crop when available.
Fidelity brief: include titleAnchor, subtitleAnchor, beam width, rail height, lineWeight, glow strength, opacity, and doNotAmplify. If the crop is subtle, do not thicken the horizontal rail or brighten the side wings.
Ownership: this PNG owns only the title beam/rail ornament behind the DOM title and subtitle. Page background owns generic ambient texture. DOM owns title text, subtitle text, logo, weather, date/time, and any right status widgets unless separately specified.
Target canvas: design for <1920x1080 or user-specified canvas>; the reference image dimensions are style input only.
Target asset size/aspect: <frontend header ornament width x height or ratio>.
Content safe zones: keep a clean central titleAnchor with enough height for DOM title text and a clean subtitleAnchor below it. Do not place bright details where the title/subtitle will sit.
Background: perfectly flat solid #00ff00 chroma-key background.
Composition: single centered asset, wide landscape, generous padding, glow fully visible.
Frontend constraints: no title text, no subtitle text, no logo, no date/time, no weather, no numbers.
Avoid: opaque dark rectangular background outside the beam, words, watermark, random glyphs, cast shadow, floor plane, green spill, clipped glow, duplicated full-width header rails already owned by background/header band.
```

## Opaque Header Band Prompt

Use this when the reference header/title beam is fused with a dark header background and a transparent overlay would change the style.

```text
Use case: productivity-visual
Asset type: frontend-ready opaque header band
Primary request: Redraw one clean no-text header band from the provided header/title crop. Preserve the reference's dark navy header background, subtle title-beam geometry, side circuit wings, lower cyan rail, central title-safe space, and subtitle-safe space. Remove title/subtitle glyphs only.
Layer type: opaque header band. This image owns the covered header-band background and title-beam chrome for its exact placement. The page ambient background should sit behind it but not duplicate its top chrome.
Style reference: append the Shared Style Clause and match the supplied header/title crop.
Fidelity brief: include header band size, titleAnchor, subtitleAnchor, beam line weight, glow strength, side wing density, opacity, and doNotAmplify.
Target asset size/aspect: <header band width x height, e.g. 940x78 or 1536x78>.
Content safe zones: keep a clean titleAnchor and subtitleAnchor for DOM text. Do not fill those zones with new decoration.
Frontend constraints: no title text, no subtitle text, no logo, no date/time/weather, no numbers, no watermark.
Avoid: transparent green background, armored bottom-nav-like plate, thick beveled rail, new center badge, random glyphs, fake text, stronger glow than the crop, changing the side-wing rhythm.
```

## Clean Factory Scene Prompt

Use this for the central live-video panel background. This asset should not contain UI callouts because Vue will render those.

```text
Use case: productivity-visual
Asset type: frontend-ready factory scene image for dashboard video panel
Primary request: Generate a clean realistic carton factory workshop scene only.
Subject: corrugated cardboard production machinery, blue and white industrial equipment, conveyors, stacks of cardboard sheets on pallets, yellow guardrails, glossy factory floor, ceiling lights, deep perspective.
Style reference: append the Shared Style Clause and match the supplied central workshop crop when available: high-detail AI-rendered machinery, cinematic industrial lighting, realistic materials, crisp edges, blue/cyan cockpit mood.
Target canvas: design for <1920x1080 or user-specified canvas>; the reference image dimensions are style input only.
Target asset size/aspect: <frontend scene width x height or ratio>.
Composition: wide 16:6 scene, camera at human eye level, machine centered, enough empty margin for frontend callout tags, no dashboard frame around it.
Content safe zones: leave clean margins for DOM callout tags and overlays; keep the main machine visible without covering all edges.
Frontend constraints: no UI labels, no status tags, no Chinese text, no numbers, no charts, no tables, no title bar, no watermark.
Avoid: cartoon, flat illustration, fake text on signs, random labels, people in foreground, low-detail machinery, blurry image, overexposed glow.
```

## Clean Scene With Blank Callout Cards Prompt

Use this only when the reference already has callout card surfaces that should remain part of the scene material while their text becomes DOM.

```text
Use case: productivity-visual
Asset type: frontend-ready central scene image with blank UI callout card materials
Primary request: Reconstruct the supplied central scene crop as a clean frontend scene asset. Preserve the factory perspective, machinery detail, lighting, and the callout card surfaces, but remove all baked callout text, values, labels, and status copy.
Reference crop role: central scene with callout cards. Use it as a strict reconstruction guide.
Callout cleanup: every source callout card must be fully covered or regenerated as a blank dark navy glass card at the same anchor and size. Do not leave partial source text, green status words, numbers, or ghosted labels behind the blank cards. Do not shift the blank cards away from their source positions.
Frontend anchors: output notes must record each blank card anchor and size as percentages or pixels so Vue text can be positioned exactly over the card.
Target canvas: design for <1920x1080 or user-specified canvas>; the reference image dimensions are style input only.
Target asset size/aspect: <frontend scene width x height or ratio>.
Style reference: append the Shared Style Clause and match the supplied central workshop crop.
Frontend constraints: no baked text, no numbers, no status labels, no chart/table content, no watermark.
Avoid: oversized blank cards that cover machinery, misplaced callout cards, residual source text, duplicated DOM callout backgrounds, cartoon machinery, low-detail blur.
```

## Icon Base Prompt

Use this for empty icon containers, not the icon glyph itself.

```text
Use case: productivity-visual
Asset type: frontend-ready transparent icon base
Primary request: Generate one empty metric icon base only.
Shape: <hexagonal plate | circular blue orb> with dark navy glass center, cyan-blue beveled rim, inner glow, subtle depth.
Style reference: append the Shared Style Clause and match the supplied icon/base crop when available.
Target canvas: design for <1920x1080 or user-specified canvas>; the reference image dimensions are style input only.
Target asset size/aspect: <frontend icon base width x height or square ratio>.
Content safe zones: keep the center empty for a DOM or separate raster pictogram when this is only the base.
Background: perfectly flat solid #00ff00 chroma-key background.
Composition: single centered asset, square canvas, generous padding, glow fully visible.
Frontend constraints: empty center, no pictogram, no text, no numbers.
Avoid: logo, watermark, random marks, cast shadow, green spill, clipped glow.
```

## Complex Icon Prompt

Use this when the reference uses high-detail dashboard pictograms that CSS shapes cannot reproduce. Generate icons as raster assets and let Vue render labels, numbers, units, and status text.

```text
Use case: productivity-visual
Asset type: frontend-ready transparent complex dashboard icon
Primary request: Generate one complex dashboard icon only: <brand cube/carton mark | production monitor/people | box stack | clipboard order | delivery truck | OEE gear | safety shield | quality medal | user/customer | energy cycle | power lightning | gas flame | water droplet | green leaf | machine cog | report table | weather sun-cloud | alarm triangle | AGV vehicle>.
Shape: icon may include its own glass badge/base such as a beveled hexagon, circular orb, or shield plate when useful. The pictogram must be centered and recognizable at 48-72px in a dashboard.
Semantic lock: this icon must match the assigned UI slot from the reference. Do not substitute a box stack for production navigation, a leaf for energy management navigation, or a generic gear for a specialized quality/status/weather icon.
Style reference: append the Shared Style Clause and match the supplied icon crop when available. Use emerald, amber, or red only where semantically useful.
Target canvas: design for <1920x1080 or user-specified canvas>; the reference image dimensions are style input only.
Target asset size/aspect: <frontend icon width x height or square ratio>.
Background: perfectly flat solid #00ff00 chroma-key background. Use magenta or clean alpha instead when the icon contains semantic green.
Composition: single centered icon, square canvas, generous padding, no clipping, glow fully visible.
Frontend constraints: no Chinese text, no English text, no numbers, no units, no chart marks, no table rows, no logo, no watermark.
Avoid: random glyphs, fake letters, badge labels, cast shadow, floor plane, reflection, gradient/texture in the green background, green inside the icon unless the icon is the green leaf.
```

## Single Precision Icon Redraw Prompt

Use this for high-fidelity KPI, quality, energy, brand, weather, status, and bottom-navigation icons. This prompt requires the actual source icon crop as image input. If the image generation path cannot attach that crop, mark the asset `blocked-needs-image-edit-input`.

```text
Use case: high-fidelity dashboard reconstruction
Asset type: frontend-ready transparent precision icon
Primary request: Edit/redraw the provided icon crop into one clean reusable UI icon for the `<semantic slot>` slot. Preserve the crop's exact badge scale, rim thickness, pictogram grammar, local glow strength, semantic hue, and compact dashboard size. Remove only dirty background pixels, text fragments, numbers, labels, and source screenshot residue.
Provided crop role: `<brand cube | weather sun-cloud | KPI production | KPI order | KPI shipping | KPI OEE | safety shield | quality material | quality process | quality finished | quality complaint | energy electric | energy gas | energy water | energy leaf | bottom nav production | bottom nav quality | bottom nav equipment | bottom nav energy | bottom nav report | bottom nav system>`.
Style lock: append the Shared Style Clause and match the provided crop, not a generic icon family.
Fidelity brief: include final UI slot size, source crop size, badge diameter/box size, lineWeight, glow, opacity, semantic color, and doNotAmplify.
Target asset size/aspect: output one square icon, normally `58x58` or the measured frontend slot. Keep enough transparent padding for glow but do not enlarge the badge relative to the crop.
Background: clean alpha preferred. If alpha is unavailable, use flat magenta chroma key when the icon contains green semantic pixels; otherwise use flat green key.
Frontend constraints: no Chinese text, no English text, no numbers, no units, no labels, no table/chart marks, no base/nav/footer/panel chrome around the icon.
Avoid: bigger glossy badge, thicker cyan ring, stronger glow, new pictogram meaning, swapped semantic glyph, generic app icon style, fake letters, clipped glow, green key collision with semantic green, reused navigation glyph in KPI/metric slots unless the crop proves it.
Acceptance: audit the processed icon at its actual UI size against the source crop. Reject if badge size, rim thickness, glow, pictogram meaning, or hue reads as a different family.
```

## Precision Icon Retry Clause

Use this after a generated icon is recognizable but too large, too glossy, too 3D, or too decorative.

```text
Retry as a dashboard UI glyph, not a standalone app icon. The visible mark must keep the same small footprint as the source crop and should occupy only about <20-35% or measured ratio> of the square canvas, leaving large flat chroma-key padding. Use thin line-art / compact badge treatment at the final UI size. Do not add realistic 3D surfaces, heavy bevels, thick rim, strong glow, large emblem framing, extra details, or decorative lighting. Preserve the source crop's simple silhouette and semantic glyph exactly.
```

## High-Fidelity Header Brand And Weather Prompt

Use these as single precision icon redraws, not CSS replacements.

```text
Brand mark: redraw the provided header brand/cube crop as one compact transparent icon. Preserve the original cube/carton mark silhouette, cyan/blue glass rim, white internal planes, and tiny dashboard scale. Do not turn it into a generic 3D logo, package icon, or large glossy badge.

Weather mark: redraw the provided header weather crop as one compact transparent sun-cloud dashboard icon. Preserve the original light blue/white line style and size. Do not add text, temperature digits, or a bigger circular badge.
```

## Complex Icon Sheet Prompt

Use this for a dashboard icon family. Keep only icons in the sheet; do not mix panels, scenes, title beams, charts, or text.

```text
Use case: productivity-visual
Asset type: same-kind transparent complex dashboard icon sheet
Primary request: Generate a clean asset sheet containing exactly these separate complex dashboard icons: <list icons>.
Style reference: append the Shared Style Clause and match the supplied icon crop when available. Use emerald, amber, or red only where semantically useful.
Crop-guided rule: use the actual provided icon crop as image input and redraw its badge material, scale, rim thickness, glow intensity, and compact pictogram language. Do not produce larger glossy generic badges. If the output is brighter, thicker, or more game-like than the crop, reject it.
If a same-kind icon sheet still drifts, do not keep iterating the sheet. Switch to single-icon crop-guided redraw: one source badge crop as image input, one generated icon output, then crop/resize the generated result to the original UI slot size and audit at that size.
Target canvas: design for <1920x1080 or user-specified canvas>; the reference image dimensions are style input only.
Target asset size/aspect: each icon must fit the intended frontend icon box, usually square.
Background: perfectly flat solid #00ff00 chroma-key background.
Composition: simple grid, every icon fully separated by large green gutters, no overlap, no clipping, no labels, consistent icon scale and lighting.
Frontend constraints: icons only; no Chinese text, no English text, no numbers, no units, no charts, no sample data, no full dashboard screenshot.
Avoid: mixed UI panels, fake labels, random glyphs, inconsistent styles, cast shadows, non-uniform green background, green spill, clipped glow.
```

## Bottom Navigation Split Prompt

Use this when a reference bottom menu has a base bar plus a selected, clicked, hover, or active glow. Generate those as separate assets. The base bar must stay neutral, and the active/click effect must be an overlay that frontend can move to any menu item.

```text
Use case: productivity-visual
Asset type: frontend-ready separated bottom navigation assets
Primary request: Generate bottom navigation assets from the provided crop without redesigning the footer. Prefer one prompt per asset when fidelity matters: neutral base first, active overlay second.

Neutral base prompt:
Generate one full-width low-profile bottom navigation base only. Preserve the crop's actual footer width, transparent dark navy glass surface, weak top/bottom hairlines, subtle item slot rhythm, faint vertical separators, and quiet cyan edge accents. Remove the selected/active glow, all icon badges, all pictograms, all labels, all subtitles, and all text glyphs. Keep only the neutral reusable footer base and empty item landing zones.

Active overlay prompt:
Generate one standalone active/click state indicator only, matching the crop's first-item cyan elliptical platform/ring glow. It must be separate from the base bar, no icon, no text, and movable to any nav slot.

Style reference: append the Shared Style Clause and match the supplied bottom-nav crop when available.
Fidelity brief: include prominence, lineWeight, glow, opacity, material, scale, slot count, slot anchors, and doNotAmplify. If the crop is subtle, say barely visible, do not thicken, do not center into a decorative standalone object, and keep weaker than normal UI asset defaults.
Target canvas: design for <1920x1080 or user-specified canvas>; the reference image dimensions are style input only.
Target asset size/aspect: base bar must match the frontend footer width/height exactly; active indicator must fit one nav item slot.
Slot manifest: record each measured item slot left/width plus iconCenter and labelAnchor. Do not assume equal slots unless the crop proves equal spacing.
Content safe zones: base bar must reserve repeated item slots with empty icon and label zones; the active overlay must remain movable to any slot.
Background: perfectly flat solid #00ff00 chroma-key background.
Composition: for base-only generation, one full-width footer base centered with generous padding and no clipped glow. For an asset sheet, place Asset 1 centered in the upper half and Asset 2 centered in the lower half, with large green gutters between assets.
Frontend constraints: no Chinese text, no English text, no numbers, no icons, no labels, no charts, no table rows, no logo, no watermark.
Avoid: baking the selected item into the base bar, putting the active circle inside the base bar, random glyphs, fake UI text, cast shadow, floor plane, background variation, green inside the assets, clipped glow, centered hex/chevron bars, thick beveled rails, heavy glow, oversized separators, changing the reference slot rhythm.
```

## State Overlay Prompt

Use this when a screenshot crop contains an obvious state effect on one repeated UI item. Examples include selected tab glow, clicked bottom-menu halo, active card light, warning pulse, running indicator aura, disabled dim layer, or focus outline.

```text
Use case: productivity-visual
Asset type: frontend-ready transparent state overlay
Primary request: Generate one standalone <selected/clicked/hover/active/warning/running/paused/disabled/focus> state overlay only for <target component type>.
Shape: match the reference state effect geometry exactly: <ellipse ring under icon | tab highlight strip | corner glow | warning pulse halo | small running light | dim glass layer>. Do not include the component base, icon, text, number, or label.
Style reference: append the Shared Style Clause and match the supplied state crop when available.
Target canvas: design for <1920x1080 or user-specified canvas>; the reference image dimensions are style input only.
Target asset size/aspect: overlay must fit the intended frontend component state box.
Background: perfectly flat solid #00ff00 chroma-key background.
Composition: single centered overlay, generous transparent padding after chroma-key removal, no clipping, glow fully visible.
Frontend constraints: overlay must be movable and reusable by CSS positioning; no Chinese text, no English text, no numbers, no icons, no labels, no logo, no watermark.
Avoid: baking the neutral base into the overlay, random glyphs, fake UI text, cast shadow, floor plane, background variation, clipped glow.
```

## Background Texture Prompt

```text
Use case: productivity-visual
Asset type: frontend-ready dashboard background texture
Primary request: Generate a clean full-screen dark navy dashboard background texture with no component chrome.
Style reference: append the Shared Style Clause and match the supplied background crop when available.
Style: subtle grid, faint circuit lines, soft blue glows, low-contrast factory cockpit atmosphere, no focal UI components.
Asset ownership: use this background only as the page's ambient backing. If separate header, footer, panel, and navigation assets are planned, this background must not include top title beams, top rails, bottom navigation bars, footer rails, panel borders, KPI cards, chart frames, selected halos, or nav slot boxes.
Zone ownership check: the top header zone and bottom footer zone should contain only generic low-contrast texture unless the manifest says the background owns header/footer chrome. Do not place recognizable symmetrical title-beam geometry in the top zone or navigation-base geometry in the bottom zone when those are separate assets.
Target canvas: generate for <1920x1080 or user-specified canvas>; do not use a non-standard reference image size.
Composition: 16:9 landscape, seamless enough for full viewport cover, center kept low-detail so panels remain readable.
Content safe zones: keep panel-heavy regions low-contrast so DOM text, charts, and panel frames remain readable.
Frontend constraints: no text, no logos, no panel frames, no title beam, no header rail, no bottom nav, no charts, no fake data, no bright clutter.
Avoid: random words, watermark, large decorative objects, strong bokeh blobs, one-note purple gradient, top V-shaped title rail, bottom nav platform, selected active glow.
```

## Same-Kind Asset Sheet Prompt

Use only for small decorative pieces. Do not mix panel frames, scenes, icons, and backgrounds in one sheet.

```text
Use case: productivity-visual
Asset type: same-kind transparent asset sheet
Primary request: Generate a clean asset sheet containing <same-kind asset description> only.
Background: perfectly flat solid #00ff00 chroma-key background.
Composition: arrange each asset in a simple grid, every asset fully separated by large green gutters, no overlap, no clipping, no labels.
Style reference: append the Shared Style Clause and match the supplied same-kind crop when available.
Target canvas: design for <1920x1080 or user-specified canvas>; the reference image dimensions are style input only.
Target asset size/aspect: each item must match its intended frontend slot.
Content safe zones: if the asset is a container, reserve empty DOM content space; if it is decorative, keep it single-purpose.
Frontend constraints: no text, no numbers, no charts, no sample data, no full dashboard screenshot.
Avoid: mixed asset types, inconsistent styles, cast shadows, non-uniform green background, green spill, clipped glow.
```

## Bad Prompt Patterns

Avoid prompts like:

```text
Generate a dashboard asset sheet with panels, charts, icons, title, data and factory scene.
```

This usually produces a nice mockup but poor frontend assets: baked text, mixed scales, hard-to-crop frames, inconsistent icon styles, unusable chart/table content, and no reliable safe zones for DOM content.
