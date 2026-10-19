# Changelog

## 1.0.0-rc2 — backdrops and heading consistency
- Fixed: item backdrops on detail pages were hidden by an opaque body background; body is transparent again and backdrops show through a navy scrim
- Fixed: "My Media" and "Continue Watching" headings now match the size and weight of the other home sections (left alignment unchanged)
- ElegantFin pinned to release v26.09.05 (commit 5efc110) instead of `main`; byte-identical to the build tested with rc1

## 1.0.0-rc1 — consolidated cinema theme
- Replaced accumulated patch layers with a single maintainable stylesheet
- Preserved user-confirmed home heading alignment and banner 10:3 proportions
- Pinned family hero image to an existing Git commit
- Improved top navigation, media cards, details, focus, responsive behaviour
- Retained all original Jellyfin library artwork: CSS does not override cover URLs
- Candidate release: actual browser verification pending

## 0.6.x
- New cinematic JPEG banner and nine static library covers
- Backed-up server-side artwork installation script
- Basic cinema polish and fixes for legacy image background overrides

## 0.3.x
- Home banner, responsive refinements, section heading alignment
