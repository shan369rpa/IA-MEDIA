# src/utils/fcpxml_parser.py

import argparse
import json
import os
import xml.etree.ElementTree as ET
import logging
from collections import defaultdict

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s', force=True)

def fcpxml_time_to_seconds(time_str: str) -> float | None:
    """Chuyển đổi định dạng thời gian của FCPXML (ví dụ: "36036/600s" hoặc "10s") thành giây."""
    if not time_str or 's' not in time_str:
        # Xử lý trường hợp không có đơn vị 's', ví dụ trong keyframe
        parts = time_str.split('/')
        if len(parts) == 2:
            try:
                return int(parts[0]) / int(parts[1])
            except (ValueError, ZeroDivisionError):
                return None
        return None
    
    time_str = time_str.replace('s', '')
    try:
        if '/' in time_str:
            num, den = map(int, time_str.split('/'))
            return num / den
        return float(time_str)
    except (ValueError, ZeroDivisionError):
        return None

def extract_events_and_map(file_path: str) -> dict:
    """
    Phân tích sâu một file FCPXML, trích xuất Time Map và danh sách chi tiết các Sự kiện Chỉnh sửa.

    Args:
        file_path (str): Đường dẫn đến file FCPXML.

    Returns:
        dict: Một dictionary chứa 'time_map' và 'edit_events'.
    """
    logging.info(f"Bắt đầu phân tích sâu file FCPXML: {os.path.basename(file_path)}")
    results = {
        "time_map": [],
        "edit_events": []
    }
    
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        logging.error(f"Lỗi cú pháp XML: {e}")
        return results

    # Duyệt qua tất cả các clip trên timeline chính
    for clip in root.findall(".//spine/*"):
        
        clip_offset = fcpxml_time_to_seconds(clip.get('offset', '0s'))
        clip_duration = fcpxml_time_to_seconds(clip.get('duration'))
        
        if clip_offset is None or clip_duration is None:
            continue
            
        clip_end = clip_offset + clip_duration

        # --- 1. XỬ LÝ TIME MAP VÀ CÁC SỰ KIỆN GẮN LIỀN VỚI CLIP ---
        if clip.tag == 'asset-clip':
            raw_start = fcpxml_time_to_seconds(clip.get('start'))
            if raw_start is not None:
                results["time_map"].append({
                    "type": "asset-clip",
                    "edited_start": clip_offset,
                    "edited_end": clip_end,
                    "raw_start": raw_start
                })

            # --- 2. QUÉT TẤT CẢ CÁC THẺ CON BÊN TRONG CLIP ĐỂ TÌM SỰ KIỆN ---
            for child in clip.iter():
                event = {"start": clip_offset, "end": clip_end, "source_tag": child.tag}

                # Nhóm các thẻ 'adjust-*'
                if child.tag.startswith('adjust-'):
                    event_type = child.tag.replace('adjust-', '').lower() # vd: 'volume', 'noisereduction'
                    event["type"] = event_type
                    event["details"] = child.attrib
                    results['edit_events'].append(event)
                
                # Nhóm các thẻ 'filter-*'
                elif child.tag == 'filter-audio':
                    effect_id = child.get('ref')
                    effect_def = root.find(f".//effect[@id='{effect_id}']")
                    if effect_def is not None:
                        event["type"] = "audio_filter"
                        event["details"] = {"name": effect_def.get('name', 'Unknown'), **child.attrib}
                        results['edit_events'].append(event)
                
                # Nhóm các thẻ fade in/out
                elif child.tag in ['fadeIn', 'fadeOut']:
                    event["type"] = child.tag.lower()
                    event["details"] = child.attrib
                    fade_duration = fcpxml_time_to_seconds(child.get('duration'))
                    if fade_duration is not None:
                        if child.tag == 'fadeIn':
                            event["end"] = clip_offset + fade_duration
                        else: # fadeOut
                            event["start"] = clip_end - fade_duration
                    results['edit_events'].append(event)
                
                # Phân tích sâu keyframe âm lượng
                elif child.tag == 'param' and child.get('name') == 'D-B':
                    for kf in child.findall("keyframe"):
                        kf_time_str = kf.get('time')
                        kf_value = kf.get('value', '0dB')
                        kf_time = fcpxml_time_to_seconds(kf_time_str)
                        
                        if kf_time is not None:
                            kf_event = {
                                "start": kf_time, "end": kf_time, # Keyframe là một điểm
                                "source_tag": "keyframe",
                                "type": "volume_keyframe",
                                "details": {"value": kf_value}
                            }
                            # Phân loại chi tiết hơn
                            if kf_value == '-96dB':
                                kf_event["type"] = "volume_mute_keyframe"
                            elif kf_value.startswith('-'):
                                kf_event["type"] = "volume_decrease_keyframe"
                            elif float(kf_value.replace('dB', '')) > 0:
                                kf_event["type"] = "volume_increase_keyframe"

                            results['edit_events'].append(kf_event)

        # --- 3. XỬ LÝ CÁC THẺ KHÔNG PHẢI CLIP ---
        elif clip.tag == 'gap':
            results['edit_events'].append({
                "start": clip_offset, "end": clip_end,
                "source_tag": "gap", "type": "deleted_segment",
                "details": {"duration": clip_duration}
            })

    # Sắp xếp lại để dễ xử lý
    results["time_map"].sort(key=lambda x: x['edited_start'])
    results["edit_events"].sort(key=lambda x: x['start'])
    
    logging.info(f"Phân tích hoàn tất. Tìm thấy {len(results['time_map'])} clip và {len(results['edit_events'])} sự kiện chỉnh sửa.")
    
    return results

if __name__ == '__main__':
    # --- Phần Test Nhanh ---
    parser = argparse.ArgumentParser(description="Test FCPXML Event Extractor.")
    parser.add_argument("fcpxml_path", type=str, help="Đường dẫn đến file FCPXML để test.")
    args = parser.parse_args()

    if os.path.exists(args.fcpxml_path):
        analysis_data = extract_events_and_map(args.fcpxml_path)
        
        # In ra một vài kết quả để kiểm tra
        print("\n--- TIME MAP (First 3) ---")
        print(json.dumps(analysis_data["time_map"][:3], indent=2))
        
        print("\n--- EDIT EVENTS (First 10) ---")
        print(json.dumps(analysis_data["edit_events"][:10], indent=2, ensure_ascii=False))

        # Lưu toàn bộ kết quả ra file JSON
        output_path = "fcpxml_parser_test_output.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        print(f"\nĐã lưu toàn bộ kết quả phân tích vào: {output_path}")

    else:
        print(f"File không tồn tại: {args.fcpxml_path}")