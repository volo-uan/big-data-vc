#!/usr/bin/env python3

import sys

current_zone = None
sum_distance = 0.0
count = 0

for line in sys.stdin:

    zone, distance, cnt = line.strip().split("\t")

    distance = float(distance)
    cnt = int(cnt)

    if zone == current_zone:
        sum_distance += distance
        count += cnt
    else:

        if current_zone is not None:
            print(f"{current_zone}\t{sum_distance}\t{count}")

        current_zone = zone
        sum_distance = distance
        count = cnt

if current_zone is not None:
    print(f"{current_zone}\t{sum_distance}\t{count}")