#!/usr/bin/env python3
"""
Scans a local samples folder and builds strudel.json manually.

Avoids the @strudel/sampler CLI entirely (its ASCII banner corrupts
stdout JSON). Encodes paths the way Strudel's samples() loader expects:
no leading slash, spaces/special chars percent-encoded, '/' and '.'
left alone.

Each leaf directory (a directory that directly contains audio files)
becomes one instrument entry. Nested folders get hyphen-joined keys,
e.g. merah/dub-chords-from-the-archives-samples -> "merah-dub-chords-from-the-archives-samples".
"""

import json
import os
from pathlib import Path
from urllib.parse import quote

AUDIO_EXTS = {".wav", ".mp3", ".ogg", ".flac", ".aif", ".aiff"}

# --- CONFIG: edit these for your setup ---
SAMPLES_ROOT = Path(__file__).resolve().parent
GITHUB_USER = "enfantdo"
GITHUB_REPO = "ubiquitous-enigma"
GITHUB_BRANCH = "main"
OUTPUT_PATH = SAMPLES_ROOT / "strudel.json"
# ------------------------------------------


def encode_path(rel_path: str) -> str:
    return quote(rel_path, safe="/.")


def build_json():
    entries = {}

    for dirpath, dirnames, filenames in os.walk(SAMPLES_ROOT):
        dirpath = Path(dirpath)
        if dirpath == SAMPLES_ROOT:
            continue
        if ".git" in dirpath.parts:
            continue

        audio_files = sorted(
            f for f in filenames if Path(f).suffix.lower() in AUDIO_EXTS
        )
        if not audio_files:
            continue

        rel_dir = dirpath.relative_to(SAMPLES_ROOT)
        key = "-".join(rel_dir.parts)
        rel_paths = [encode_path(f"{rel_dir.as_posix()}/{f}") for f in audio_files]

        entries[key] = rel_paths[0] if len(rel_paths) == 1 else rel_paths

    data = {
        "_base": (
            f"https://raw.githubusercontent.com/"
            f"{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/"
        ),
        **entries,
    }

    OUTPUT_PATH.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Wrote {OUTPUT_PATH} with {len(entries)} instrument(s):")
    for k in entries:
        print(f"  - {k}")


if __name__ == "__main__":
    build_json()
