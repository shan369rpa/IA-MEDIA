Đây là bước chuyển mình quan trọng: từ **Giai đoạn "Học" (Training/Ingestion)** sang **Giai đoạn "Suy luận" (Inference/Detection)**.

Chúng ta sẽ xây dựng một module mới tên là `detector`. Module này sẽ không cần file `blocked` hay `edited` để đối chiếu nữa. Nó sẽ "tự thân vận động" bằng cách so sánh với kiến thức đã lưu trong Vector DB.

Dưới đây là kiến trúc và mã nguồn chi tiết để thực hiện việc này.

---

### **Kiến trúc Module Phát hiện Lỗi (`Detector`)**

1.  **Input:** 1 File Video Raw (chưa chỉnh sửa).
2.  **Process:**
    *   **Bước 1 (Processing):** Trích xuất Audio $\rightarrow$ Whisper $\rightarrow$ Lấy timestamp từng từ $\rightarrow$ Cắt audio chunk tạm.
    *   **Bước 2 (Vectorization):** Tạo vector embedding cho chunk từ đó (Ví dụ: từ "pháp").
    *   **Bước 3 (Retrieval - RAG):** Truy vấn DB: *"Lấy cho tôi các mẫu vector của từ 'pháp' đã lưu. So sánh xem vector mới này giống phiên bản 'clean' hơn hay giống phiên bản 'error' hơn?"*
    *   **Bước 4 (Decision):**
        *   Nếu giống `error` hơn $\rightarrow$ **Gán nhãn Lỗi**.
        *   Nếu khoảng cách đến `clean` quá quá xa (vượt ngưỡng) $\rightarrow$ **Gán nhãn Bất thường (Anomaly)**.
3.  **Output:** File `project.fcpxml` chứa danh sách To-Do markers.

---

### **Triển khai Chi tiết**

#### **Bước 1: Cập nhật `src/database/db_manager.py`**

Chúng ta cần một hàm để truy vấn so sánh. Logic ở đây là: Với một từ (ví dụ "hạnh"), hãy tìm xem trong quá khứ, cách phát âm này gần với các mẫu "Lỗi" hay mẫu "Sạch".

```python
# Thêm vào src/database/db_manager.py

def analyze_word_vector(conn, word_text: str, target_vector: list, limit=5):
    """
    So sánh vector mới với các vector đã lưu trong DB của cùng từ đó.
    Trả về khoảng cách trung bình đến nhóm Clean và nhóm Error.
    """
    # Chuyển list thành string định dạng vector cho SQL
    vector_str = str(target_vector)
    
    query = """
        SELECT 
            (embedding_clean <=> %s) as dist_clean,
            (embedding_error <=> %s) as dist_error
        FROM words 
        WHERE word_text = %s
        -- Chỉ lấy những bản ghi có cả 2 vector (để so sánh công bằng)
        AND embedding_error IS NOT NULL 
        ORDER BY dist_error ASC -- Tìm những lỗi giống nhất trước
        LIMIT %s;
    """
    
    try:
        with conn.cursor() as cur:
            cur.execute(query, (vector_str, vector_str, word_text, limit))
            rows = cur.fetchall()
            
            if not rows:
                return None # Từ này chưa từng xuất hiện trong DB
            
            # Tính trung bình khoảng cách
            avg_dist_clean = sum(r[0] for r in rows) / len(rows)
            avg_dist_error = sum(r[1] for r in rows) / len(rows)
            
            return {
                "avg_dist_clean": avg_dist_clean,
                "avg_dist_error": avg_dist_error,
                "sample_count": len(rows)
            }
            
    except Exception as e:
        logging.error(f"Lỗi khi phân tích vector: {e}")
        return None
```

#### **Bước 2: Tạo module tạo file XML `src/utils/fcpxml_generator.py`**

Module này chịu trách nhiệm "vẽ" ra file kết quả cho editor.

```python
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
```

#### **Bước 3: Tạo Logic Phân tích `src/analysis/detector.py`**

Đây là bộ não của quá trình suy luận.

