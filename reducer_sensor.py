#!/usr/bin/env python3
import sys

current_sensor = None
count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    sensor, val = line.split('\t')
    if current_sensor == sensor:
        count = count + int(val)
    else:
        if current_sensor is not None:
            print(f"{current_sensor}\t{count}")
        current_sensor = sensor
        count = int(val)

if current_sensor is not None:
    print(f"{current_sensor}\t{count}")
