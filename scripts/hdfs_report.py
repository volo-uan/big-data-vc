#!/usr/bin/env python3
"""W3 - reports how a file is stored in HDFS.

Runs `hdfs fsck` and turns its output into three numbers. The shell is fine for
starting containers; pulling numbers out of text is Python's job, which is why
this script is Python and load_to_hdfs.sh is not.

Usage:
    python3 scripts/hdfs_report.py /taxi/yellow_tripdata_2024-01.parquet

Fill in the places marked TODO.
"""
import re
import subprocess
import sys

COMPOSE = ["docker", "compose", "-f", "compose-hdfs.yml", "exec", "-T", "namenode"]


def fsck(path: str) -> str:
    result = subprocess.run(
        COMPOSE + ["hdfs", "fsck", path],
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout


def parse(report: str) -> dict:
    """Pull the numbers we care about out of the fsck output.

    Return a dict with keys: size, files, blocks, replication.
    The lines you are looking for are shaped like:

        Total size:                    49961641 B
        Total files:                   1
        Total blocks (validated):      2 (avg. block size 24980820 B)
        Average block replication:     2.0
    """
    size = int(
        re.search(
            r"Total size:\s+(\d+)",
            report
        ).group(1)
    )

    files = int(
        re.search(
            r"Total files:\s+(\d+)",
            report
        ).group(1)
    )

    blocks = int(
        re.search(
            r"Total blocks \(validated\):\s+(\d+)",
            report
        ).group(1)
    )

    replication = float(
        re.search(
            r"Average block replication:\s+([0-9.]+)",
            report
        ).group(1)
    )

    return {
        "size": size,
        "files": files,
        "blocks": blocks,
        "replication": replication,
    }


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: hdfs_report.py <hdfs-path>")
    path = sys.argv[1]
    data = parse(fsck(path))

    print(f"path        : {path}")
    print(f"size        : {data['size']:,} B")
    print(f"files       : {data['files']}")
    print(f"blocks      : {data['blocks']}")
    print(f"replication : {data['replication']}")

    disk_usage = int(
        data["size"] * data["replication"]
    )

    map_tasks = data["blocks"]

    print(f"disk usage  : {disk_usage:,} B")
    print(f"map tasks   : {map_tasks}")


if __name__ == "__main__":
    main()
