#!/usr/bin/env python3
"""SAKO Cinema: set the hero title to this Jellyfin server's name.

CSS cannot read the server name, so this writes it into Custom CSS once:
  :root { --sako-hero-title: "<server name>"; }
inside a marked block that a later run replaces (never duplicates).
Run it again after renaming the server. Python stdlib only.

--dry-run needs no key: it reads the public server name and Custom CSS.
--apply prompts for an admin API key (not saved), backs up the branding
settings first and reads the result back. --restore puts a backup back.
"""
import argparse, getpass, json, pathlib, re, sys, urllib.request, urllib.error
from datetime import datetime, timezone

BEGIN = "/* sako-hero-title: managed by scripts/set-hero-title.py */"
END = "/* sako-hero-title: end */"
BLOCK_RE = re.compile(r"\n*" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", re.S)

def request(url, token=None, method="GET", data=None):
    headers = {"User-Agent": "SAKO-Cinema-Hero-Title/1.0"}
    if token:
        # Jellyfin 12 disables deprecated token-only headers by default.
        headers["Authorization"] = (
            'MediaBrowser Client="SAKO Cinema Installer", '
            'Device="CLI", DeviceId="sako-cinema-hero-title-cli", '
            'Version="1.0", Token="' + token + '"'
        )
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, headers=headers, data=data, method=method)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8")

def css_string(text):
    # one line, quotes and backslashes escaped, so the name can't break out of the CSS string
    text = re.sub(r"[\x00-\x1f\x7f]", " ", text).strip()
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'

def with_title(css, title):
    block = BEGIN + "\n:root { --sako-hero-title: " + css_string(title) + "; }\n" + END
    return BLOCK_RE.sub("\n", css or "").rstrip() + "\n" + block + "\n"

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--url", default="http://127.0.0.1:8096", help="Jellyfin base URL reachable from where this script runs")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true", help="Show the change; no key needed, nothing written")
    g.add_argument("--apply", action="store_true", help="Back up branding settings, then write the title")
    g.add_argument("--restore", metavar="BACKUP_JSON", help="Write a backup made by --apply back to Jellyfin")
    p.add_argument("--title", help="Use this text instead of the server name")
    p.add_argument("--backup-dir", default="./sako-cinema-branding-backup")
    args = p.parse_args()
    base = args.url.rstrip("/")
    print("Jellyfin:", base)

    if args.restore:
        saved = json.loads(pathlib.Path(args.restore).read_text(encoding="utf-8"))
        key = getpass.getpass("Jellyfin admin API key (input hidden): ").strip()
        if not key: p.error("API key required")
        if input("Type RESTORE to write this backup back to Jellyfin: ").strip() != "RESTORE":
            sys.exit("Cancelled without changes.")
        request(base + "/System/Configuration/branding", key, "POST", saved)
        print("Restored branding settings from", args.restore)
        return

    try:
        title = args.title or json.loads(request(base + "/System/Info/Public")).get("ServerName", "")
        current_css = request(base + "/Branding/Css")
    except (urllib.error.URLError, ValueError) as e:
        sys.exit("Cannot reach Jellyfin at " + base + ": " + str(e))
    if not title.strip(): sys.exit("Server name is empty; pass --title instead. No changes made.")
    if "SAKO-Cinema-Theme" not in current_css:
        print("Note: Custom CSS does not import SAKO Cinema yet; the title only shows once it does.")
    new_css = with_title(current_css, title)
    print("Hero title:", css_string(title))
    if new_css.strip() == current_css.strip():
        print("Custom CSS already has this title. Nothing to do."); return
    print("\nCustom CSS after the change:\n" + new_css)
    if args.dry_run:
        print("DRY RUN: nothing written. Run --apply to write it."); return

    key = getpass.getpass("Jellyfin admin API key (input hidden): ").strip()
    if not key: p.error("API key required")
    try:
        branding = json.loads(request(base + "/System/Configuration/branding", key))
    except urllib.error.HTTPError as e:
        sys.exit("Cannot read branding settings (HTTP " + str(e.code) + "). The key needs admin rights. No changes made.")
    if input("Type APPLY to back up and update Custom CSS: ").strip() != "APPLY":
        sys.exit("Cancelled without changes.")
    backup = pathlib.Path(args.backup_dir).expanduser().resolve()
    backup.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_file = backup / ("branding-" + stamp + ".json")
    n = 1
    while backup_file.exists():  # never overwrite an earlier backup
        backup_file = backup / ("branding-" + stamp + "-" + str(n) + ".json"); n += 1
    with open(backup_file, "x", encoding="utf-8") as f:
        f.write(json.dumps(branding, indent=2))
    print("Backup:", backup_file)
    branding["CustomCss"] = with_title(branding.get("CustomCss") or "", title)
    request(base + "/System/Configuration/branding", key, "POST", branding)
    if css_string(title) not in request(base + "/Branding/Css"):
        sys.exit("Written, but the read-back does not show the title. Restore with: --restore " + str(backup_file))
    print("Done. Reload Jellyfin with Ctrl+Shift+R. Undo with: --restore " + str(backup_file))

if __name__ == "__main__": main()
