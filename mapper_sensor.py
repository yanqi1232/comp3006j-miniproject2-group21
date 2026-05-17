#!/usr/bin/env python3
import sys

first_line = True

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    if first_line:
        first_line = False
        continue

    parts = line.split(',')
    if len(parts) >= 6:
        sensor_type = parts[5]
        print(f"{sensor_type}\t1")
