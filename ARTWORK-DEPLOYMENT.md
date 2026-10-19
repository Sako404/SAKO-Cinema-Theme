# Library artwork setup

The repository ships one hero banner and nine library covers:

- `artwork/family-cinema-hero.jpg`: home banner, 2290 × 687 (10:3). `theme.css` loads it, so you don't need to install it.
- `artwork/libraries/*.jpg`: library covers, 1672 × 941 (16:9). The SVG files are editable source versions.

Assign each cover as the library's **Primary** image in Jellyfin. Unlike CSS, a Primary image is stored on the server. It survives theme updates and appears in the native TV apps.

| Cover file | Typical library |
|---|---|
| `movies.jpg` | Movies |
| `tv-shows.jpg` | TV Shows |
| `music.jpg` | Music |
| `collections.jpg` | Collections |
| `home-videos-and-photos.jpg` | Home Videos & Photos |
| `live-tv.jpg` | Live TV |
| `playlists.jpg` | Playlists |
| `movies-on-wd.jpg` | A second movie drive or archive |
| `adult-movies.jpg` | Adults-only library. Access must be restricted through Jellyfin user permissions. |

## Option A: by hand

Dashboard → Libraries → open a library → **Images** → upload the matching JPG as *Primary*.

## Option B: installer script

`scripts/install-library-artwork.py` uses the Jellyfin API and only the Python standard library. It asks for an API key interactively and never stores it. It maps libraries to covers by name, backs up the current images and changes nothing until you confirm.

```sh
python3 install-library-artwork.py --url http://YOUR-SERVER:8096 --dry-run
python3 install-library-artwork.py --url http://YOUR-SERVER:8096 --apply --backup-dir ./backups
```

Other flags:
- `--diagnose`: checks connectivity and auth only.
- `--only "Movies"`: processes one library.
- `--exclude NAME`: skips a library.

For running it on a TrueNAS host over SSH from the fish shell, see [scripts/FISH-SSH-SETUP.md](scripts/FISH-SSH-SETUP.md).

Create a temporary API key for the run (Dashboard → API Keys) and revoke it afterwards.
