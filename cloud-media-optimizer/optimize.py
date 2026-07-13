#!/usr/bin/env python3
"""Compress photos/videos to Google Photos "Storage saver" quality.

Photos: capped at 16 MP, recompressed (HEIC->HEIC, JPG->JPG q80, PNG->JPG q85) via sips.
Videos: capped at 1080p, HEVC via VideoToolbox hardware encoder, metadata preserved.

Default mode mirrors INPUT_DIR into OUTPUT_DIR, originals untouched.
--replace mode (for a OneDrive synced folder) swaps optimized files in place,
moving each original into --backup-dir first. Nothing is ever deleted outright.

Stdlib only. Requires: ffmpeg, ffprobe, sips (macOS built-in).
"""

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PHOTO_EXTS = {".heic", ".jpg", ".jpeg", ".png"}
VIDEO_EXTS = {".mp4", ".mov", ".m4v"}
MAX_PIXELS = 16_000_000          # Google "Storage saver" photo cap
MAX_VIDEO_DIM = 1920             # 1080p cap (longest side)
EFFICIENT_VIDEO_BPS = 6_000_000  # already-HEVC 1080p under this: not worth re-encoding
JPEG_QUALITY = 80
PNG_TO_JPEG_QUALITY = 85
VIDEOTOOLBOX_QUALITY = 60


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


class Stats:
    def __init__(self):
        self.lock = threading.Lock()
        self.counts = {}          # action -> count
        self.bytes_in = 0
        self.bytes_out = 0
        self.failures = []        # (relpath, error)

    def record(self, action, size_in, size_out):
        with self.lock:
            self.counts[action] = self.counts.get(action, 0) + 1
            self.bytes_in += size_in
            self.bytes_out += size_out

    def fail(self, relpath, err):
        with self.lock:
            self.failures.append((str(relpath), err))


# ---------------------------------------------------------------- photos

def photo_dimensions(path):
    r = run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)])
    if r.returncode != 0:
        raise RuntimeError(f"sips probe failed: {r.stderr.strip()}")
    w = h = None
    for line in r.stdout.splitlines():
        line = line.strip()
        if line.startswith("pixelWidth:"):
            w = int(line.split(":")[1])
        elif line.startswith("pixelHeight:"):
            h = int(line.split(":")[1])
    if not w or not h:
        raise RuntimeError("could not read image dimensions")
    return w, h


def optimize_photo(src, dst):
    """Write optimized version of src to dst. Returns output path actually written
    (extension may change for PNG->JPEG)."""
    ext = src.suffix.lower()
    w, h = photo_dimensions(src)

    if ext == ".png":
        out_fmt, quality = "jpeg", PNG_TO_JPEG_QUALITY
        dst = dst.with_suffix(".jpg")
    elif ext == ".heic":
        out_fmt, quality = "heic", JPEG_QUALITY
    else:
        out_fmt, quality = "jpeg", JPEG_QUALITY

    cmd = ["sips", "-s", "format", out_fmt, "-s", "formatOptions", str(quality)]
    if w * h > MAX_PIXELS:
        target = int(max(w, h) * math.sqrt(MAX_PIXELS / (w * h)))
        cmd += ["-Z", str(target)]
    cmd += [str(src), "--out", str(dst)]

    r = run(cmd)
    if r.returncode != 0 or not dst.exists() or dst.stat().st_size == 0:
        raise RuntimeError(f"sips failed: {r.stderr.strip() or r.stdout.strip()}")
    return dst


# ---------------------------------------------------------------- videos

def probe_video(path):
    r = run(["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_format", "-show_streams", str(path)])
    if r.returncode != 0:
        raise RuntimeError("ffprobe failed")
    info = json.loads(r.stdout)
    vstream = next((s for s in info.get("streams", [])
                    if s.get("codec_type") == "video"), None)
    if vstream is None:
        raise RuntimeError("no video stream")
    bitrate = int(vstream.get("bit_rate")
                  or info.get("format", {}).get("bit_rate") or 0)
    return {
        "codec": vstream.get("codec_name", ""),
        "width": int(vstream.get("width", 0)),
        "height": int(vstream.get("height", 0)),
        "bitrate": bitrate,
    }


