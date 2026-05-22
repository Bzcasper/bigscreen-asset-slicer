# Slice Spec Reference

## Minimal Spec

```json
{
  "source": "generated-dashboard.png",
  "outputDir": "<app>/src/assets/bigscreen/overview",
  "baseWidth": 1920,
  "baseHeight": 1080,
  "targetCanvas": {
    "width": 1920,
    "height": 1080,
    "note": "Reference image guides layout and component geometry; regenerated assets are normalized to the target canvas."
  },
  "referenceCrops": [
    {
      "name": "header-title-rail",
      "role": "title-ornament-reference",
      "box": [360, 0, 820, 86],
      "regenerate": true,
      "remove": ["title text", "subtitle text"],
      "preserve": ["top rail geometry", "cyan glow", "line density"]
    }
  ],
  "assets": [
    {
      "name": "background",
      "category": "background",
      "role": "page-background",
      "box": [0, 0, 1920, 1080],
      "format": "webp",
      "quality": 92,
      "zIndex": 0
    },
    {
      "name": "left-panel-frame",
      "category": "panels",
      "role": "panel-frame",
      "box": { "x": 32, "y": 126, "w": 456, "h": 386 },
      "format": "png",
      "trim": false,
      "contentInsets": { "top": 44, "right": 24, "bottom": 22, "left": 24 },
      "safeZone": { "x": 24, "y": 58, "w": 408, "h": 298 },
      "zIndex": 10
    },
    {
      "name": "adaptive-panel-corners",
      "category": "frame-parts",
      "role": "adaptive-split-frame-parts",
      "box": [40, 40, 420, 220],
      "format": "png",
      "trim": true,
      "assembly": {
        "mode": "css-connected-frame",
        "fixedParts": [
          "corner-top-left",
          "corner-top-right",
          "corner-bottom-left",
          "corner-bottom-right",
          "title-notch",
          "edge-node"
        ],
        "cssConnectors": ["top", "right", "bottom", "left"],
        "connectorThickness": 1,
        "connectorAnchors": {
          "topY": 4,
          "bottomYFromBottom": 4,
          "leftX": 2,
          "rightXFromRight": 2,
          "cornerCut": 36
        },
        "fillClipPath": "polygon(36px 0, calc(100% - 36px) 0, 100% 36px, 100% calc(100% - 30px), calc(100% - 36px) 100%, 36px 100%, 0 calc(100% - 30px), 0 36px)",
        "minWidth": 280,
        "minHeight": 120
      },
      "contentInsets": { "top": 42, "right": 24, "bottom": 22, "left": 24 },
      "zIndex": 10
    }
  ]
}
```

## Top-Level Fields

- `source`: Source image path. Relative paths resolve from the spec file.
- `outputDir`: Directory for generated files. Relative paths resolve from the spec file.
- `manifest`: Optional manifest path. Defaults to `<outputDir>/manifest.json`.
- `baseWidth`: Design canvas width in pixels.
- `baseHeight`: Design canvas height in pixels.
- `targetCanvas`: Optional note object describing the production canvas when the source/reference image dimensions are not the final canvas.
- `styleNotes`: Optional short object or string describing the strict visual lock extracted from the reference.
- `regions`: Optional list of layout-level reference crops for divide-and-conquer reconstruction and review. Use this before generating assets when the reference is a full dashboard screenshot. Typical regions: header, KPI strip, left panels, central scene, chart panels, right status/quality/energy panels, bottom navigation, and icon/status families.
- `referenceCrops`: Optional list of source crop boxes used as imggen/editing references. Use this to prove generated assets were crop-guided instead of loosely prompted. `regenerate: true` means the crop itself is not a final asset.
- `sceneCalloutAnchors`: Optional list of blank card anchors for cleaned scene assets. Use this when the scene keeps no-text callout card materials and Vue must place DOM text over the exact same positions.
- `assets`: Array of asset entries.

## Asset Fields

