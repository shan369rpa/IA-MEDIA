# scripts/batch_analyze_fcpxml.py

import os
import argparse
import xml.etree.ElementTree as ET
import logging
import json
from collections import defaultdict, Counter

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s', force=True)

# --- BỘ QUY TẮC PHÂN TÍCH ---
# Định nghĩa "kiến thức" của chúng ta về các thẻ FCPXML
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

    # Clip Types
    "asset-clip": {"type": "Clip Type", "desc": "Clip media cơ bản, trỏ đến file media gốc."},
    "ref-clip": {"type": "Clip Type (Complex)", "desc": "Tham chiếu đến Compound Clip (cấu trúc lồng nhau)."},
    "multicam": {"type": "Clip Type (Complex)", "desc": "Clip nhiều góc máy."},
    "sync-clip": {"type": "Clip Type", "desc": "Clip đã được đồng bộ hóa audio/video."},
    "gap": {"type": "Clip Type", "desc": "Khoảng trống trên timeline, dấu hiệu của một đoạn bị xóa."},
    "clip": {"type": "Clip Type", "desc": "Một clip chung, thường là container cho các clip khác."},
    "video": {"type": "Clip Type", "desc": "Một clip chỉ chứa video (ví dụ: logo, title)."},
    "title": {"type": "Clip Type", "desc": "Một clip chứa hiệu ứng text/title."},

    # Audio Adjustments
    "adjust-EQ": {"type": "Audio Adjustment", "desc": "Áp dụng hiệu ứng Equalizer."},
    "adjust-humReduction": {"type": "Audio Adjustment", "desc": "Giảm tiếng ù điện (50/60Hz)."},
    "adjust-loudness": {"type": "Audio Adjustment", "desc": "Điều chỉnh độ lớn tổng thể (Loudness)."},
    "adjust-noiseReduction": {"type": "Audio Adjustment", "desc": "Hiệu ứng giảm nhiễu nền."},
    "adjust-panner": {"type": "Audio Adjustment", "desc": "Điều chỉnh Panner (âm thanh nổi trái/phải)."},
    "adjust-voiceIsolation": {"type": "Audio Adjustment", "desc": "Tính năng cách ly giọng nói."},
    "adjust-volume": {"type": "Audio Adjustment", "desc": "Điều chỉnh âm lượng tổng thể của clip."},
    "filter-audio": {"type": "Audio Adjustment", "desc": "Áp dụng một hiệu ứng âm thanh chung."},
    "audio-channel-source": {"type": "Audio Detail", "desc": "Lựa chọn kênh audio (L/R/Stereo)."},
    
    # Audio Details
    "fadeIn": {"type": "Audio Detail", "desc": "Hiệu ứng âm thanh vào (Fade In)."},
    "fadeOut": {"type": "Audio Detail", "desc": "Hiệu ứng âm thanh ra (Fade Out)."},

    # Video Adjustments
    "adjust-colorConform": {"type": "Video Adjustment", "desc": "Tự động điều chỉnh màu sắc."},
    "adjust-transform": {"type": "Video Adjustment", "desc": "Điều chỉnh vị trí, kích thước, xoay hình ảnh."},
    "filter-video": {"type": "Video Adjustment", "desc": "Áp dụng bộ lọc màu, hiệu ứng hình ảnh."},
    "transition": {"type": "Video Adjustment", "desc": "Hiệu ứng chuyển cảnh."},
    "conform-rate": {"type": "Video Adjustment", "desc": "Điều chỉnh frame rate của clip cho khớp timeline."},

    # Detailed Parameters
    "effect": {"type": "Detailed Parameter", "desc": "Định nghĩa một hiệu ứng cụ thể."},
    "param": {"type": "Detailed Parameter", "desc": "Một tham số của effect (ví dụ: 'gain', 'frequency')."},
    "keyframe": {"type": "Detailed Parameter", "desc": "Một điểm neo thời gian cho animation (ví dụ: âm lượng)."},
    "keyframeAnimation": {"type": "Detailed Parameter", "desc": "Chứa một chuỗi các keyframe."},

    # Metadata & Others
    "metadata": {"type": "Metadata", "desc": "Chứa các thẻ metadata con."},
    "md": {"type": "Metadata", "desc": "Một cặp key-value metadata."},
    "caption": {"type": "Metadata", "desc": "Phụ đề được nhúng."},
    "text": {"type": "Metadata", "desc": "Một lớp văn bản trên video."},
    "text-style-def": {"type": "Metadata", "desc": "Định nghĩa một style cho text."},
    "text-style": {"type": "Metadata", "desc": "Áp dụng một style cho text."},
    "bookmark": {"type": "Metadata", "desc": "Dấu trang do editor đặt."},
    "keyword": {"type": "Metadata", "desc": "Từ khóa được gán cho clip."},
    "rating": {"type": "Metadata", "desc": "Đánh dấu yêu thích/từ chối cho clip."},
    "media-rep": {"type": "Metadata", "desc": "Đại diện cho một file media vật lý (gốc, proxy)."},
    "data": {"type": "Metadata", "desc": "Chứa dữ liệu nhị phân hoặc cấu hình cho thẻ cha."},
    "array": {"type": "Metadata", "desc": "Một mảng các giá trị."},
    "string": {"type": "Metadata", "desc": "Một giá trị chuỗi."},

    # Project Organization
    "smart-collection": {"type": "Project Organization", "desc": "Một bộ sưu tập thông minh tự động nhóm clip."},
    "keyword-collection": {"type": "Project Organization", "desc": "Một bộ sưu tập nhóm clip theo từ khóa."},
    "match-clip": {"type": "Project Organization", "desc": "Quy tắc lọc cho collection."},
    "match-media": {"type": "Project Organization", "desc": "Quy tắc lọc cho collection."},
    "match-ratings": {"type": "Project Organization", "desc": "Quy tắc lọc cho collection."},
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

