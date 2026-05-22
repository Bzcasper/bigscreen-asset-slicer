# Frontend Integration Notes

## Repository Placement

Put generated files under the host application's normal source/static asset root. A common layout is:

```text
<app>/src/assets/bigscreen/<page-name>/
```

Keep the generated `manifest.json` next to the sliced image folders when it helps implementation or QA. The production component can import individual assets directly if that is simpler.

For a user-facing big-screen result, prefer a real route/page in the host application instead of a standalone `preview.html`. For Vue projects, a common page location is:

```text
<app>/src/views/bigscreen/<page-name>.vue
```

When the user asks for a direct big-screen route or route-based validation, register it using the host app's existing route pattern. Some projects use file routes, some use a local route module, and some load menus from a backend; follow the project already in front of you.

Use the existing app dev server when it is already running. Do not start an extra port just to serve a generated preview.

## Vue Page Pattern

Use raster assets for static visual materials and Vue components for live content:

```vue
<script setup lang="ts">
import bgUrl from '#/assets/bigscreen/overview/background/background.webp';
import panelFrameUrl from '#/assets/bigscreen/overview/panels/left-panel-frame.png';
</script>

<template>
  <div class="bigscreen-page">
    <img class="bigscreen-bg" :src="bgUrl" alt="" />
    <section class="data-panel data-panel-left">
      <img class="panel-frame" :src="panelFrameUrl" alt="" />
      <div class="panel-content">
        <!-- charts, tables, and live numbers stay here -->
      </div>
    </section>
  </div>
</template>

<style scoped>
.bigscreen-page {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background: #020712;
}

.bigscreen-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  pointer-events: none;
}

.data-panel {
  position: absolute;
}

.panel-frame {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.panel-content {
  position: relative;
  z-index: 1;
}
</style>
```

## Scaling Rule

For fixed-design dashboards, map coordinates from the manifest to percentages:

```ts
const left = `${(asset.x / manifest.baseWidth) * 100}%`;
const top = `${(asset.y / manifest.baseHeight) * 100}%`;
const width = `${(asset.width / manifest.baseWidth) * 100}%`;
const height = `${(asset.height / manifest.baseHeight) * 100}%`;
```

Use `aspect-ratio: 16 / 9` on the main stage when exact composition matters. For operational dashboards that must fill many screens, keep background images flexible and keep panel content responsive.

Respect manifest `contentInsets`, `safeZone`, and `safeZones` when placing DOM content. These fields exist to keep generated panel art from fighting titles, values, charts, tables, legends, nav labels, or callout tags.

## High-Fidelity Integration Gate

For 85%+ restoration tasks, implementation is allowed only after the asset coverage matrix has no high-impact gaps. The page may still render ECharts placeholders, but these non-chart pieces must not be generic substitutes:

- Header brand/logo, weather/status icon, and title chrome.
- KPI icon badges and KPI strip rhythm.
- Right-side quality, energy, safety, and status icons.
- Bottom navigation base, active halo, and per-slot icon anchors.
- Irregular panel/frame chrome and central scene controls/callout anchors.

If any of these are still `missing`, `css-approximation`, or `blocked-needs-image-edit-input`, keep them visible as explicit gaps in the audit instead of hiding them with reused icons or CSS-only artwork. After screenshot capture, generate `asset-audit/page-region-compare-<canvas>.png` and review local regions before claiming acceptance.

Route verification must use the same URL and viewport the user will inspect. Use the host app's actual dev URL, capture a cache-busted URL and the clean URL, and record the rendered asset sources and computed dimensions for critical icons, header/nav images, and frame layers.

Do not trust declared CSS dimensions alone. Project-wide CSS such as `img { max-width: 100% }`, grid columns, flex items, or wrapper boxes can shrink generated bitmap assets after import. When a generated icon, badge, active halo, or chrome image looks too small, inspect `getComputedStyle()` and the element bounding box in the browser. Fix the containing slot and add `max-width: none` for decorative imported images when the asset must render at its planned size.

## Implementation Rules

- Do not bake page titles, labels, timestamps, table data, chart values, or business copy into images.
- Keep important controls and dynamic content as real DOM.
- Match the reference style lock in CSS too: panel placement, title density, glow strength, icon sizing, and text rhythm should support the generated assets instead of drifting into a new theme.
- Do not replace high-impact generated assets with loosely similar DOM/CSS/icon-library approximations when the reference contains a distinct raster badge, logo, ornament, or active state.
- Keep text inside the safe zones planned during generation. If a safe zone is too small, regenerate or resize the asset rather than squeezing text over decorative details.
- Keep decorative images `pointer-events: none`.
- Use `alt=""` for purely decorative assets.
- Avoid nested card-like wrappers for big-screen layouts; use full-screen stages and absolute or grid-based placement.
- Use `Page` from `@vben/common-ui` only when the page lives inside the normal admin layout. For full-screen cockpit routes, a custom full-viewport root is acceptable if existing pages use that pattern.
