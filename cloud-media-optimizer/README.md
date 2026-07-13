# cloud-media-optimizer

Reclaim Google Photos and OneDrive storage: compress photos/videos to Google
"Storage saver" quality (photos ≤16 MP, videos ≤1080p HEVC) locally, keep the
optimized set as your archive, re-upload it, delete the fat cloud originals.

**Rule #1: never delete a cloud original until its optimized replacement is
verified in the cloud.**

## Setup (once)

```bash
brew install exiftool        # ffmpeg + sips assumed present
```

Both scripts are stdlib-only Python 3 — no pip installs.

## What each script does

| Script | Purpose |
|---|---|
| `takeout_fix.py TAKEOUT_DIR` | Merge Takeout JSON sidecar capture-time/GPS into files that are missing it, and fix file mtimes. Run **before** optimizing. Never overwrites existing embedded metadata. |
| `optimize.py IN OUT` | Mirror `IN` into `OUT` with photos ≤16 MP (same format, q80; PNG→JPEG) and videos ≤1080p HEVC (VideoToolbox hardware encoder). Metadata and mtimes preserved. Resumable; keeps the original bytes whenever recompression isn't smaller. |
| `optimize.py DIR --replace --backup-dir BAK` | Same optimization but swaps files in place (for a OneDrive synced folder). Every original is moved to `BAK` first — nothing is deleted. |

Both support `--dry-run`.

## Google Photos runbook (per batch — one year / one Takeout archive at a time)

1. **Export**: [takeout.google.com](https://takeout.google.com) → deselect all →
   Google Photos only → pick the year's albums (or take the full split archives
   and do one archive per batch). Download and extract.
2. **Fix metadata**:
   ```bash
   python3 takeout_fix.py ~/takeout-2019/
   ```
   Review the UNMATCHED list — those files have no sidecar (usually fine if
   they already have EXIF).
3. **Optimize**:
   ```bash
   python3 optimize.py ~/takeout-2019/ ~/photos-archive/2019/
   ```
   Disk check: you need ~1.5× the batch size free.
4. **Spot-check** the report and a handful of outputs: dates and GPS present,
   videos play, savings look right (typically 50–80%).
5. **Re-upload**: drag `~/photos-archive/2019/` folders into
   [photos.google.com](https://photos.google.com) → wait for upload to finish →
   confirm items appear **with correct dates** in the timeline.
6. **Delete originals** (manual — no API for this): in the web UI, search the
   date range, select-all per day/month, delete. The re-uploaded copies are
   distinguishable by their newer upload date in search tools; go carefully.
   Then Trash → Empty trash (space frees after that).
7. Keep `~/photos-archive/2019/` as your local archive; delete the Takeout
   extract to free disk. Next batch.

> Shortcut with zero control: Google Photos → Settings → **Recover storage**
> compresses everything already uploaded in one click. This pipeline exists
> because you want control + a local archive.

## OneDrive runbook

OneDrive is synced locally, so it's one command per folder:

```bash
python3 optimize.py ~/OneDrive/Pictures/2019 \
    --replace --backup-dir ~/onedrive-originals/2019
```

Sync uploads the smaller files automatically. Verify in the OneDrive web UI
(open a few photos/videos), and only then delete `~/onedrive-originals/2019`.

Notes for `--replace`:
- `--backup-dir` is required and must be outside the input folder.
- Resume works via the backup dir: a file whose backup already exists is
  skipped. Don't delete the backup until the whole folder is done and verified.
- Pause OneDrive sync during the run if you want to avoid churn, resume after.

## Quality settings (edit constants at the top of optimize.py)

| Constant | Default | Meaning |
|---|---|---|
| `MAX_PIXELS` | 16 MP | photo resolution cap (Google Storage saver) |
| `JPEG_QUALITY` | 80 | JPEG/HEIC recompression quality |
| `MAX_VIDEO_DIM` | 1920 | video longest side (1080p) |
| `VIDEOTOOLBOX_QUALITY` | 60 | HEVC constant-quality (higher = better/bigger) |
| `EFFICIENT_VIDEO_BPS` | 6 Mbps | already-HEVC-1080p videos under this are copied, not re-encoded |
