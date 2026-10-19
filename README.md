# SAKO Cinema Theme 🎬

Public, free family-oriented theme for **Jellyfin Web**, built on ElegantFin. Navy, blue, violet, magenta and cozy home cinema artwork. No gold.

![SAKO Cinema hero](artwork/family-cinema-hero.jpg)

## Install (single CSS import)

In **Jellyfin Dashboard → Branding → Custom CSS**, replace existing custom CSS with:

```css
@import url("https://cdn.jsdelivr.net/gh/Sako404/SAKO-Cinema-Theme/theme.css");
```

Save, then reload Jellyfin Web with Ctrl+Shift+R. This stylesheet already imports ElegantFin. Do not import ElegantFin a second time or paste the earlier v0.5 override blocks underneath.

This address always follows the latest published theme, so updates arrive without editing Jellyfin. Two things to know:

- jsDelivr caches the file (CDN up to 12 h, browsers up to 7 days). After an update, reload with Ctrl+Shift+R. Maintainers can clear the CDN copy at `https://purge.jsdelivr.net/gh/Sako404/SAKO-Cinema-Theme/theme.css`.
- To freeze a specific version, pin a commit instead:

```css
@import url("https://cdn.jsdelivr.net/gh/Sako404/SAKO-Cinema-Theme@aee12516ab43d1b51dd6382d64324e863c1e2e54/theme.css");
```

**Rollback:** previous release candidate (1.0.0-rc1):

```css
@import url("https://cdn.jsdelivr.net/gh/Sako404/SAKO-Cinema-Theme@0d6745cd7034b49b2213f4a1b8af988636fc8651/theme.css");
```

or the earlier working v0.6.1 version:

```css
@import url("https://cdn.jsdelivr.net/gh/Sako404/SAKO-Cinema-Theme@2bb4583dc36a057a9e360f9da8cc82bbd614e620/theme.css");
```

## What is included

- Clean CSS with one set of rules for home hero, card visuals, progress and headings
- Layout refinements for Jellyfin Web home, browse and detail pages
- Focus visibility, mobile adjustments and reduced-motion preference
- New cinematic family hero (JPG) and nine permanent cover images
- [Library artwork](artwork/libraries/) and [artwork installation script](scripts/install-library-artwork.py)

Original media-library covers should be assigned in Jellyfin as **Primary** images rather than replaced with CSS. They then persist through style updates and may be displayed by native TV clients.

## Scope and limitations

The original mockup is a *visual design reference*, not a pixel-perfect Jellyfin implementation. This is **CSS layered on existing Jellyfin Web**, not a replacement web app. It preserves actual navigation and functionality; a different functional sidebar, new recommendations engine, or custom menu hierarchy would require client development rather than CSS.

Native Jellyfin apps on Fire TV/Google TV do not apply web CSS. Artwork is stored on the server and can carry across where the native clients support it.

Jellyfin permissions must control access to private/adult libraries. CSS is not a security boundary. Never put API keys or private family photos in public repository content.

**Release status:** v1.0.0-rc2. Checked in desktop Chrome on the owner's Jellyfin (home, library browse, item details) and on a 400px-wide mobile viewport; not yet checked on the login page, the video player, or other browsers. ElegantFin is pinned to release v26.09.05 (commit `5efc110`), so the import is reproducible.

## Maintainers

Original CSS/docs/artwork: MIT (see LICENSE). ElegantFin is a separate dependency under its upstream licence. Contributions and screenshots without sensitive information welcome.
