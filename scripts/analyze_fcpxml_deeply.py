# scripts/analyze_fcpxml_deeply.py

import os
import argparse
import xml.etree.ElementTree as ET
import logging
import json
from collections import defaultdict

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s', force=True)

# --- [MỚI] BỘ QUY TẮC PHÂN TÍCH ---
# Chúng ta định nghĩa "kiến thức" của mình về các thẻ ở đây
TAG_CLASSIFICATION = {
    # Core Structure
    "fcpxml": {"type": "Core Structure", "desc": "Thẻ gốc của tài liệu."},
    "resources": {"type": "Core Structure", "desc": "Khai báo tất cả các tài nguyên (assets, formats)."},
    "asset": {"type": "Core Structure", "desc": "Định nghĩa một file media (video, audio, image)."},
    "format": {"type": "Core Structure", "desc": "Định nghĩa một định dạng video (độ phân giải, frame rate)."},
    "library": {"type": "Core Structure", "desc": "Thư viện chứa các event và project."},
    "event": {"type": "Core Structure", "desc": "Một sự kiện, chứa các project và clip."},
    "project": {"type": "Core Structure", "desc": "Một project, chứa timeline chính."},
    "sequence": {"type": "Core Structure", "desc": "Timeline chính của project."},
    "spine": {"type": "Core Structure", "desc": "Trục chính của timeline, chứa các clip."},

    # Clip Types - Quan trọng cho Alignment
    "asset-clip": {"type": "Clip Type", "desc": "Clip cơ bản, trỏ đến file media gốc. Cốt lõi của Time Map."},
    "ref-clip": {"type": "Clip Type (Complex)", "desc": "Tham chiếu đến Compound Clip. Yêu cầu phân tích đệ quy."},
    "multicam": {"type": "Clip Type (Complex)", "desc": "Clip nhiều góc máy. Cần tìm angle được chọn."},
    "sync-clip": {"type": "Clip Type", "desc": "Clip đã được đồng bộ hóa audio/video."},
    "gap": {"type": "Clip Type", "desc": "Khoảng trống trên timeline. Dấu hiệu của một đoạn bị xóa."},

    # Audio Adjustments - Vàng!
    "adjust-volume": {"type": "Audio Adjustment", "desc": "Điều chỉnh âm lượng tổng thể của clip."},
    "filter-audio": {"type": "Audio Adjustment", "desc": "Áp dụng một hiệu ứng âm thanh."},
    "adjust-noiseReduction": {"type": "Audio Adjustment", "desc": "Hiệu ứng giảm nhiễu nền cụ thể."},
    "audio-channel-source": {"type": "Audio Adjustment", "desc": "Lựa chọn kênh audio (L/R/Stereo)."},
    
    # Audio Details
    "volume": {"type": "Audio Detail", "desc": "(Thẻ cũ) Điều chỉnh âm lượng, thường thấy trong các thẻ con."},
    "pan": {"type": "Audio Detail", "desc": "Điều chỉnh pan (vị trí âm thanh trái/phải)."},
    "balance": {"type": "Audio Detail", "desc": "Điều chỉnh balance cho âm thanh stereo."},

    # Video Adjustments
    "adjust-transform": {"type": "Video Adjustment", "desc": "Điều chỉnh vị trí, kích thước, xoay hình ảnh."},
    "filter-video": {"type": "Video Adjustment", "desc": "Áp dụng bộ lọc màu, hiệu ứng hình ảnh."},
    "video": {"type": "Video Adjustment", "desc": "Chứa các thông tin và hiệu ứng liên quan đến track video."},
    "transition": {"type": "Video Adjustment", "desc": "Hiệu ứng chuyển cảnh."},
    
    # Detailed Parameters
    "effect": {"type": "Detailed Parameter", "desc": "Định nghĩa một hiệu ứng cụ thể, là thẻ con của <filter-audio>."},
    "param": {"type": "Detailed Parameter", "desc": "Một tham số của effect, ví dụ: 'gain', 'frequency'."},
    "keyframe": {"type": "Detailed Parameter", "desc": "Một điểm neo thời gian cho animation (ví dụ: âm lượng giảm dần)."},
    "keyframeAnimation": {"type": "Detailed Parameter", "desc": "Chứa một chuỗi các keyframe."},

    # Metadata & Others
    "metadata": {"type": "Metadata", "desc": "Chứa các thẻ metadata con."},
    "md": {"type": "Metadata", "desc": "Một cặp key-value metadata."},
    "caption": {"type": "Metadata", "desc": "Phụ đề được nhúng."},
    "text": {"type": "Metadata", "desc": "Một lớp văn bản trên video."},
    # ... có thể thêm các thẻ khác vào đây nếu phát hiện
}
DEFAULT_CLASSIFICATION = {"type": "Unknown", "desc": "Thẻ chưa được định nghĩa trong bộ quy tắc."}