- `name`: Stable lowercase-ish identifier. Used for filenames when `file` is omitted.
- `category`: Output subfolder, such as `background`, `panels`, `decorations`, `icons`, `effects`, or `misc`.
- `role`: Semantic use, such as `page-background`, `panel-frame`, `title-ornament`, `divider`, `corner`, `glow`, or `icon`.
- `box`: Crop rectangle. Use `[x, y, w, h]`, `{ "x": 0, "y": 0, "w": 100, "h": 80 }`, or `{ "left": 0, "top": 0, "right": 100, "bottom": 80 }`.
- `format`: `png`, `webp`, `jpg`, or `jpeg`. Defaults to `png`.
- `quality`: WebP/JPEG quality. Defaults to `92`.
- `file`: Optional output path relative to `outputDir`.
- `zIndex`: Suggested stacking order in the reconstructed page.
- `opacity`: Optional CSS opacity hint.
- `repeat`: Optional CSS repeat hint for texture strips.
- `semanticSlot`: Optional exact UI meaning for icon assets, such as `header-brand`, `kpi-production`, `nav-production-monitor`, `nav-energy-cycle`, `energy-leaf`, `status-running`, or `weather-sun-cloud`. Use this to prevent accidental icon reuse across unlike slots.
- `stateAnchor`: Optional anchor metadata for overlay assets. Record what visual element the overlay is positioned against, such as `nav-icon-center`, `tab-center`, or `status-dot-center`, plus normalized anchor coordinates when useful.
- `navigationSlots`: Optional top-level array for divided bottom navigation bars. Record each slot's left/width and icon/text anchors from the reference crop so frontend placement does not fall back to equal columns.
- `contentInsets`: Optional `{ "top", "right", "bottom", "left" }` padding for DOM content inside a container asset.
- `safeZone`: Optional `{ "x", "y", "w", "h" }` rectangle inside an asset for DOM-rendered content such as titles, charts, tables, legends, values, labels, or callouts.
- `safeZones`: Optional array when an asset has multiple reserved DOM zones, such as bottom navigation icon slots plus label slots.
- `assembly`: Optional instructions for frontend reconstruction. Use this for adaptive split-frame systems where fixed PNG parts are combined with CSS connector lines instead of stretching one full frame bitmap.
  - `connectorAnchors`: Required for adaptive split frames. Records the shared crop/line baseline so every corner, notch, spark, and CSS connector lands on the same line.
  - `fillClipPath`: Required when the panel has clipped/diagonal corners. The CSS fill layer should use this polygon or an equivalent mask so no rectangular background shows behind missing corners.
  - `renderBoundary`: Optional note describing which visual features are owned by CSS versus image parts. Use it to prevent duplicate chrome; for example, CSS owns only straight connectors and clipped fill, while PNG parts own corners, notches, caps, glow nodes, and short highlights.
- `trim`: Boolean. When true, trim empty borders after cropping.
- `trimMode`: `alpha` or `solid`. `alpha` trims transparent pixels. `solid` trims border pixels similar to the crop's top-left color.
- `trimTolerance`: Color tolerance for `solid` trim. Defaults to `8`.
- `padding`: Pixels to add back around a trimmed crop. Defaults to `0`.

## Recommended Categories

- `background`: Full-screen or section-level opaque backing images.
- `panels`: Reusable frames, headers, and containers.
- `decorations`: Title ornaments, corner accents, brackets, lines, dividers.
- `effects`: Glows, bloom layers, scanlines, light streaks, grid textures.
- `icons`: Static pictograms that are part of the visual language.
- `frame-parts`: Non-scalable panel pieces such as clipped corners, title notches, bevel caps, glow nodes, and short highlight sparks for CSS-connected adaptive frames.

## Asset Generation Prompts

Read `imagegen-prompts.md` before generating assets. Prefer one asset per generation prompt for major assets. Every generation plan should state the target canvas, intended frontend asset size, reference style lock, and content safe zones:

```text
Use the supplied panel-frame crop as a strict reconstruction guide.
Generate one clean empty dashboard panel frame only on a perfectly flat #00ff00 chroma-key background.
Target canvas: 1920x1080. Target asset size: 456x386.
Content safe zones: empty 44px title band and 24px inner padding for live charts/tables.
Preserve the crop's corner cuts, border thickness, inner line, and cyan glow. Remove all text/data/chart/table marks.
No text, no numbers, no charts, no tables, no icons, no watermark.
Keep the asset centered with generous padding and no clipped glow.
```

