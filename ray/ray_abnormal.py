#!/usr/bin/env python3
import ray
import pandas as pd
import oss2
from io import StringIO

# Configuration
ACCESS_KEY_ID = os.environ.get('OSS_ACCESS_KEY_ID')
ACCESS_KEY_SECRET = os.environ.get('OSS_ACCESS_KEY_SECRET')
BUCKET_NAME = 'iot-project-group21'
ENDPOINT = 'oss-cn-beijing.aliyuncs.com'
FILE_KEY = 'Comp3006J MiniProject 2 Dataset.csv'

print("=" * 60)
print("Ray Abnormal Device Detection - Reading data directly from OSS")
print("=" * 60)

# Read data from OSS
auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)
content = bucket.get_object(FILE_KEY).read().decode('utf-8')
df = pd.read_csv(StringIO(content))

print(f"Successfully read! Total {len(df)} rows, {df['device_id'].nunique()} devices")

# Initialize Ray
ray.init(ignore_reinit_error=True)

@ray.remote
def detect_abnormal(device_id, device_df):
    reasons = []
    device_df = device_df.copy()
    device_df['battery_level'] = pd.to_numeric(device_df['battery_level'], errors='coerce')
    device_df['value'] = pd.to_numeric(device_df['value'], errors='coerce')
    
    if device_df['battery_level'].min() < 20:
        reasons.append("low battery")
    if len(device_df[device_df['status'] == 'ERROR']) >= 3:
        reasons.append("repeated errors")
    high_temp = device_df[(device_df['sensor_type'] == 'temperature') & (device_df['value'] > 32)]
    if len(high_temp) >= 3:
        reasons.append("repeated high temperature")
    
    if reasons:
        return (device_id, device_df['building'].iloc[0], ", ".join(reasons))
    return None

# Parallel detection
print("\nDetecting abnormal devices in parallel...")
grouped = df.groupby('device_id')
futures = [detect_abnormal.remote(device_id, group) for device_id, group in grouped]
results = ray.get(futures)

# Output results
print("\nAbnormal device list (device_id, building, reason):")
print("-" * 50)
count = 0
for r in results:
    if r:
        print(f"{r[0]}, {r[1]}, {r[2]}")
        count += 1
print(f"\nTotal {count} abnormal devices found")

ray.shutdown()
