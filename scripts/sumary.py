import xml.etree.ElementTree as ET
import os
import csv

fcpxml_file = r"D:\IA MEDIA\Data\daphantich\2004.09.19-đối phó với cơn bão trong lòng\2004.09.19-đối phó với cơn bão trong lòng.fcpxml"

output_csv = r"D:\IA MEDIA\Data\daphantich\summary_detailed.csv"

def parse_time(time_str):
    time_str = time_str.strip()
    if time_str.endswith('s'):
        time_str = time_str[:-1]
    if '/' in time_str:
        num, den = time_str.split('/')
        return float(num)/float(den)
    return float(time_str)

def parse_value(val_str):
    if val_str.endswith('dB'):
        return float(val_str.replace('dB',''))
    return float(val_str)

def classify_behavior(keyframes):
    MUTE_THRESHOLD = -95
    DELTA_MINOR = 2
    DELTA_HARD = 10
    SUSTAIN_THRESHOLD = 6

    total_keyframes = len(keyframes)
    mute = hold = minor = hard = fade_in = fade_out = sustain_boost = 0

    if total_keyframes == 0:
        return {}

    prev_val = keyframes[0][1]
    sustain_count = 0
    for i in range(total_keyframes):
        t, v = keyframes[i]
        delta = v - prev_val if i > 0 else 0

        if v <= MUTE_THRESHOLD:
            mute += 1
        elif abs(delta) <= DELTA_MINOR:
            hold += 1
        elif abs(delta) >= DELTA_HARD:
            hard += 1
        else:
            minor += 1

        if i > 0:
            if delta > 0:
                fade_in += 1
            elif delta < 0:
                fade_out += 1

        if v >= 0:
            sustain_count += 1
            if sustain_count >= 3:
                sustain_boost += 1
        else:
            sustain_count = 0

        prev_val = v

    avg_vol = sum(v for t, v in keyframes)/total_keyframes
    min_vol = min(v for t, v in keyframes)
    max_vol = max(v for t, v in keyframes)

    return {
        "total_keyframes": total_keyframes,
        "Mute": mute,
        "Hold": hold,
        "Minor Adjustment": minor,
        "Hard Cut": hard,
        "Fade In": fade_in,
        "Fade Out": fade_out,
        "Sustain Boost": sustain_boost,
        "avg_volume": round(avg_vol,2),
        "min_volume": round(min_vol,2),
        "max_volume": round(max_vol,2)
    }

# Parse FCPXML
tree = ET.parse(fcpxml_file)
root = tree.getroot()

rows = []

for asset_clip in root.findall(".//asset-clip"):
    clip_name = asset_clip.attrib.get('name','UnknownClip')
    # Thời gian clip trên timeline
    start_time = parse_time(asset_clip.attrib.get('start','0'))
    duration = parse_time(asset_clip.attrib.get('duration','0'))
    end_time = start_time + duration

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

    behavior_stats = classify_behavior(keyframes)
    behavior_stats["file"] = clip_name
    behavior_stats["start_time"] = round(start_time,3)
    behavior_stats["end_time"] = round(end_time,3)
    rows.append(behavior_stats)

# Write CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(f"Summary saved to {output_csv}")