def fcpxml_time_to_seconds(time_str: str) -> float | None:
    """Chuyển đổi định dạng thời gian của FCPXML thành giây."""
    if not time_str or 's' not in time_str:
        return None
    time_str = time_str.replace('s', '')
    try:
        if '/' in time_str:
            num, den = map(int, time_str.split('/'))
            return num / den
        return float(time_str)
    except (ValueError, ZeroDivisionError):
        return None

def analyze_fcpxml(file_path: str) -> tuple[dict, list, list]:
    """
    Phân tích sâu một file FCPXML, trả về 3 thành phần:
    1. Thống kê thẻ.
    2. Time Map.
    3. Danh sách sự kiện chỉnh sửa.
    """
    tag_inventory = defaultdict(lambda: {"count": 0, "example_attributes": {}})
    time_map = []
    audio_events = []
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 1. Quét toàn bộ file để thống kê thẻ (inventory)
    for elem in root.iter():
        tag_inventory[elem.tag]["count"] += 1
        if not tag_inventory[elem.tag]["example_attributes"]:
            # Lấy ví dụ thuộc tính của lần xuất hiện đầu tiên
            tag_inventory[elem.tag]["example_attributes"] = elem.attrib

    # 2. Quét timeline chính để lấy Time Map và Sự kiện chỉnh sửa
    for clip in root.findall(".//spine/*"): # Lấy tất cả các con của spine
        
        # --- XỬ LÝ TIME MAP (từ asset-clip) ---
        if clip.tag == 'asset-clip':
            offset = fcpxml_time_to_seconds(clip.get('offset', '0s'))
            duration = fcpxml_time_to_seconds(clip.get('duration'))
            start = fcpxml_time_to_seconds(clip.get('start'))
            if all(x is not None for x in [offset, duration, start]):
                time_map.append({
                    "type": "asset-clip",
                    "edited_start": offset,
                    "edited_end": offset + duration,
                    "raw_start": start
                })
        
        # --- XỬ LÝ SỰ KIỆN CHỈNH SỬA ---
        # Tìm tất cả các thẻ chỉnh sửa âm thanh bên trong clip này
        for adjustment in clip.iter():
            event = None
            
            if adjustment.tag == 'adjust-volume':
                amount = adjustment.get('amount', '0dB')
                event = {
                    "type": "volume_adjustment",
                    "value": amount,
                    "start": fcpxml_time_to_seconds(clip.get('offset', '0s')),
                    "end": fcpxml_time_to_seconds(clip.get('offset', '0s')) + fcpxml_time_to_seconds(clip.get('duration'))
                }
            
            elif adjustment.tag == 'filter-audio':
                effect_name = adjustment.get('name', 'Unknown Filter')
                effect_id = adjustment.get('ref') # ref="r3"
                # Tìm thẻ effect tương ứng trong resources để lấy tên chính xác
                effect_def = root.find(f".//effect[@id='{effect_id}']")
                if effect_def is not None:
                    effect_name = effect_def.get('name', effect_name)
                
                event = {
                    "type": "audio_filter",
                    "value": effect_name,
                    "start": fcpxml_time_to_seconds(clip.get('offset', '0s')),
                    "end": fcpxml_time_to_seconds(clip.get('offset', '0s')) + fcpxml_time_to_seconds(clip.get('duration'))
                }

            # --- [ĐẶC BIỆT] BÓC TÁCH NOISE REDUCTION ---
            elif adjustment.tag == 'adjust-noiseReduction':
                amount = adjustment.find("param[@name='amount']")
                if amount is not None:
                    amount_value = amount.get('value', '0') # 0 to 1
                else:
                    amount_value = 'N/A'

                event = {
                    "type": "noise_reduction",
                    "value": f"amount={amount_value}",
                    "start": fcpxml_time_to_seconds(clip.get('offset', '0s')),
                    "end": fcpxml_time_to_seconds(clip.get('offset', '0s')) + fcpxml_time_to_seconds(clip.get('duration'))
                }

            if event:
                audio_events.append(event)

    time_map.sort(key=lambda x: x['edited_start'])
    return tag_inventory, time_map, audio_events


