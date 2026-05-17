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
    if len(parts) >= 9:
        building = parts[2]
        status = parts[8]
        if status == 'WARNING' or status == 'ERROR':
            print(f"{building}\t1")
