#!/usr/bin/env python3

import sys

first = True

for line in sys.stdin:
    if first:
        first = False
        continue

    cols = line.strip().split(",")

    try:
        zone = cols[7]
        distance = float(cols[4])

        print(f"{zone}\t{distance}")
    except:
        pass