def analyze_single_fcpxml(file_path: str, session_id: str) -> dict:
    """Phân tích một file FCPXML và trả về dữ liệu có cấu trúc."""
    analysis = {
        "session_id": session_id,
        "tags": defaultdict(lambda: {"count": 0, "examples": []}),
        "audio_events": []
    }
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 1. Thống kê tất cả các thẻ
    for elem in root.iter():
        tag = elem.tag
        analysis["tags"][tag]["count"] += 1
        # Chỉ lưu ví dụ thuộc tính cho 3 lần xuất hiện đầu tiên để tránh quá tải
        if len(analysis["tags"][tag]["examples"]) < 3:
             analysis["tags"][tag]["examples"].append(elem.attrib)

    # 2. Trích xuất các sự kiện chỉnh sửa âm thanh từ timeline chính
    for clip in root.findall(".//spine/*"):
        start_time = fcpxml_time_to_seconds(clip.get('offset', '0s'))
        duration = fcpxml_time_to_seconds(clip.get('duration'))
        if start_time is None or duration is None:
            continue
        end_time = start_time + duration

        if clip.tag == 'gap':
            analysis['audio_events'].append({
                "session_id": session_id, "type": "gap", "start": start_time, "end": end_time, 
                "duration": duration, "details": {}
            })
            
        # Quét tất cả các thẻ con bên trong một clip để tìm sự kiện audio
        for child in clip.iter():
            event = {"session_id": session_id, "start": start_time, "end": end_time}
            tag = child.tag
            
            # Xử lý các thẻ điều chỉnh trực tiếp (adjust-*)
            if tag.startswith('adjust-') and 'audio' in tag.lower():
                event["type"] = tag.replace('adjust-', '')
                event["details"] = child.attrib
                analysis['audio_events'].append(event)

            # Xử lý các thẻ filter-audio
            elif tag == 'filter-audio':
                effect_id = child.get('ref')
                effect_def = root.find(f".//effect[@id='{effect_id}']")
                if effect_def is not None:
                    event["type"] = "audio_filter"
                    event["details"] = {"name": effect_def.get('name')}
                    analysis['audio_events'].append(event)
            
            # Xử lý fade in/out
            elif tag in ['fadeIn', 'fadeOut']:
                event["type"] = tag.lower()
                event["details"] = child.attrib
                fade_duration = fcpxml_time_to_seconds(child.get('duration'))
                if fade_duration is not None:
                    if tag == 'fadeIn':
                        event["end"] = start_time + fade_duration
                    else: # fadeOut
                        event["start"] = end_time - fade_duration
                analysis['audio_events'].append(event)
            
            # Phân tích keyframe âm lượng (thường nằm trong thẻ param có name='D-B')
            elif tag == 'param' and child.get('name') == 'D-B':
                for kf in child.findall("keyframe"):
                    kf_time = fcpxml_time_to_seconds(kf.get('time'))
                    kf_value = kf.get('value', '0dB')
                    if kf_time is not None:
                        analysis['audio_events'].append({
                           "session_id": session_id,
                           "type": "volume_keyframe",
                           "start": kf_time, "end": kf_time, # Keyframe là một điểm thời gian
                           "details": {"value": kf_value}
                        })
                        
    return analysis