def video_already_efficient(meta):
    return (meta["codec"] == "hevc"
            and max(meta["width"], meta["height"]) <= MAX_VIDEO_DIM
            and 0 < meta["bitrate"] <= EFFICIENT_VIDEO_BPS)


def optimize_video(src, dst):
    scale = (f"scale='min({MAX_VIDEO_DIM},iw)':'min({MAX_VIDEO_DIM},ih)'"
             ":force_original_aspect_ratio=decrease:force_divisible_by=2")
    tmp = dst.with_name(dst.name + ".part" + dst.suffix)
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src),
           "-map", "0:v:0", "-map", "0:a:0?",
           "-c:v", "hevc_videotoolbox", "-q:v", str(VIDEOTOOLBOX_QUALITY),
           "-tag:v", "hvc1", "-vf", scale,
           "-c:a", "aac", "-b:a", "128k",
           "-map_metadata", "0", "-movflags", "use_metadata_tags+faststart",
           str(tmp)]
    r = run(cmd)
    if r.returncode != 0 or not tmp.exists() or tmp.stat().st_size == 0:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"ffmpeg failed: {r.stderr.strip()[:300]}")
    # sanity check the result decodes
    if run(["ffprobe", "-v", "error", str(tmp)]).returncode != 0:
        tmp.unlink(missing_ok=True)
        raise RuntimeError("encoded file failed ffprobe validation")
    tmp.rename(dst)
    return dst


# ---------------------------------------------------------------- pipeline

def finalize(src, produced, dst, relpath, action, args, stats):
    """Apply keep-smaller guard, mtime, and --replace swap for one finished file."""
    size_in = src.stat().st_size
    if produced is not None and produced.stat().st_size < size_in:
        shutil.copystat(src, produced)
        out_path, size_out = produced, produced.stat().st_size
    else:
        # not smaller (or intentionally copied): keep the original bytes
        if produced is not None:
            produced.unlink()
            action = "kept-original (not smaller)"
        if args.replace:
            stats.record(action, size_in, size_in)
            return
        out_path, size_out = dst.with_suffix(src.suffix), size_in
        shutil.copy2(src, out_path)

    if args.replace and produced is not None:
        backup = args.backup_dir / relpath
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(backup))
        final = src.with_suffix(out_path.suffix)
        shutil.move(str(out_path), str(final))
        size_out = final.stat().st_size

    stats.record(action, size_in, size_out)


def process_file(src, relpath, args, stats):
    ext = src.suffix.lower()
    dst = (args.output_dir / relpath) if not args.replace \
        else (args.work_dir / relpath)
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        if ext in PHOTO_EXTS:
            produced = optimize_photo(src, dst)
            finalize(src, produced, dst, relpath, "photo optimized", args, stats)
        elif ext in VIDEO_EXTS:
            meta = probe_video(src)
            if video_already_efficient(meta):
                finalize(src, None, dst, relpath, "video copied (already efficient)",
                         args, stats)
            else:
                produced = optimize_video(src, dst)
                finalize(src, produced, dst, relpath, "video re-encoded", args, stats)
        else:
            finalize(src, None, dst, relpath, "copied (other type)", args, stats)
    except Exception as e:
        stats.fail(relpath, str(e))
        try:
            if not args.replace:
                shutil.copy2(src, dst)
            stats.record("copied (failed to optimize)",
                         src.stat().st_size, src.stat().st_size)
        except OSError:
            pass


def gather(args):
    """Return (photos, videos, others) as lists of (src, relpath), applying resume-skip."""
    photos, videos, others, skipped = [], [], [], 0
    for src in sorted(args.input_dir.rglob("*")):
        if not src.is_file() or src.name.startswith("."):
            continue
        relpath = src.relative_to(args.input_dir)
        if args.replace:
            if args.work_dir in src.parents:
                continue
            if (args.backup_dir / relpath).exists():   # already replaced in a prior run
                skipped += 1
                continue
        else:
            out = args.output_dir / relpath
            if out.exists() or out.with_suffix(".jpg").exists():
                skipped += 1
                continue
        ext = src.suffix.lower()
        (photos if ext in PHOTO_EXTS else
         videos if ext in VIDEO_EXTS else others).append((src, relpath))
    return photos, videos, others, skipped


