# src/utils/fcpxml_generator.py

import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import logging
from datetime import datetime

# --- [MỚI] Định nghĩa màu sắc và từ khóa cho từng loại lỗi ---
# Final Cut Pro hỗ trợ các màu: Blue, Red, Green, Yellow, Orange, Purple, Pink, Gray
ERROR_STYLES = {
    "PRONUNCIATION": {"color": "Orange", "keyword": "AI-Pronunciation"},
    "CLIPPING":      {"color": "Red",    "keyword": "AI-Clipping"},
    "NOISE_SPIKE":   {"color": "Purple", "keyword": "AI-Noise"},
    "LOW_VOLUME":    {"color": "Blue",   "keyword": "AI-Volume"},
    "AUDIO":         {"color": "Yellow", "keyword": "AI-Audio-General"}, # Lỗi chung
    # Thêm các loại lỗi khác ở đây
}
DEFAULT_STYLE = ERROR_STYLES["AUDIO"]

def _pretty_print_xml(root_element):
    """Định dạng lại cây XML cho dễ đọc."""
    rough_string = ET.tostring(root_element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_fcpxml_with_markers(
    output_path: str,
    video_path: str,
    video_duration_sec: float,
    markers_list: list
) -> bool:
    """
    Tạo một file FCPXML chứa clip video và ghim các To-Do Marker đã được tô màu và gắn từ khóa.
    """
    try:
        logging.info(f"Đang tạo file FCPXML tại: {output_path}")
        video_name = os.path.basename(video_path)
        video_duration_str = f"{int(video_duration_sec * 600)}/600s"

        fcpxml = ET.Element("fcpxml", version="1.10") # Nâng version lên để hỗ trợ keywords
        
        resources = ET.SubElement(fcpxml, "resources")
        format_id = "r1"
        ET.SubElement(resources, "format", id=format_id, name="FFVideoFormat1080p25", frameDuration="1/25s", width="1920", height="1080")
        asset_id = "r2"
        asset_src = f"file://{os.path.abspath(video_path)}".replace("\\", "/")
        ET.SubElement(resources, "asset", id=asset_id, name=video_name, src=asset_src, start="0s", duration=video_duration_str, hasVideo="1", hasAudio="1", format=format_id)

        library = ET.SubElement(fcpxml, "library")
        event_name = f"AI Analysis - {datetime.now().strftime('%Y-%m-%d')}"
        event = ET.SubElement(library, "event", name=event_name)
        
        # --- [MỚI] Thêm các Keyword vào Event để FCP có thể nhận diện ---
        for style in ERROR_STYLES.values():
            ET.SubElement(event, "keyword", name=style["keyword"], start="0s", duration=video_duration_str)

        project_name = f"AI Errors for {video_name}"
        project = ET.SubElement(event, "project", name=project_name)
        
        sequence = ET.SubElement(project, "sequence", duration=video_duration_str, format=format_id)
        spine = ET.SubElement(sequence, "spine")

        # Thêm Clip video chính
        main_clip = ET.SubElement(spine, "asset-clip", ref=asset_id, name=video_name, offset="0s", duration=video_duration_str)

        logging.info(f"Đang thêm {len(markers_list)} marker vào timeline...")
        for i, marker_info in enumerate(markers_list):
            start_sec = marker_info.get('start_sec', 0)
            duration_sec = marker_info.get('duration_sec', 0.2)
            word = marker_info.get('word', '')
            error_type = marker_info.get('error_type', 'AUDIO') # Ví dụ: 'CLIPPING'
            
            style = ERROR_STYLES.get(error_type, DEFAULT_STYLE)
            color = style["color"]
            keyword = style["keyword"]

            # --- [MỚI] Tạo nội dung marker chi tiết hơn ---
            marker_text = f"Lỗi {error_type.lower()} tại từ: '{word}'"

            start_str = f"{int(start_sec * 600)}/600s"
            duration_str = f"{int(duration_sec * 600)}/600s"
            
            # Marker giờ được gắn vào `asset-clip` thay vì `spine` để có màu
            marker_node = ET.SubElement(main_clip, "marker", 
                                        start=start_str, 
                                        duration=duration_str, 
                                        value=marker_text, 
                                        completed="0",
                                        note=f"Marker ID: {i+1}") # Thêm ID để truy vết feedback
            
            # --- [MỚI] Gắn Keyword vào Marker để tô màu ---
            # Cấu trúc hơi phức tạp: <marker> chứa <keyword>
            ET.SubElement(marker_node, "keyword", start=start_str, duration=duration_str, value=keyword, note=color)

        # Ghi file
        xml_content = _pretty_print_xml(fcpxml)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml_content)
        
        logging.info("Tạo file FCPXML nâng cao thành công.")
        return True

    except Exception as e:
        logging.error(f"Lỗi khi tạo file FCPXML: {e}", exc_info=True)
        return False