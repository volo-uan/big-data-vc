#!/usr/bin/env bash
# W3 - loads the yearly dataset into HDFS.
# Runs INSIDE the cluster, where the hdfs client and its configuration live:
#   docker compose -f compose-hdfs.yml exec namenode bash /scripts/load_to_hdfs.sh | tee out/02-load.log
# Must be re-runnable: after the cluster is destroyed you want to restore
# the state with one command, not twelve.
#
# Fill in the places marked TODO.
#!/usr/bin/env bash
set -euo pipefail

HDFS_DIR="/taxi"
LOCAL_DIR="${1:-/mnt/host}"

echo "== creating target directory in HDFS =="

hdfs dfs -mkdir -p "$HDFS_DIR"

echo "== removing old files =="

hdfs dfs -rm -f "$HDFS_DIR"/* 2>/dev/null || true

echo "== uploading files =="

for f in "$LOCAL_DIR"/yellow_tripdata_2024-*.parquet; do
  echo "  -> $(basename "$f")"

  hdfs dfs -put -f "$f" "$HDFS_DIR/"
done

echo "== verification =="

COUNT=$(hdfs dfs -ls "$HDFS_DIR" | grep parquet | wc -l)

echo "files in $HDFS_DIR: $COUNT"