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
        file_handler.cut_audio_segment(audio_path, chunk_path, start, end) 
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