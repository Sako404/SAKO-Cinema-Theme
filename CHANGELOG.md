# Changelog

## Unreleased
- New `scripts/set-hero-title.py`: writes the Jellyfin server name (or `--title`) into Custom CSS as `--sako-hero-title`, in a marked block that re-runs replace; `--dry-run` without a key, backup before `--apply`, `--restore` to undo

## 1.2.0-rc.1 — your own hero title
- Hero image is now text-free (`artwork/family-cinema-hero-clean.jpg`); kicker, title, subtitle, tagline and accent bar are drawn by CSS and scale with the hero
- New variables `--sako-hero-title`, `--sako-hero-kicker`, `--sako-hero-subtitle`, `--sako-hero-tagline`; defaults reproduce the 1.1.0 look, `""` hides a line (closes #8)
- Phones show the title only, centred on the hero
- Hero size and offset now come from `--sako-hero-w` / `--sako-hero-top`, so the image and its text always move together (theme-only, layout and sidebar modes)

## 1.1.0 — release
- Same CSS as 1.1.0-rc.2: theme with detail backdrops, hover poster fix, details and library polish, aligned headings; optional `layout.css` with sidebar, full-width hero, tile grid and one card family across home rows
- Install from release tags only (README); jsDelivr branch URLs can serve stale commits
- Known limitation: the login page uses base styling only

## 1.1.0-rc.2 — one card family on the home page
- layout.css: Continue Watching, Next Up and every Recently Added row now share the panel card (artwork, left-aligned text, violet edge, lift and glow on hover); rows stay horizontal scrollers and keep their native poster shapes
- layout.css: top-right header icons get a dark backdrop in sidebar mode so they stay legible over scrolled content

## 1.1.0-rc1 — optional layout module
- New `layout.css` (opt-in second import): sidebar from Jellyfin's library nav, full-width home hero with overlapping library tiles, My Media tile grid, panel Continue Watching cards, full-width library grids next to the sidebar
- Sidebar only from 1100px, never in the TV layout or video player, and only where `:has()` is supported
- theme.css fix: all home headings now align with Jellyfin's 3.3% section indent at every width (previously correct only at 2560px)

## 1.0.0-rc3 — details and library polish
- Fixed: posters disappeared on mouse hover in every card grid (Jellyfin 12 overlay link inherited the opaque card background)
- Details: gradient Play/Resume, glass secondary buttons, lavender tagline, readable overview, violet external-link chips, tinted info panels, section headings matching home, ring on cast photos
- Library: gradient Play All group, violet item-count chip, gradient unplayed-count badges, card outline with hover glow

## 1.0.0-rc2 — backdrops and heading consistency
- Fixed: item backdrops on detail pages were hidden by an opaque body background; body is transparent again and backdrops show through a navy scrim
- Fixed: "My Media" and "Continue Watching" headings now match the size and weight of the other home sections (left alignment unchanged)
- ElegantFin pinned to release v26.09.05 (commit 5efc110) instead of `main`; byte-identical to the build tested with rc1
- README: recommended install is now the unversioned jsDelivr address; the pinned commit stays documented for a frozen install

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
