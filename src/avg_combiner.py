#!/usr/bin/env python3

import sys

current_zone = None
total = 0.0
count = 0

for line in sys.stdin:
    zone, distance = line.strip().split("\t")
    distance = float(distance)

    if zone == current_zone:
        total += distance
        count += 1
    else:
        if current_zone is not None:
            print(f"{current_zone}\t{total / count}")

        current_zone = zone
        total = distance
        count = 1

if current_zone is not None:
    print(f"{current_zone}\t{total / count}")