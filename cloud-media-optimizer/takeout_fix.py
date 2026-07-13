#!/usr/bin/env python3
"""Merge Google Takeout JSON sidecar metadata back into photo/video files.

Google Takeout ships capture time and GPS in per-file JSON sidecars; files that
were uploaded without EXIF (or edited in Google Photos) lack it embedded. This
tool writes DateTimeOriginal/CreateDate and GPS into files that are MISSING
them (existing embedded metadata is never overwritten), and sets every matched
file's mtime to the photo-taken time.

Run this on an extracted Takeout folder BEFORE optimize.py.

Requires: exiftool (brew install exiftool).
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

MEDIA_EXTS = {".heic", ".jpg", ".jpeg", ".png", ".gif", ".webp",
              ".mp4", ".mov", ".m4v", ".3gp", ".avi", ".mpg"}
VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".3gp", ".avi", ".mpg"}
SUPP = ".supplemental-metadata"
TRUNC_LEN = 46  # Takeout truncates long sidecar names around this length


def sidecar_target(json_path):
    """Derive the media filename a sidecar refers to, from the sidecar's name."""
    t = json_path.name[:-len(".json")]
    # strip ".supplemental-metadata", possibly itself truncated
    for i in range(len(SUPP), 1, -1):
        if t.endswith(SUPP[:i]):
            t = t[:-i]
            break
    # "IMG_001.jpg(1)" -> "IMG_001(1).jpg"
    m = re.match(r"^(.*)\.([A-Za-z0-9]+)\((\d+)\)$", t)
    if m:
        t = f"{m.group(1)}({m.group(3)}).{m.group(2)}"
    return t


def match_media(target, title, media_by_name):
    """Match a sidecar to media files in the same directory. Conservative:
    exact name, JSON title, explicit -edited variant, or truncated prefix."""
    hits = []
    for name in (target, title):
        if name and name in media_by_name:
            hits.append(media_by_name[name])
        if name:
            stem, ext = os.path.splitext(name)
            edited = f"{stem}-edited{ext}"
            if edited in media_by_name:
                hits.append(media_by_name[edited])
    if not hits and len(target) >= TRUNC_LEN:
        hits = [p for n, p in media_by_name.items() if n.startswith(target)]
    # dedupe, keep order
    seen, out = set(), []
    for p in hits:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def collect(root):
    """Walk the takeout tree; return {media_path: sidecar_data} and unmatched media."""
    matched, all_media = {}, set()
    for dirpath, _, filenames in os.walk(root):
        d = Path(dirpath)
        media_by_name = {f: d / f for f in filenames
                         if os.path.splitext(f)[1].lower() in MEDIA_EXTS}
        all_media.update(media_by_name.values())
        for f in filenames:
            if not f.endswith(".json"):
                continue
            jp = d / f
            try:
                data = json.loads(jp.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                continue
            if "photoTakenTime" not in data:   # album metadata etc., not a sidecar
                continue
            for media in match_media(sidecar_target(jp), data.get("title"),
                                     media_by_name):
                matched.setdefault(media, data)
    return matched, sorted(all_media - set(matched))


def wanted_tags(media, data, existing):
    """Return list of exiftool tag args to write for this file (only missing tags)."""
    args = []
    ts = int(data["photoTakenTime"]["timestamp"])
    dt = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)
    exif_dt = dt.strftime("%Y:%m:%d %H:%M:%S")
    is_video = media.suffix.lower() in VIDEO_EXTS

    has_date = existing.get("DateTimeOriginal") or existing.get("CreateDate")
    if not has_date:
        if is_video:
            args.append(f"-CreateDate={exif_dt}")
        else:
            args += [f"-DateTimeOriginal={exif_dt}", f"-CreateDate={exif_dt}"]

    geo = data.get("geoData") or {}
    lat, lon = geo.get("latitude", 0.0), geo.get("longitude", 0.0)
    if (lat or lon) and not existing.get("GPSLatitude") \
            and not existing.get("GPSCoordinates"):
        if is_video:
            args.append(f"-Keys:GPSCoordinates={lat} {lon}")
        else:
            args += [f"-GPSLatitude={abs(lat)}",
                     f"-GPSLatitudeRef={'N' if lat >= 0 else 'S'}",
                     f"-GPSLongitude={abs(lon)}",
                     f"-GPSLongitudeRef={'E' if lon >= 0 else 'W'}"]
    return args


def read_existing(files):
    """One exiftool invocation to read current date/GPS tags for all files."""
    if not files:
        return {}
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
        fh.write("\n".join(str(p) for p in files))
        listfile = fh.name
    try:
        r = subprocess.run(
            ["exiftool", "-j", "-fast2", "-q", "-DateTimeOriginal", "-CreateDate",
             "-GPSLatitude", "-GPSCoordinates", "-@", listfile],
            capture_output=True, text=True)
        entries = json.loads(r.stdout) if r.stdout.strip() else []
    finally:
        os.unlink(listfile)
    return {os.path.abspath(e["SourceFile"]): e for e in entries}


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("takeout_dir", type=Path)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    root = args.takeout_dir.resolve()
    if not root.is_dir():
        sys.exit(f"ERROR: {root} is not a directory")

    matched, unmatched = collect(root)
    print(f"Matched {len(matched)} media files to sidecars; "
          f"{len(unmatched)} media files have no sidecar")

    existing = read_existing(sorted(matched))
    blocks, writes = [], 0
    for media, data in sorted(matched.items()):
        tags = wanted_tags(media, data, existing.get(str(media), {}))
        if tags:
            blocks.append("\n".join(tags + [str(media)]))
            writes += 1

    if args.dry_run:
        print(f"Would write missing metadata into {writes} files "
              f"(rest already have embedded dates/GPS).")
        for b in blocks[:20]:
            print("  " + b.replace("\n", " "))
        print("Dry run — nothing written.")
        return

    if blocks:
        argfile_text = ("\n-execute\n".join(blocks)
                        + "\n-common_args\n-overwrite_original\n-q\n-api\nQuickTimeUTC=1\n")
        with tempfile.NamedTemporaryFile("w", suffix=".args", delete=False) as fh:
            fh.write(argfile_text)
            argfile = fh.name
        try:
            r = subprocess.run(["exiftool", "-@", argfile],
                               capture_output=True, text=True)
            if r.stderr.strip():
                print(r.stderr.strip(), file=sys.stderr)
        finally:
            os.unlink(argfile)
        print(f"Wrote missing metadata into {writes} files")
    else:
        print("All matched files already have embedded metadata")

    # mtime -> photo taken time, for every matched file
    for media, data in matched.items():
        ts = int(data["photoTakenTime"]["timestamp"])
        try:
            os.utime(media, (ts, ts))
        except OSError:
            pass
    print(f"Set mtime on {len(matched)} files")

    if unmatched:
        print(f"\nUNMATCHED ({len(unmatched)}) — check these manually:")
        for m in unmatched[:50]:
            print(f"  {m.relative_to(root)}")
        if len(unmatched) > 50:
            print(f"  ... and {len(unmatched) - 50} more")


if __name__ == "__main__":
    main()
