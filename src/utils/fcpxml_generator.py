# src/utils/fcpxml_generator.py

import xml.etree.ElementTree as ET
from xml.dom import minidom
import logging
import os

class FCPXMLGenerator:
    def __init__(self, video_path: str, video_duration_sec: float):
        self.video_path = os.path.abspath(video_path)
        self.duration_sec = video_duration_sec
        self.frame_rate = 24 # Mặc định, nên lấy từ mediainfo nếu có thể
        self.timebase = 2400 # Timebase chuẩn của FCP (ví dụ 24fps * 100)

    def _sec_to_fcptime(self, seconds: float) -> str:
        """Chuyển giây sang định dạng phân số của FCPXML (vd: 1200/2400s)."""
        value = int(seconds * self.timebase)
        return f"{value}/{self.timebase}s"

    def generate(self, markers: list, output_path: str):
        """
        Tạo file FCPXML chứa các markers.
        markers: List các dict {'start': float, 'name': str, 'note': str}
        """
        try:
            # 1. Cấu trúc gốc
            root = ET.Element("fcpxml", version="1.9")
            
            # 2. Resources (Định nghĩa file video gốc)
            resources = ET.SubElement(root, "resources")
            format_id = "r1"
            # Định nghĩa format video
            ET.SubElement(resources, "format", id=format_id, width="1920", height="1080", 
                          frameDuration=self._sec_to_fcptime(1/self.frame_rate))
            
            # Định nghĩa asset (file video)
            asset_id = "r2"
            duration_fcp = self._sec_to_fcptime(self.duration_sec)
            ET.SubElement(resources, "asset", id=asset_id, name=os.path.basename(self.video_path), 
                          src=f"file://{self.video_path}", start="0s", duration=duration_fcp, hasVideo="1", format=format_id)

            # 3. Library / Event / Project Structure
            library = ET.SubElement(root, "library")
            event = ET.SubElement(library, "event", name="AI Detected Errors")
            project = ET.SubElement(event, "project", name="Error Review Timeline")
            sequence = ET.SubElement(project, "sequence", duration=duration_fcp, format=format_id, tcStart="0s", tcFormat="NDF")
            spine = ET.SubElement(sequence, "spine")

            # 4. Clip chính (Chứa video và các marker)
            asset_clip = ET.SubElement(spine, "asset-clip", name=os.path.basename(self.video_path), 
                                       ref=asset_id, duration=duration_fcp, start="0s", offset="0s")

            # 5. Thêm Markers vào trong Clip
            for m in markers:
                start_seconds = m.get('start', 0)
                marker_name = m.get('name', 'AI Marker')
                marker_note = m.get('note', 'Auto detected by IA MEDIA')
                
                # duration của marker (cho To-Do marker thì không cần thiết lắm, nhưng có thể để nhỏ)
                # Quan trọng: completed="0" biến nó thành To-Do Marker
                ET.SubElement(asset_clip, "marker", 
                              start=self._sec_to_fcptime(start_seconds), 
                              duration="1/2400s", 
                              value=marker_name, 
                              completed="0", 
                              note=marker_note)

            # 6. Xuất ra file đẹp
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(xml_str)
            
            logging.info(f"Đã tạo FCPXML thành công tại: {output_path}")
            return True

        except Exception as e:
            logging.exception(f"Lỗi khi tạo FCPXML: {e}")
            return False