import xml.etree.ElementTree as ET
import os
import csv
import uuid

fcpxml_file = "D:\\IA MEDIA\\Data\\daphantich\\2004.09.19-đối phó với cơn bão trong lòng\\2004.09.19-đối phó với cơn bão trong lòng.fcpxml"
output_dir = r"C:\Users\Son\Documents\GitHub\IA-MEDIA\data_csv"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def parse_time(time_str):
    time_str = time_str.strip()
    if time_str.endswith('s'):
        time_str = time_str[:-1]
    if '/' in time_str:
        numerator, denominator = time_str.split('/')
        return float(numerator)/float(denominator)
    return float(time_str)

def parse_value(value_str):
    if value_str.endswith('dB'):
        return float(value_str.replace('dB',''))
    return float(value_str)

tree = ET.parse(fcpxml_file)
root = tree.getroot()

for idx, asset_clip in enumerate(root.findall(".//asset-clip")):
    clip_name = asset_clip.attrib.get('name','UnknownClip')
    keyframes = []

    for adj_vol in asset_clip.findall('.//adjust-volume'):
        for param in adj_vol.findall('param'):
            if param.attrib.get('name') != 'amount':
                continue
            for kfa in param.findall('keyframeAnimation'):
                for kf in kfa.findall('keyframe'):
                    time = kf.attrib.get('time')
                    value = kf.attrib.get('value')
                    if time and value:
                        t_sec = parse_time(time)
                        v_db = parse_value(value)
                        keyframes.append((t_sec, v_db))
    
    if keyframes:
        keyframes.sort()
        
        # Tạo file csv tên clip kèm chỉ số để tránh trùng
        csv_file = os.path.join(output_dir, f"{clip_name}_{idx}.csv")
        
        with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Header
            writer.writerow(["Time(s)", "Volume(dB)", "Delta(dB)"])
            
            prev_v = None
            for t, v in keyframes:
                delta = v - prev_v if prev_v is not None else 0
                writer.writerow([t, v, delta])
                prev_v = v
        
        print(f"Saved CSV data for {clip_name} -> {csv_file}")
