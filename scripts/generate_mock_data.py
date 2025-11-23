# scripts/generate_mock_data.py

import os
import subprocess
import numpy as np
from scipy.io.wavfile import write as write_wav
import xml.etree.ElementTree as ET
from xml.dom import minidom

# --- CẤU HÌNH ---
BATCH_NAME = "Batch_01"
SESSION_ID = "2025-01-01-dummy-test"
DATA_DIR = os.path.join("data", BATCH_NAME)

# Định dạng tên file theo quy ước (FILE_NAMING_CONVENTION.md)
RAW_FILENAME = f"{SESSION_ID}_raw.mp4"
EDITED_FILENAME = f"{SESSION_ID}_edited.mp4"
FCPXML_FILENAME = f"{SESSION_ID}.fcpxml"

# Thông số giả lập
SAMPLE_RATE = 16000
RAW_DURATION = 60  # Video gốc dài 60 giây
EDITED_START = 10  # Video đã sửa bắt đầu từ giây thứ 10 của Raw
EDITED_DURATION = 30 # Video đã sửa dài 30 giây

def generate_sine_wave(filename, duration, rate=SAMPLE_RATE):
    """Tạo file audio WAV chứa sóng sine (âm thanh bíp) để giả lập tiếng nói."""
    t = np.linspace(0., duration, int(rate * duration))
    # Tạo âm thanh 440Hz (note La)
    data = 0.5 * np.sin(2. * np.pi * 440. * t)
    
    # Thêm một chút ngắt quãng để Whisper có thể nhận diện như các "từ"
    # Cứ mỗi 0.5s thì im lặng 0.1s
    mask = np.ones_like(data)
    cycle_samples = int(rate * 0.6)
    silence_samples = int(rate * 0.1)
    for i in range(0, len(data), cycle_samples):
        end = min(i + silence_samples, len(data))
        mask[i:end] = 0
    
    data = data * mask
    write_wav(filename, rate, (data * 32767).astype(np.int16))
    print(f"--> Đã tạo audio tạm: {filename}")

def create_video_from_audio(audio_path, output_video_path, duration):
    """Dùng FFmpeg tạo video MP4 từ file audio và hình ảnh testsrc."""
    if os.path.exists(output_video_path):
        print(f"--> Video đã tồn tại, bỏ qua: {output_video_path}")
        return

    print(f"--> Đang tạo video: {output_video_path} ({duration}s)...")
    # Sử dụng testsrc của ffmpeg để tạo hình ảnh đồng hồ chạy
    command = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"testsrc=size=640x360:rate=24:duration={duration}",
        "-i", audio_path,
        "-c:v", "libx264", "-preset", "ultrafast",
        "-c:a", "aac", "-shortest",
        "-loglevel", "error",
        output_video_path
    ]
    subprocess.run(command, check=True)
    print(f"    OK.")

def create_fcpxml(output_path, raw_filename, raw_duration, run_start, run_duration):
    """Tạo file FCPXML mô tả mối quan hệ giữa Raw và Edited."""
    
    # Cấu trúc cơ bản của FCPXML
    fcpxml = ET.Element("fcpxml", version="1.9")
    resources = ET.SubElement(fcpxml, "resources")
    
    # Định nghĩa tài nguyên (File Raw)
    asset_id = "r1"
    asset = ET.SubElement(resources, "asset", id=asset_id, name=raw_filename, src=f"file:///mock/path/{raw_filename}", duration=f"{raw_duration}s")
    
    library = ET.SubElement(fcpxml, "library")
    event = ET.SubElement(library, "event", name="Mock Event")
    project = ET.SubElement(event, "project", name="Mock Project")
    sequence = ET.SubElement(project, "sequence", duration=f"{run_duration}s")
    spine = ET.SubElement(sequence, "spine")
    
    # Tạo Clip: Lấy một đoạn từ Raw đưa vào timeline
    # start: Thời điểm bắt đầu lấy trên file RAW
    # duration: Độ dài đoạn lấy
    # offset: Thời điểm đặt trên timeline EDITED (ở đây là 0s, đầu video)
    ET.SubElement(spine, "asset-clip", 
                  ref=asset_id, 
                  name=raw_filename, 
                  offset="0s", 
                  start=f"{run_start}s", 
                  duration=f"{run_duration}s")

    # Lưu file XML đẹp (pretty print)
    xml_str = minidom.parseString(ET.tostring(fcpxml)).toprettyxml(indent="    ")
    with open(output_path, "w") as f:
        f.write(xml_str)
    print(f"--> Đã tạo FCPXML: {output_path}")

def main():
    # 1. Tạo thư mục
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Đường dẫn các file đích
    raw_video_path = os.path.join(DATA_DIR, RAW_FILENAME)
    edited_video_path = os.path.join(DATA_DIR, EDITED_FILENAME)
    fcpxml_path = os.path.join(DATA_DIR, FCPXML_FILENAME)
    
    temp_audio_path = "temp_mock_audio.wav"

    try:
        # 2. Tạo Video RAW
        print("1. Đang tạo Video RAW...")
        generate_sine_wave(temp_audio_path, RAW_DURATION)
        create_video_from_audio(temp_audio_path, raw_video_path, RAW_DURATION)
        
        # 3. Tạo Video EDITED (Cắt từ Raw hoặc tạo mới ngắn hơn)
        print("2. Đang tạo Video EDITED...")
        # Để đơn giản, ta tạo một video mới ngắn hơn, tương ứng với đoạn cắt logic
        generate_sine_wave(temp_audio_path, EDITED_DURATION)
        create_video_from_audio(temp_audio_path, edited_video_path, EDITED_DURATION)
        
        # 4. Tạo file FCPXML
        print("3. Đang tạo FCPXML...")
        # Logic: Video Edited lấy từ giây thứ 10 của Raw, dài 30s
        create_fcpxml(fcpxml_path, RAW_FILENAME, RAW_DURATION, EDITED_START, EDITED_DURATION)
        
        print("\n✅ HOÀN TẤT! Dữ liệu mẫu đã sẵn sàng tại:")
        print(f"   {DATA_DIR}")
        print(f"   - {RAW_FILENAME}")
        print(f"   - {EDITED_FILENAME}")
        print(f"   - {FCPXML_FILENAME}")

    except Exception as e:
        print(f"\n❌ LỖI: {e}")
    finally:
        # Dọn dẹp file tạm
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

if __name__ == "__main__":
    main()