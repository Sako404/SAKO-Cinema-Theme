# Artwork and setup

The SVG artwork files in `artwork/libraries/` are **original static cover designs**, not dynamically generated posters. Use the **Primary** image (and optionally Backdrop) for a Jellyfin library in its image editor. This is independent of the Custom CSS theme and can persist through theme changes.

## Available images

| Jellyfin library | File |
| --- | --- |
| Movies | `movies.svg` |
| Movies on WD | `movies-on-wd.svg` |
| TV Shows | `tv-shows.svg` |
| Music | `music.svg` |
| Live TV | `live-tv.svg` |
| Collections | `collections.svg` |
| Playlists | `playlists.svg` |
| Home Videos & Photos | `family-photos.svg` |
| Adult Movies | `adult-movies.svg` |

**Compatibility note:** Some Jellyfin image upload paths/TV apps may not accept SVG files or render them consistently. Convert to PNG/JPEG first (1200 × 675 recommended) if necessary. SVG source remains editable in this repo.

The family hero banner is `artwork/family-cinema-banner.svg` and is referenced directly by `theme.css`. It is purely decorative, is not a clickable Jellyfin feature, and does not disclose private family photographs.

**Security:** The family user should have library restrictions configured on the server. Theme artwork is not an access-control boundary. The public repo artwork is fictional and non-identifying.

**Rollback:** Restore your prior ElegantFin `@import` and remove the SAKO import. Media and user permissions are unaffected.