def generate_inventory_report(tag_inventory: dict, file_name: str, source_dir: str) -> str:
    """Tạo báo cáo Markdown từ kết quả thống kê thẻ."""
    report_lines = [
        f"# FCPXML Tag Inventory: `{file_name}`",
        f"This report lists all unique XML tags found in the specified FCPXML file.",
        f"*Báo cáo này liệt kê tất cả các thẻ XML duy nhất được tìm thấy trong file FCPXML được chỉ định.*\n",
        "| Tag Name / Tên Thẻ | Type / Phân Loại | Description / Mô tả | Count / Số lần XH | Example Attributes / Ví dụ Thuộc tính |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]
    sorted_tags = sorted(tag_inventory.keys())
    for tag in sorted_tags:
        info = TAG_CLASSIFICATION.get(tag, DEFAULT_CLASSIFICATION)
        count = tag_inventory[tag]['count']
        attrs = ' '.join([f'{k}="{v}"' for k, v in tag_inventory[tag]['example_attributes'].items()])
        report_lines.append(f"| `{tag}` | **{info['type']}** | {info['desc']} | {count} | `{attrs}` |")
    return "\n".join(report_lines)

def main():
    parser = argparse.ArgumentParser(description="Phân tích sâu file FCPXML và xuất ra báo cáo và dữ liệu JSON.")
    parser.add_argument("fcpxml_path", type=str, help="Đường dẫn đến file FCPXML cần phân tích.")
    parser.add_argument("-o", "--output_dir", type=str, default="fcpxml_analysis", help="Thư mục để lưu kết quả phân tích.")
    
    args = parser.parse_args()

    if not os.path.exists(args.fcpxml_path):
        logging.error(f"File không tồn tại: {args.fcpxml_path}")
        return

    session_id = os.path.splitext(os.path.basename(args.fcpxml_path))[0]
    session_output_dir = os.path.join(args.output_dir, session_id)
    os.makedirs(session_output_dir, exist_ok=True)
    
    logging.info(f"Bắt đầu phân tích sâu file: {args.fcpxml_path}")
    tag_inventory, time_map, audio_events = analyze_fcpxml(args.fcpxml_path)

    # 1.1: Tạo báo cáo thống kê thẻ
    inventory_report_path = os.path.join(session_output_dir, "FCPXML_TAG_INVENTORY.md")
    report_content = generate_inventory_report(tag_inventory, os.path.basename(args.fcpxml_path), os.path.dirname(args.fcpxml_path))
    with open(inventory_report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    logging.info(f"Đã lưu báo cáo thống kê thẻ tại: {inventory_report_path}")

    # 1.2: Xuất dữ liệu Time Map và Sự kiện chỉnh sửa ra file JSON
    output_data = {
        "time_map": time_map,
        "audio_events": audio_events
    }
    json_output_path = os.path.join(session_output_dir, "analysis_data.json")
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    logging.info(f"Đã lưu Time Map và Audio Events tại: {json_output_path}")
    
    logging.info("Phân tích hoàn tất.")


if __name__ == "__main__":
    main()