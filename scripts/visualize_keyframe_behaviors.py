import csv
import matplotlib.pyplot as plt

# CSV xuất ra từ script trước
csv_file = r"C:\Users\Son\Documents\GitHub\IA-MEDIA\fcpxml_keyframe_behavior.csv"

# Màu cho từng behavior
behavior_colors = {
    "Mute / Hold": "gray",
    "Hold": "lightblue",
    "Fade In": "green",
    "Fade Out": "red",
    "Fade In / Boost": "darkgreen",
    "Fade Out / Dip": "darkred",
    "Hard Cut": "orange",
    "Minor Adjustment": "purple"
}

# Đọc dữ liệu CSV
times = []
values = []
colors = []

with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        start = float(row['start_sec'])
        end = float(row['end_sec'])
        v_start = float(row['v_start_dB'])
        v_end = float(row['v_end_dB'])
        behavior = row['behavior']

        # Chia nhỏ thành 2 điểm: start và end
        times.extend([start, end])
        values.extend([v_start, v_end])
        # Gán màu cùng behavior cho cả đoạn
        colors.extend([behavior_colors.get(behavior, "black")]*2)

# Vẽ
plt.figure(figsize=(16,6))
for i in range(0, len(times)-1, 2):
    plt.plot(times[i:i+2], values[i:i+2], color=colors[i], linewidth=2)

plt.xlabel("Time (s)")
plt.ylabel("Volume (dB)")
plt.title("Keyframe Volume Curve with Behavior Highlight")
plt.grid(True)
plt.show()