def generate_report(all_analyses: list, output_file_name: str):
    """Tạo báo cáo Markdown từ dữ liệu phân tích tổng hợp."""
    md_path = f"{output_file_name}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Báo cáo Phân tích FCPXML - {output_file_name}\n\n")
        f.write(f"- **Tổng số file FCPXML đã phân tích:** {len(all_analyses)}\n")
        f.write("- **Danh sách Session ID:**\n")
        for analysis in all_analyses:
            f.write(f"  - `{analysis['session_id']}`\n")
        f.write("\n---\n")
        
        # Thống kê tần suất thẻ
        overall_tag_counter = Counter()
        files_containing_tag = defaultdict(int)
        for analysis in all_analyses:
            for tag, data in analysis['tags'].items():
                overall_tag_counter[tag] += data['count']
                files_containing_tag[tag] += 1
        
        f.write("## 2. Thống kê Tần suất Thẻ trên Toàn bộ các File\n\n")
        f.write("| Tag Name | Tổng số lần XH | Số File có Chứa Thẻ này |\n")
        f.write("| :--- | :--- | :--- |\n")
        for tag, count in sorted(overall_tag_counter.items()):
            f.write(f"| `{tag}` | {count} | {files_containing_tag[tag]}/{len(all_analyses)} |\n")
        f.write("\n---\n")

        # Phân tích chuyên sâu các sự kiện audio
        f.write("## 3. Phân tích Chuyên sâu theo Từng Loại Chỉnh sửa Âm thanh\n\n")
        event_summary = defaultdict(list)
        for analysis in all_analyses:
            for event in analysis['audio_events']:
                event_summary[event['type']].append(event)

        for i, (event_type, events) in enumerate(sorted(event_summary.items())):
            f.write(f"### 3.{i + 1}. {event_type}\n")
            unique_sessions = len(set(e.get('session_id') for e in events))
            f.write(f"- **Tần suất:** Xuất hiện **{len(events)}** lần trong **{unique_sessions}/{len(all_analyses)}** file.\n")
            
            # Tính toán thống kê thời lượng nếu có
            durations = [e['end'] - e['start'] for e in events if 'end' in e and 'start' in e]
            if durations:
                avg_duration = sum(durations) / len(durations) if durations else 0
                f.write(f"- **Thời lượng trung bình:** {avg_duration:.2f} giây.\n")
            
            # Lấy ví dụ từ event đầu tiên
            if events:
                f.write(f"- **Ví dụ (từ `{events[0]['session_id']}`):**\n  ```json\n  {json.dumps(events, indent=2, ensure_ascii=False)}\n  ```\n")

    logging.info(f"Đã lưu báo cáo Markdown tại: {md_path}")

def main():
    parser = argparse.ArgumentParser(description="Phân tích hàng loạt file FCPXML và tạo báo cáo tổng hợp.")
    parser.add_argument("source_dir", type=str, help="Thư mục gốc chứa các session (đã được sắp xếp theo cấu trúc chuẩn).")
    parser.add_argument("output_file_name", type=str, help="Tên file cho báo cáo (ví dụ: FCPXML_ANALYSIS_BATCH_1).")
    
    args = parser.parse_args()
    
    all_analyses = []
    
    # Duyệt qua các thư mục session trong source_dir
    for session_id in os.listdir(args.source_dir):
        session_path = os.path.join(args.source_dir, session_id)
        if os.path.isdir(session_path):
            # Tìm file FCPXML theo quy ước
            fcpxml_path = os.path.join(session_path, f"{session_id}.fcpxml")
            
            if os.path.exists(fcpxml_path):
                logging.info(f"Đang phân tích: {session_id}")
                try:
                    analysis = analyze_single_fcpxml(fcpxml_path, session_id)
                    all_analyses.append(analysis)
                except Exception as e:
                    logging.error(f"Lỗi không thể xử lý file {fcpxml_path}: {e}")
            else:
                logging.warning(f"Bỏ qua '{session_id}' vì không tìm thấy file '{session_id}.fcpxml'.")
    
    if not all_analyses:
        logging.error("Không phân tích được file FCPXML nào.")
        return

    # Tạo báo cáo
    generate_report(all_analyses, args.output_file_name)

    # Lưu dữ liệu JSON chi tiết
    json_path = f"{args.output_file_name}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_analyses, f, indent=2, ensure_ascii=False)
    logging.info(f"Đã lưu dữ liệu JSON chi tiết tại: {json_path}")

if __name__ == "__main__":
    main()