Use same-kind asset sheets only for small decorations. Do not mix scenes, panel frames, icon bases, state icons, charts, and backgrounds in one sheet. The slicer should crop and package already-good regenerated assets; it should not rescue mixed, baked, or text-bearing screenshot crops.

For icon families, include a semantic slot map in the spec before generation or slicing. Distinguish KPI icons from bottom-navigation icons, header icons, weather icons, status icons, and right-panel metric icons even when they share the same glass badge style:

```json
{
  "name": "nav-energy-cycle",
  "category": "icons",
  "role": "bottom-navigation-icon",
  "semanticSlot": "nav-energy-cycle",
  "file": "styleKit/icons/nav-energy-cycle.png"
}
```

For selected/active overlays, record the anchor target so frontend placement can be verified in a browser screenshot:

```json
{
  "name": "nav-active",
  "category": "navigation",
  "role": "bottom-nav-active-overlay",
  "file": "styleKit/nav-active.png",
  "stateAnchor": {
    "target": "nav-icon-center",
    "x": 0.5,
    "y": 0.72
  }
}
```

For bottom navigation bases that visually split into segmented boxes, record the slot map from the reference crop and use it in Vue/CSS:

```json
{
  "navigationSlots": [
    {
      "name": "production",
      "leftPercent": 0.6,
      "widthPercent": 17.8,
      "iconCenterInNavBasePx": 60
    },
    {
      "name": "quality",
      "leftPercent": 18.6,
      "widthPercent": 16.4,
      "iconCenterInNavBasePx": 330
    }
  ]
}
```

Do not replace this with uniform `repeat(n, 1fr)` layout unless the measured reference slots are actually uniform.

## Layout Crop Spec

Before writing asset prompts for a full dashboard reference, create a layout crop spec and run `crop_reference_regions.py`. These crops keep model attention on one problem at a time and make local failures obvious.

```json
{
  "source": "img-bg-1.png",
  "baseWidth": 1536,
  "baseHeight": 1024,
  "regions": [
    {
      "name": "kpi-strip",
      "role": "top-kpi-cards",
      "box": [294, 80, 780, 96],
      "preserve": ["KPI card frame", "icon slots", "value/target/ring spacing"],
      "remove": ["numbers", "labels", "target text"]
    },
    {
      "name": "right-energy",
      "role": "right-energy-metrics",
      "box": [1235, 612, 288, 195],
      "preserve": ["energy icon colors", "four metric layout", "leaf green hue"],
      "remove": ["labels", "numbers", "units"]
    }
  ]
}
```

```bash
python .agents/skills/bigscreen-asset-slicer/scripts/crop_reference_regions.py --source img-bg-1.png --spec path/to/layout-regions.json --out path/to/reference-crops/layout
```

Use each crop as the nearest style lock for prompts and review. Do not rely on whole-page screenshots to judge small assets such as icons, KPI targets, panel corners, chart ticks, or bottom navigation slots.

For reusable frame systems, prefer a split-frame spec when the same visual style appears in several ratios. Generate or slice the non-scalable parts only, then let Vue/CSS draw the long straight connectors:

```text
Use the supplied panel-frame crop as a strict reconstruction guide.
Generate a transparent adaptive split-frame part sheet, not a complete frame.
Parts: top-left corner, top-right corner, bottom-left corner, bottom-right corner, title notch, glow node, short highlight spark.
Preserve clipped-corner geometry, cyan glow, thin line weight, and endpoint alignment.
Connector anchors: top connector y=4px, bottom connector y=height-4px, left connector x=2px, right connector x=width-2px, corner cut=36px.
Do not include long straight lines, title text, sample data, charts, icons, or center fill.
The frontend will draw the top/right/bottom/left connector lines with CSS gradients, so all part endpoints must align to the exact connector anchors. The panel fill must use a matching CSS clip-path/mask so diagonal corner gaps stay transparent.
CSS connectors must stop at the PNG part anchors. Do not redraw the diagonal corner cuts, local notches, bright nodes, bevel caps, or short highlight sparks with CSS when those features exist in the part sheet.
```
