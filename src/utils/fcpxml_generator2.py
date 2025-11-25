# src/utils/fcpxml_generator.py

import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

def create_fcpxml_with_markers(video_path, markers, output_path):
    """
    Tạo file FCPXML chứa video gốc và các To-Do Markers.
    
    Args:
        video_path: Đường dẫn file video raw.
        markers: List các dict {'start_sec', 'duration_sec', 'name', 'note'}
        output_path: Đường dẫn file xml đầu ra.
    """
    video_name = os.path.basename(video_path)
    fps = "25" # Tạm để 25, lý tưởng là lấy từ metadata video thật
    frame_duration = "100/2500s" # Tương ứng 25fps
    
    # Tạo cấu trúc XML cơ bản
    fcpxml = ET.Element("fcpxml", version="1.9")
    resources = ET.SubElement(fcpxml, "resources")
    format_elem = ET.SubElement(resources, "format", id="r1", name="FFVideoFormat1080p25", frameDuration=frame_duration, width="1920", height="1080")
    
    # Asset Video
    asset_id = "r2"
    asset = ET.SubElement(resources, "asset", id=asset_id, name=video_name, src=f"file://{os.path.abspath(video_path)}", start="0s", duration="3600s", hasVideo="1", hasAudio="1", format="r1")
    
    library = ET.SubElement(fcpxml, "library")
    event = ET.SubElement(library, "event", name="AI Detected Errors")
    project = ET.SubElement(event, "project", name=f"Checked_{video_name}")
    sequence = ET.SubElement(project, "sequence", duration="3600s", format="r1")
    spine = ET.SubElement(sequence, "spine")
    
    # Clip chính
    asset_clip = ET.SubElement(spine, "asset-clip", name=video_name, ref=asset_id, offset="0s", start="0s", duration="3600s")
    
    # Thêm Markers
    for m in markers:
        # Chuyển đổi giây sang định dạng phân số của FCPXML (ví dụ: giây * 2500 / 2500)
        # Để đơn giản, ta dùng dạng "Xs"
        start_str = f"{m['start_sec']}s"
        duration_str = f"{m.get('duration_sec', 0.5)}s"
        
        # Tạo marker note
        note = m.get('note', '')
        
        ET.SubElement(asset_clip, "marker", 
                      start=start_str, 
                      duration=duration_str, 
                      value=m['name'], 
                      completed="0", # 0 = To Do (Chưa xong)
                      note=note)

    # Lưu file
    xml_str = minidom.parseString(ET.tostring(fcpxml)).toprettyxml(indent="    ")
    with open(output_path, "w") as f:
        f.write(xml_str)
    
    return True