#!/usr/bin/env bash
set -euo pipefail

########################
# CONFIGURATION
########################

# Folder on your Mac you want to sync (absolute path, no trailing slash)
SRC="/Users/jeremiassiehr/Documents/Amitis/Data"

# Mount point of your external drive (check under /Volumes)
DEST="/Volumes/DataStorage/Data"

# Keep this many days on the SOURCE (Mac)
KEEP_DAYS=90

########################
# PRE-CHECKS
########################

if [[ ! -d "$SRC" ]]; then
  echo "Source folder does not exist: $SRC" >&2
  exit 1
fi

if [[ ! -d "$DEST" ]]; then
  echo "Destination folder does not exist or drive not mounted: $DEST" >&2
  exit 1
fi

########################
# STEP 1: SYNC FROM SOURCE TO EXTERNAL
########################
# Copy new/changed files to external, but do NOT delete anything on external.
# rsync will not touch the source except for reading it.[web:29]

rsync -av "$SRC"/ "$DEST"/

########################
# STEP 2: DELETE OLD DATED FOLDERS FROM SOURCE
########################
# Assumes top-level dirs named YYYY_MM_DD under $SRC.
# Everything (including old data) remains on $DEST.

# macOS date: use -v-<n>d to go back N days.[web:30][web:44]
CUTOFF_DATE=$(date -v-"${KEEP_DAYS}"d +"%Y_%m_%d")

echo "On SOURCE: keeping date-folders from $CUTOFF_DATE and newer."
echo "Older date-folders will be deleted from SOURCE (but kept on DEST)."

find "$SRC" -maxdepth 1 -type d -regex '.*/[0-9]\{4\}_[0-9]\{2\}_[0-9]\{2\}' | while read -r dir; do
  basename_dir=$(basename "$dir")

  # For YYYY_MM_DD, lexicographic compare matches chronological order.[web:41]
  if [[ "$basename_dir" < "$CUTOFF_DATE" ]]; then
    echo "Deleting old folder from SOURCE (already backed up): $dir"
    rm -rf -- "$dir"
  fi
done

echo "Done: data kept fully on external, source trimmed to last $KEEP_DAYS days."