# Install library artwork using fish + SSH

The installer runs **on TrueNAS**, not inside fish. Run the commands below in your local **fish** terminal. The `ssh truenas` alias must already work.

The temporary Jellyfin API key is entered **interactively** after the connection opens; it is never placed in command history, this repository, or the chat.

## Step 1: Download installer to TrueNAS

```fish
ssh truenas 'mkdir -p ~/sako-cinema && curl -fLsS https://raw.githubusercontent.com/Sako404/SAKO-Cinema-Theme/main/scripts/install-library-artwork.py -o ~/sako-cinema/install-library-artwork.py'
```

If your TrueNAS has no `curl`, replace it with `wget -O ~/sako-cinema/install-library-artwork.py URL`.

## Step 2: Dry-run (no writes)

```fish
ssh -t truenas 'python3 ~/sako-cinema/install-library-artwork.py --url http://127.0.0.1:30013 --dry-run'
```

If Jellyfin isn't reachable on localhost from TrueNAS, replace `127.0.0.1` with `192.168.0.175`.

Check the printed matches. Especially check that `Porno` is mapped to `adult-movies.jpg`; it changes **only** library artwork, never user permissions.

## Step 3: Apply with backup (after reviewing dry-run)

```fish
ssh -t truenas 'python3 ~/sako-cinema/install-library-artwork.py --url http://127.0.0.1:30013 --apply --backup-dir ~/sako-cinema/backups'
```

It prompts again for the temporary token and then asks you to type `APPLY`. The script saves original primary images and a manifest to the selected backup directory. Make sure the destination is writable and persistent (on TrueNAS consider a mounted dataset path for long-term retention instead of your home folder).

The source JPG files are public under `artwork/libraries`; the API key stays local.

## If it fails

- Do **not** proceed from a failed dry-run to apply.
- Record the error text **without the API token**.
- Don't use `sudo` unless needed; it shouldn't require root.
- On TrueNAS systems where `python3` or network access is unavailable from the SSH shell, use another device on the LAN or make the script available there.
- After success, revoke/delete the temporary API token via Jellyfin Dashboard.

## Scope

This utility changes library Primary images only. It does **not** modify user accounts, content access permissions, movies, metadata, or browser CSS. The main `theme.css` controls the web UI.
