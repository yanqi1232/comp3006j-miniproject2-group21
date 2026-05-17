#!/usr/bin/env python3
import sys
from collections import defaultdict

counts = defaultdict(int)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    device, val = line.split('\t')
    counts[device] += int(val)

sorted_devices = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]

for device, cnt in sorted_devices:
    print(f"{device}\t{cnt}")
