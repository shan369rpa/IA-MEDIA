# fcpxml_utils.py (Fixed)
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import ffmpeg
import math

def get_video_info(video_path):
    """
    Lấy thông tin FPS, Duration và Timecode Start chuẩn xác từ FFmpeg.
    """
    try:
        probe = ffmpeg.probe(video_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        format_info = probe['format']
        
        if not video_stream:
            return None

        # 1. Xử lý Frame Rate (r_frame_rate)
        # r_frame_rate thường dạng "24000/1001" (23.98fps) hoặc "30000/1001" (29.97fps)
        num, den = map(int, video_stream['r_frame_rate'].split('/'))
        
        # FCPXML quy ước: frameDuration = mẫu số / tử số
        frame_duration_str = f"{den}/{num}s"

        # 2. Xử lý Duration
        # Lấy duration gốc (tính bằng giây)
        duration_sec = float(format_info.get('duration', 0))
        
        # Chuyển đổi sang đơn vị tick của FCP (dựa trên tử số FPS làm mẫu số thời gian)
        # Công thức: duration_ticks = seconds * FPS_numerator / FPS_denominator * FPS_denominator
        # Rút gọn: duration_ticks = seconds * FPS_numerator
        # Ví dụ: 9s * 24000 = 216000 ticks. XML: "216000/24000s"
        total_duration_ticks = int(duration_sec * num / den * den) # Giữ nguyên mẫu số của timebase
        # Cách FCP: duration luôn có mẫu số khớp với frameDuration nghịch đảo (tức là num)
        # Tuy nhiên file chuẩn của bạn dùng mẫu số 24000 (tử số fps). Hãy theo chuẩn đó.
        
        total_duration_str = f"{int(duration_sec * num)}/{num}s"

        # 3. Xử lý Start Timecode (Quan trọng để fix lỗi "Invalid edit")
        # Một số file quay chuyên nghiệp có timecode bắt đầu != 0
        start_time_sec = 0
        if 'tags' in format_info and 'timecode' in format_info['tags']:
            # Parse timecode HH:MM:SS:FF sang giây (Logic phức tạp, tạm thời bỏ qua nếu không cần thiết)
            # Hoặc lấy start_time từ stream nếu có
            pass
        
        # Nếu FFmpeg start_time có giá trị
        if 'start_time' in format_info:
            try:
                start_time_sec = float(format_info['start_time'])
            except:
                start_time_sec = 0
        
        start_ticks = int(start_time_sec * num)
        asset_start_str = f"{start_ticks}/{num}s"

        return {
            "width": video_stream['width'],
            "height": video_stream['height'],
            "frame_duration": frame_duration_str, # vd: 1001/24000s
            "total_duration": total_duration_str, # vd: 9009/24000s
            "asset_start": asset_start_str,       # vd: 0s hoặc 30816786/24000s
            "fps_num": num,
            "fps_den": den
        }
    except Exception as e:
        print(f"Lỗi đọc video info: {e}")
        return None

def create_fcpxml(output_path, video_path, markers):
    video_info = get_video_info(video_path)
    if not video_info:
        return False, "Không đọc được thông tin video."

    video_name = os.path.basename(video_path)
    
    # Dùng version 1.10 (An toàn nhất)
    root = ET.Element("fcpxml", version="1.10")
    
    resources = ET.SubElement(root, "resources")
    format_id = "r1"
    asset_id = "r2"
    
    # Format
    ET.SubElement(resources, "format", 
                  id=format_id, 
                  name=f"FFVideoFormat{video_info['height']}p", 
                  frameDuration=video_info['frame_duration'], 
                  width=str(video_info['width']), 
                  height=str(video_info['height']))

    # Asset: Thêm start đúng và media-rep
    asset = ET.SubElement(resources, "asset", 
                          id=asset_id, 
                          name=video_name, 
                          start=video_info['asset_start'], 
                          duration=video_info['total_duration'], 
                          hasVideo="1", hasAudio="1", format=format_id)
    
    # Đường dẫn file tuyệt đối
    asset_url = f"file://{os.path.abspath(video_path)}".replace("\\", "/")
    ET.SubElement(asset, "media-rep", kind="original-media", src=asset_url)

    # Library Structure
    library = ET.SubElement(root, "library")
    event = ET.SubElement(library, "event", name="IA Media Analysis")
    project = ET.SubElement(event, "project", name=f"Errors: {video_name}")
    
    # Sequence duration phải khớp Asset duration
    sequence = ET.SubElement(project, "sequence", duration=video_info['total_duration'], format=format_id)
    spine = ET.SubElement(sequence, "spine")
    
    # Asset Clip
    # Quan trọng: start của clip phải khớp start của asset
    clip = ET.SubElement(spine, "asset-clip", 
                         ref=asset_id, name=video_name, 
                         offset="0s", 
                         start=video_info['asset_start'], # Fix lỗi Invalid edit
                         duration=video_info['total_duration'])

    # Markers
    fps_num = video_info['fps_num']
    # FPS thực tế = num / den (ví dụ 24000/1001 = 23.976)
    fps_real = video_info['fps_num'] / video_info['fps_den']

    for m in markers:
        # Chuyển giây sang ticks dựa trên tử số FPS (Timebase)
        # start_sec * fps_real sẽ sai nếu timebase là num. 
        # Chuẩn FCP: value = seconds * timebase_rate
        
        start_val = int(m['start'] * fps_num)
        dur_val = int(m['duration'] * fps_num)
        
        # Cộng thêm offset start của asset nếu có (để marker nằm đúng vị trí trên clip)
        # Tuy nhiên marker nằm TRONG clip nên tính relative từ 0 của clip (offset)
        # Trong FCPXML, marker start là relative với clip start.
        # Nếu clip start=30s, marker start=10s -> Marker nằm ở giây thứ 40 của source, nhưng giây thứ 10 của clip trên timeline.
        # Code cũ của bạn: marker start="0/24000s".
        # Đúng: marker start="12000/24000s" (0.5s kể từ đầu clip).
        
        # Lưu ý: Marker start tính từ đầu clip (0), không cộng asset_start.
        
        ET.SubElement(clip, "marker", 
                      start=f"{start_val}/{fps_num}s", 
                      duration=f"{dur_val}/{fps_num}s", 
                      value=f"[{m['label']}]", 
                      completed="0", 
                      note="AI Detected")
        
        # Keyword (Màu)
        color = "Red"
        if "noise" in m['label'].lower(): color = "Purple"
        
        ET.SubElement(clip, "keyword", 
                      start=f"{start_val}/{fps_num}s", 
                      duration=f"{dur_val}/{fps_num}s", 
                      value=f"AI-{m['label']}", 
                      note=color)

    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_str)
        
    return True, "Success"