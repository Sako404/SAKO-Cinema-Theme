# SAKO Cinema — Cinematic Artwork Pack v0.6

Contains an original hero JPEG (2290 x 687) and 9 library covers (1672 x 941), with all original generated artwork kept separate from other theme files.

## Deploy on GitHub

1. Upload `artwork/family-cinema-hero.jpg` to `Sako404/SAKO-Cinema-Theme/artwork/family-cinema-hero.jpg`.
2. Upload all JPG files from `artwork/libraries/` to `Sako404/SAKO-Cinema-Theme/artwork/libraries/`.
3. Upload `theme-v0.6.css` to repository root (or merge it into `theme.css`).
4. In Jellyfin > Dashboard > Branding > Custom CSS, use `@import url("https://cdn.jsdelivr.net/gh/Sako404/SAKO-Cinema-Theme@main/theme-v0.6.css");`
5. Save and force refresh. For production, pin to a tested release tag instead of `@main`.

## Permanent library artwork

In Jellyfin's admin library manager, open the library image editor and upload the matching JPG as the library's primary image. This assignment survives CSS theme switches and can show on Fire TV.

- movies.jpg — Movies
- movies-on-wd.jpg — Movies on WD
- tv-shows.jpg — Shows
- music.jpg — Music
- collections.jpg — Collections
- playlists.jpg — Playlists
- home-videos-and-photos.jpg — Home Videos and Photos
- live-tv.jpg — Live TV
- adult-movies.jpg — adults-only library (keep access controlled by Jellyfin account permissions)

The CSS banner is presentation only. The Jellyfin permissions protect private libraries, not CSS.

Important: this package is ready to upload, but until files are uploaded to GitHub the v0.6 import will not work. The earlier v0.5.1 remains usable.