def check_disk_space(files, target_dir):
    batch = sum(src.stat().st_size for src, _ in files)
    free = shutil.disk_usage(target_dir).free
    if free < batch * 1.5:
        sys.exit(f"ERROR: {free / 1e9:.1f} GB free but batch is {batch / 1e9:.1f} GB "
                 f"(need 1.5x). Process a smaller batch.")


def report(stats, skipped):
    print("\n===== Report =====")
    for action, n in sorted(stats.counts.items()):
        print(f"  {action}: {n}")
    if skipped:
        print(f"  skipped (already done): {skipped}")
    if stats.bytes_in:
        saved = stats.bytes_in - stats.bytes_out
        print(f"  {stats.bytes_in / 1e9:.2f} GB -> {stats.bytes_out / 1e9:.2f} GB "
              f"({saved / stats.bytes_in * 100:.1f}% saved)")
    if stats.failures:
        print(f"\n  FAILURES ({len(stats.failures)}) — copied as-is:")
        for relpath, err in stats.failures:
            print(f"    {relpath}: {err}")


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("input_dir", type=Path)
    p.add_argument("output_dir", type=Path, nargs="?",
                   help="mirror output dir (omit with --replace)")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--photo-workers", type=int, default=4)
    p.add_argument("--replace", action="store_true",
                   help="swap optimized files in place (requires --backup-dir)")
    p.add_argument("--backup-dir", type=Path,
                   help="originals moved here in --replace mode")
    args = p.parse_args()

    args.input_dir = args.input_dir.resolve()
    if not args.input_dir.is_dir():
        sys.exit(f"ERROR: {args.input_dir} is not a directory")
    if args.replace:
        if not args.backup_dir:
            sys.exit("ERROR: --replace requires --backup-dir")
        args.backup_dir = args.backup_dir.resolve()
        if args.backup_dir == args.input_dir or args.input_dir in args.backup_dir.parents:
            sys.exit("ERROR: --backup-dir must be outside the input dir")
        args.work_dir = args.backup_dir / ".work"
    else:
        if not args.output_dir:
            sys.exit("ERROR: output_dir required (or use --replace)")
        args.output_dir = args.output_dir.resolve()
        if args.output_dir == args.input_dir or args.input_dir in args.output_dir.parents:
            sys.exit("ERROR: output_dir must be outside the input dir")

    photos, videos, others, skipped = gather(args)
    total = photos + videos + others
    print(f"Found {len(photos)} photos, {len(videos)} videos, "
          f"{len(others)} other files ({skipped} already done, skipped)")

    if args.dry_run:
        for src, relpath in total:
            ext = src.suffix.lower()
            kind = ("photo" if ext in PHOTO_EXTS else
                    "video" if ext in VIDEO_EXTS else "copy")
            print(f"  [{kind}] {relpath} ({src.stat().st_size / 1e6:.1f} MB)")
        print("\nDry run — nothing written.")
        return
    if not total:
        print("Nothing to do.")
        return

    if args.replace:
        args.backup_dir.mkdir(parents=True, exist_ok=True)
        args.work_dir.mkdir(parents=True, exist_ok=True)
        check_disk_space(total, args.backup_dir)
    else:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        check_disk_space(total, args.output_dir)

    stats = Stats()
    with ThreadPoolExecutor(max_workers=args.photo_workers) as pool:
        futures = [pool.submit(process_file, src, rel, args, stats)
                   for src, rel in photos + others]
        for i, (src, rel) in enumerate(videos, 1):   # sequential: one hw encoder
            print(f"  video {i}/{len(videos)}: {rel}")
            process_file(src, rel, args, stats)
        for f in futures:
            f.result()

    if args.replace:
        shutil.rmtree(args.work_dir, ignore_errors=True)
    report(stats, skipped)


if __name__ == "__main__":
    main()
