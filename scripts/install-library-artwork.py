#!/usr/bin/env python3
"""SAKO Cinema: safely assign permanent library cover artwork via Jellyfin API.

Run on the machine that can access Jellyfin. Python stdlib only.
Always run --dry-run first; --apply requires explicit confirmation.
The key is prompted locally (not saved in shell history or source).
"""
import argparse, base64, getpass, json, os, pathlib, re, sys, urllib.request, urllib.error
from datetime import datetime, timezone

REPO = "https://raw.githubusercontent.com/Sako404/SAKO-Cinema-Theme/main/artwork/libraries"
MAP = {
    "movies": "movies.jpg",
    "movies on wd": "movies-on-wd.jpg",
    "tv shows": "tv-shows.jpg",
    "shows": "tv-shows.jpg",
    "music": "music.jpg",
    "collections": "collections.jpg",
    "playlists": "playlists.jpg",
    "home videos and photos": "home-videos-and-photos.jpg",
    "live tv": "live-tv.jpg",
    "porno": "adult-movies.jpg",
    "adult movies": "adult-movies.jpg",
}
def norm(s):
    return re.sub(r"\s+", " ", s.casefold().strip())
def request(url, token=None, method="GET", data=None, content_type=None):
    headers={"User-Agent":"SAKO-Cinema-Library-Artwork/0.8"}
    if token:
        # Jellyfin 12 disables deprecated token-only headers by default.
        # Current supported MediaBrowser authorization scheme:
        headers["Authorization"]=(
            'MediaBrowser Client="SAKO Cinema Installer", '
            'Device="TrueNAS SSH", DeviceId="sako-cinema-artwork-cli", '
            'Version="0.7.1", Token="'+token+'"'
        )
    if content_type: headers["Content-Type"]=content_type
    req=urllib.request.Request(url,headers=headers,data=data,method=method)
    with urllib.request.urlopen(req,timeout=25) as r:
        return r.read(),r.headers.get("Content-Type","")
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--url",default="http://127.0.0.1:30013",help="Jellyfin base URL accessible from where this script runs")
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--diagnose",action="store_true",help="Check public and authenticated endpoints without changing anything")
    g.add_argument("--inspect-special",action="store_true",help="Inspect Live TV and Playlists views read-only; no changes")
    g.add_argument("--dry-run",action="store_true")
    g.add_argument("--apply",action="store_true")
    p.add_argument("--backup-dir",default="./sako-cinema-library-backup")
    p.add_argument("--only",help="Process only one exact library name, recommended for initial apply")
    p.add_argument("--exclude",action="append",default=[],help="Skip a library by exact name (repeatable)")
    args=p.parse_args()
    base=args.url.rstrip("/")
    print("Jellyfin:",base)
    key=getpass.getpass("Temporary Jellyfin API token (input hidden): ").strip()
    if not key: p.error("API token required")
    if args.inspect_special:
        try:
            raw,_=request(base+"/Users",key)
            users=json.loads(raw)
            if not isinstance(users,list):
                raise ValueError("Unexpected /Users response")
        except Exception as e:
            sys.exit("Cannot enumerate views: "+str(e))
        found={}
        for user in users:
            uid=user.get("Id")
            if not uid: continue
            try:
                raw,_=request(base+"/Users/"+str(uid)+"/Views",key)
                views=json.loads(raw).get("Items",[])
            except Exception as e:
                print("View query failed (user identifier hidden):",type(e).__name__)
                continue
            for v in views:
                name=str(v.get("Name",""))
                collection=str(v.get("CollectionType",""))
                kind=str(v.get("Type",""))
                if any(word in norm(name+" "+collection+" "+kind) for word in ("playlist","live tv","livetv")):
                    vid=v.get("Id")
                    found[(name,str(vid))]=(collection,kind)
        if not found:
            print("No matching special views found through /Users/{id}/Views.")
            print("These may be web-client navigation entries without image-backed server items.")
        else:
            print("Potential Live TV / Playlists views (deduplicated):")
            for (name,vid),(collection,kind) in sorted(found.items()):
                print("  Name:",name,"| ItemId:",vid,"| CollectionType:",collection,"| Type:",kind)
        print("READ ONLY. No changes made.")
        return
    if args.diagnose:
        for label, path, tok in [("public", "/System/Info/Public", None), ("authentication", "/System/Info", key), ("libraries", "/Library/VirtualFolders", key)]:
            try:
                request(base+path, tok)
                print(label + ": HTTP 200 (OK)")
            except urllib.error.HTTPError as err:
                print(label + ": HTTP " + str(err.code))
            except Exception as err:
                print(label + ": " + type(err).__name__)
        print("Diagnosis complete. No changes made. Never share the API key.")
        return
    try:
        raw,_=request(base+"/Library/VirtualFolders",key)
        folders=json.loads(raw)
    except Exception as e:
        sys.exit(f"Could not list Jellyfin libraries: {e}. Check URL, API key and permissions.")
    matches=[]
    for f in folders:
        name=f.get("Name","")
        itemid=f.get("ItemId")
        file=MAP.get(norm(name))
        if not file or not itemid:
            print("SKIP (not mapped or missing ItemId):",name)
            continue
        matches.append((name,itemid,file))
    if args.only:
        matches=[m for m in matches if norm(m[0])==norm(args.only)]
    excluded={norm(name) for name in args.exclude}
    matches=[m for m in matches if norm(m[0]) not in excluded]
    if not matches: sys.exit("No mapped libraries found. No changes made.")
    print("\nMatched libraries:")
    for name,itemid,file in matches: print("  ",name,"->",file,"(ItemId:",itemid,")")
    if args.dry_run:
        print("\nDRY RUN: No images modified. Run --apply after reviewing the mapping.")
        return
    confirm=input("\nType APPLY to back up and replace these Primary images: ").strip()
    if confirm!="APPLY":sys.exit("Cancelled without changes.")
    backup=pathlib.Path(args.backup_dir).expanduser().resolve()/datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup.mkdir(parents=True,exist_ok=False)
    manifest=[]
    for name,itemid,file in matches:
        safe=re.sub(r"[^a-zA-Z0-9_.-]","_",name)[:50]+"-"+str(itemid)
        row={"name":name,"itemId":itemid,"newFile":file,"oldImage":None,"status":"pending"}
        manifest.append(row)
        image_url=base+"/Items/"+str(itemid)+"/Images/Primary"
        try:
            old,ctype=request(image_url,key)
            ext=".png" if "png" in ctype else ".jpg"
            target=backup/(safe+ext)
            target.write_bytes(old)
            row["oldImage"]=target.name
        except urllib.error.HTTPError as e:
            if e.code!=404:
                row["status"]="backup-failed";print("FAILED to back up",name,e);continue
            row["oldImage"]="none"
        except Exception as e:
            row["status"]="backup-failed";print("FAILED to back up",name,e);continue
        try:
            image,content_type=request(REPO+"/"+file)
            if len(image)<1000 or not image.startswith(bytes.fromhex("ffd8")): raise ValueError("Not a valid JPG file")
            request(image_url,key,method="POST",data=base64.b64encode(image),content_type="image/jpeg")
            # Confirm that Jellyfin serves a Primary image after the update.
            confirmed,_=request(image_url,key)
            if not confirmed: raise ValueError("Jellyfin returned an empty Primary image after upload")
            row["status"]="uploaded-and-readable"
            print("UPDATED:",name)
        except Exception as e:
            row["status"]="upload-failed";print("FAILED to update",name,e)
        (backup/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print("\nBackups and manifest:",backup)
    print("No library permissions, accounts, paths or media files were changed.")
    if any(row["status"]!="uploaded-and-readable" for row in manifest):sys.exit("Some image updates failed; see manifest.")
if __name__=="__main__":main()
