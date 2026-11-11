#!/usr/bin/env python3

import sys

current_zone = None
total_distance = 0.0
trip_count = 0

for line in sys.stdin:
    zone, distance = line.strip().split("\t")
    distance = float(distance)

    if zone == current_zone:
        total_distance += distance
        trip_count += 1
    else:
        if current_zone is not None:
            avg = total_distance / trip_count
            print(f"{current_zone}\t{avg:.4f}\t{trip_count}")

        current_zone = zone
        total_distance = distance
        trip_count = 1

if current_zone is not None:
    avg = total_distance / trip_count
    print(f"{current_zone}\t{avg:.4f}\t{trip_count}")