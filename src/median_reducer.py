#!/usr/bin/env python3

import sys

current_zone = None
counts = {}

def emit(zone, counts):
    total = sum(counts.values())

    values = sorted(float(v) for v in counts.keys())

    target1 = (total - 1) // 2
    target2 = total // 2

    pos = 0
    m1 = None
    m2 = None

    for value in values:
        cnt = counts[str(value)]

        if m1 is None and pos + cnt > target1:
            m1 = value

        if m2 is None and pos + cnt > target2:
            m2 = value

        pos += cnt

    median = (m1 + m2) / 2

    print(
        f"{zone}\t{median:.3f}\t{total}\t{len(counts)}"
    )

for line in sys.stdin:

    zone, distance, cnt = line.strip().split("\t")
    cnt = int(cnt)

    if zone != current_zone:

        if current_zone is not None:
            emit(current_zone, counts)

        current_zone = zone
        counts = {distance: cnt}

    else:
        counts[distance] = counts.get(distance, 0) + cnt

if current_zone is not None:
    emit(current_zone, counts)