```python
# src/analysis/detector.py

import os
import logging
from src.utils import file_handler, fcpxml_generator
from src.analysis import transcriber
from src.ai import vectorizer
from src.database import db_manager

def detect_errors_in_video(video_path: str, output_xml_path: str, workspace_dir: str):
    logging.info(f"🔍 Bắt đầu phân tích video: {video_path}")
    
    # 1. Trích xuất Audio
    audio_path = file_handler.extract_audio(video_path, workspace_dir)
    if not audio_path: return False
    
    # 2. Phiên âm
    words = transcriber.get_word_timestamps(audio_path)
    if not words: return False
    
    # 3. Tải Model & DB
    model = vectorizer.load_embedding_model()
    conn = db_manager.get_db_connection()
    
    detected_markers = []
    
    logging.info(f"Đang quét {len(words)} từ...")
    
    # Tạo thư mục temp cho chunks
    temp_chunk_dir = os.path.join(workspace_dir, "temp_inference_chunks")
    os.makedirs(temp_chunk_dir, exist_ok=True)
    
    # 4. Quét từng từ
    for word_info in words:
        word_text = word_info['word'].strip().lower() # Chuẩn hóa
        processed_word = file_handler.sanitize_filename(word_text)
        start = word_info['start']
        end = word_info['end']
        
        # Cắt chunk nhỏ để vector hóa
        chunk_path = os.path.join(temp_chunk_dir, f"{start}_{end}.wav")
        # (Giả định có hàm cắt audio đơn giản trong file_handler, hoặc dùng pydub trực tiếp ở đây)
        # ... Code cắt audio ...
        # Ví dụ dùng file_handler.cut_audio_segment(audio_path, chunk_path, start, end) 
        # (Bạn cần thêm hàm này vào file_handler.py nếu chưa có)
        
        # Tạo vector
        vector = vectorizer.create_embedding(chunk_path, model)
        if not vector: continue
        
        # 5. Truy vấn DB (So sánh)
        analysis = db_manager.analyze_word_vector(conn, processed_word, vector)
        
        if analysis:
            # LOGIC QUYẾT ĐỊNH QUAN TRỌNG
            # Nếu khoảng cách đến mẫu "Lỗi" GẦN HƠN khoảng cách đến mẫu "Sạch"
            # Hoặc vector này quá khác biệt so với mẫu Sạch
            
            dist_error = analysis['avg_dist_error']
            dist_clean = analysis['avg_dist_clean']
            
            # Ngưỡng chênh lệch (Cần tinh chỉnh)
            if dist_error < dist_clean:
                confidence = dist_clean - dist_error # Càng dương lớn càng chắc chắn là lỗi
                
                # Ghi nhận lỗi
                detected_markers.append({
                    'start_sec': start,
                    'duration_sec': end - start,
                    'name': f"[AI] Lỗi Phát âm: {word_text}",
                    'note': f"Confidence: {confidence:.4f}. (Gần mẫu lỗi hơn mẫu sạch)"
                })
        
        # Dọn dẹp file temp
        if os.path.exists(chunk_path): os.remove(chunk_path)

    # 6. Xuất File XML
    if detected_markers:
        logging.info(f"⚠️ Phát hiện {len(detected_markers)} lỗi tiềm ẩn.")
        fcpxml_generator.create_fcpxml_with_markers(video_path, detected_markers, output_xml_path)
        logging.info(f"✅ Đã tạo file markers tại: {output_xml_path}")
    else:
        logging.info("✅ Không phát hiện lỗi nào đáng kể.")
        
    conn.close()
    return True
```

#### **Bước 4: Script chạy chính `detect.py`**

Tạo file `detect.py` ở thư mục gốc để chạy tool này.

```python
# detect.py
import argparse
import os
from dotenv import load_dotenv
from src.analysis import detector

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="AI Error Detector for Dharma Talks")
    parser.add_argument("input_video", help="Path to the raw video file")
    parser.add_argument("--output", help="Path to save the FCPXML file", default="output_markers.fcpxml")
    
    args = parser.parse_args()
    
    workspace = os.getenv("WORKSPACE_DIR", "./workspace")
    
    print(f"🚀 Starting Error Detection for: {args.input_video}")
    detector.detect_errors_in_video(args.input_video, args.output, workspace)

if __name__ == "__main__":
    main()
```

---

### **Cách Sử dụng Module Này**

Bây giờ, quy trình của bạn cho 300 video còn lại sẽ là:

1.  **Trên Colab:** Chạy lệnh.
    ```bash
    python detect.py "/content/drive/MyDrive/Batch_New/video_raw_01.mp4" --output "/content/drive/MyDrive/Batch_New/video_raw_01.fcpxml"
    ```
2.  **Kết quả:** Bạn nhận được file `.fcpxml`.
3.  **Gửi file này cho Editor:** Họ import vào Final Cut Pro, và các lỗi sẽ hiện lên như các To-Do list màu đỏ trên timeline.

Đây chính là sản phẩm cuối cùng mà chúng ta hướng tới trong Phase 1.