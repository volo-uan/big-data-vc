#!/usr/bin/env python3

import sys

current_key = None
count = 0

for line in sys.stdin:

    zone, distance, cnt = line.strip().split("\t")

    key = f"{zone}\t{distance}"
    cnt = int(cnt)

    if key == current_key:
        count += cnt
    else:

        if current_key is not None:
            print(f"{current_key}\t{count}")

        current_key = key
        count = cnt

if current_key is not None:
    print(f"{current_key}\t{count}")