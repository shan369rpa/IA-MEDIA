import xml.etree.ElementTree as ET
import csv
import os

fcpxml_file = r"D:\IA MEDIA\Data\daphantich\2004.09.19-đối phó với cơn bão trong lòng\2004.09.19-đối phó với cơn bão trong lòng.fcpxml"
output_csv = "D:\\IA MEDIA\\Data\\daphantich\\keyframes_summary.csv"

def sec_to_minsec(seconds):
    minutes = int(seconds // 60)
    seconds_int = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{minutes}:{seconds_int:02d}:{milliseconds:03d}"



def parse_time(time_str):
    time_str = time_str.strip()
    if time_str.endswith('s'):
        time_str = time_str[:-1]
    if '/' in time_str:
        num, denom = time_str.split('/')
        return float(num)/float(denom)
    return float(time_str)

def parse_value(value_str):
    if value_str.endswith('dB'):
        return float(value_str.replace('dB',''))
    return float(value_str)

def classify_action(delta, value):
    if value <= -95:
        return 'Mute'
    elif delta >= 10:
        return 'Hard Cut / Boost'
    elif delta >= 3:
        return 'Minor Adjustment'
    else:
        return 'Hold'

tree = ET.parse(fcpxml_file)
root = tree.getroot()

with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['clip_name','keyframe_time_in_clip','timeline_time','volume_dB','action_type'])

    for asset_clip in root.findall(".//asset-clip"):
        clip_name = asset_clip.attrib.get('name','UnknownClip')
        start_time = parse_time(asset_clip.attrib.get('start','0s'))
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
        
        keyframes.sort()
        prev_v = None
        for t_sec, v_db in keyframes:
            timeline_sec = start_time + t_sec
            timeline_time_str = sec_to_minsec(timeline_sec)   # chuyển sang mm:ss
            delta = abs(v_db - prev_v) if prev_v is not None else 0
            action = classify_action(delta, v_db)
            writer.writerow([clip_name, t_sec, timeline_time_str, v_db, action])
            prev_v = v_db

print(f"CSV with keyframes exported to: {output_csv}")
