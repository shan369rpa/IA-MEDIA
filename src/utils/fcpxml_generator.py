import xml.etree.ElementTree as ET
import os

class FCPXMLGenerator:
    def __init__(self, video_path, video_duration_seconds, frame_rate=60):
        self.video_path = os.path.abspath(video_path)
        self.duration_seconds = video_duration_seconds
        self.frame_rate = frame_rate
        self.markers = []

    def add_marker(self, start_seconds, label, note=""):
        """Thêm một marker vào danh sách chờ."""
        self.markers.append({
            "start": start_seconds,
            "label": label,
            "note": note
        })

    def _seconds_to_frame_str(self, seconds):
        """Chuyển đổi giây sang định dạng phân số của FCPXML (ví dụ: "3600/600s")."""
        total_frames = int(seconds * self.frame_rate * 100) # Nhân thêm hệ số để chính xác
        # FCPXML thường dùng mẫu số (timescale) là frame_rate * n
        timescale = self.frame_rate * 100
        return f"{total_frames}/{timescale}s"

    def generate_xml(self, output_path):
        """Tạo và lưu file .fcpxml."""
        
        # 1. Cấu trúc cơ bản
        fcpxml = ET.Element("fcpxml", version="1.9")
        resources = ET.SubElement(fcpxml, "resources")
        
        # 2. Định nghĩa Asset (File video gốc)
        # format="r1" là định dạng (sẽ định nghĩa sau hoặc FCP tự hiểu)
        asset_duration_str = self._seconds_to_frame_str(self.duration_seconds)
        asset = ET.SubElement(resources, "asset", id="r1", src=f"file://{self.video_path}", duration=asset_duration_str)
        
        # 3. Thư viện & Sự kiện
        library = ET.SubElement(fcpxml, "library")
        event = ET.SubElement(library, "event", name="AI Detected Errors")
        project = ET.SubElement(event, "project", name=f"Analysis: {os.path.basename(self.video_path)}")
        sequence = ET.SubElement(project, "sequence", duration=asset_duration_str)
        spine = ET.SubElement(sequence, "spine")
        
        # 4. Clip chính (Chứa các markers)
        # offset="0s" start="0s" duration=...
        asset_clip = ET.SubElement(spine, "asset-clip", ref="r1", offset="0s", name=os.path.basename(self.video_path), duration=asset_duration_str)
        
        # 5. Chèn Markers
        for m in self.markers:
            start_str = self._seconds_to_frame_str(m['start'])
            # Marker trong FCPXML: <marker start="..." duration="..." value="..." note="..."/>
            # value hiển thị như tên marker trên timeline
            ET.SubElement(asset_clip, "marker", start=start_str, duration="100/6000s", value=m['label'], note=m['note'])

        # 6. Lưu file
        # Lấy thư mục chứa file
        output_dir = os.path.dirname(output_path)

        # Kiểm tra và tạo thư mục nếu chưa có
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # Kiểm tra và tạo file nếu chưa có
        if not os.path.exists(output_path):
            with open(output_path, 'w',encoding="UTF-8") as f:
                # Nếu muốn tạo file rỗng hoặc thêm nội dung mặc định
                f.write("")  # Hoặc bạn có thể viết dữ liệu mặc định vào đây
                f.close()
        tree = ET.ElementTree(fcpxml)
        # Pretty print (thụt đầu dòng) để dễ đọc (tùy chọn)
        ET.indent(tree, space="    ", level=0)
        tree.write(output_path, encoding="UTF-8", xml_declaration=True)
        return output_path