# SAKO Cinema Theme

A family-first, navy / electric blue / violet / subtle magenta theme for **Jellyfin Web**, inspired by a cinematic, comfortable home entertainment experience. Built as an optional styling layer on top of [ElegantFin](https://github.com/lscambo13/ElegantFin).

> **Status: v0.1.0 preview.** CSS selectors have not yet been verified against the owner's running Jellyfin instance or all ElegantFin versions. Test before everyday use.

## Install

In Jellyfin Dashboard → General → Custom CSS, replace your old ElegantFin import (do **not** stack both) with:

```css
@import url("https://cdn.jsdelivr.net/gh/Sako404/SAKO-Cinema-Theme@main/theme.css");
```

For production, use a pinned release once one has been published (e.g. `@v1.0.0`) rather than `@main`. No release tag exists yet.

**To roll back:** remove the SAKO import and restore your previous ElegantFin import:

```css
@import url("https://cdn.jsdelivr.net/gh/lscambo13/ElegantFin@main/Theme/ElegantFin-jellyfin-theme-build-latest-minified.css");
```

## What it changes

- Dark navy UI, blue-to-violet accents and subtle magenta
- Navigation, focus indication, cards, progress bars, buttons, scrollbar
- Restrained desktop hover motion and reduced-motion support
- Responsive refinements for small screens

## What it does not change

- **Android TV / Amazon Fire TV native Jellyfin app:** Custom CSS normally applies to Jellyfin's web client, not its native Android TV interface. Static artwork assigned to libraries can appear in supported native clients.
- Library access and parental controls: keep permissions enforced in Jellyfin user settings. CSS must never be used to hide adult content as an access control.
- Your server files, media metadata or Jellyfin login flow.

## Artwork

Our preferred visual direction is a family watching a movie together: warm human atmosphere with restrained electric blue/violet highlights; **no gold**. The original concept image is a *mockup*, not a working screenshot of Jellyfin. Static library images should be managed in Jellyfin as **library primary/backdrop images**, not swapped via CSS. That makes them independent from theme updates. An artwork pack will be added separately after asset review; it is **not included** in this preview.

Planned library artwork: Movies, TV Shows, Music, Collections, Playlists, Home Videos & Photos, Live TV, plus optional discreet Adult Movies art (access controlled in Jellyfin). Do not include private family photos in a public repository.

## Dependencies / licensing

This repository's original CSS and documentation are MIT licensed. ElegantFin is fetched independently at runtime under its own upstream license; it is not redistributed here. Movie posters or other third-party imagery are not included. Upstream `@main` can change without notice; a future release should pin a tested ElegantFin commit.

## Maintenance

Please report the Jellyfin server version, browser/client, reproduction steps and a screenshot with sensitive information removed when opening an issue.

Created for a real family media server and shared for anyone to adapt.
