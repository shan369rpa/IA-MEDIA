# src/inference/detector.py

import os
import logging
import numpy as np
from scipy.spatial.distance import cosine

from src.utils import file_handler, fcpxml_generator
from src.analysis import transcriber, signal_analyzer
from src.ai import vectorizer
from src.database import db_manager

logging.basicConfig(level=logging.INFO)

class ErrorDetector:
    def __init__(self, workspace_dir):
        self.workspace_dir = workspace_dir
        self.signal_analyzer = signal_analyzer.SignalAnalyzer()
        
        # Kết nối DB và Load Model khi khởi tạo
        self.conn = db_manager.get_db_connection()
        self.embedding_model = vectorizer.load_embedding_model()

    def _classify_vector_knn(self, target_vector, reference_data, k=5):
        """
        Thuật toán KNN đơn giản để phân loại lỗi.
        So sánh vector mục tiêu với các vector tham chiếu (đã gán nhãn clean/error).
        """
        if not reference_data:
            return "unknown", 0.0

        distances = []
        for item in reference_data:
            # Tính cosine distance
            # SpeechBrain vector thường cần flatten
            ref_vec = np.array(item['embedding']).flatten()
            tgt_vec = np.array(target_vector).flatten()
            
            dist = cosine(ref_vec, tgt_vec)
            distances.append((dist, item['label']))
        
        # Sắp xếp theo khoảng cách gần nhất
        distances.sort(key=lambda x: x[0])
        nearest_neighbors = distances[:k]
        
        # Đếm phiếu (Voting)
        error_votes = sum(1 for d in nearest_neighbors if d[1] == 'error')
        clean_votes = sum(1 for d in nearest_neighbors if d[1] == 'clean')
        
        # Logic quyết định
        if error_votes > clean_votes:
            return "error_pronunciation", nearest_neighbors[0][0] # Trả về loại lỗi và khoảng cách min
        else:
            # Kiểm tra khoảng cách "Bất thường"
            # Nếu "clean" nhưng khoảng cách quá xa => có thể là giọng lạ/nhiễu lạ
            min_dist = nearest_neighbors[0][0]
            if min_dist > 0.4: # Ngưỡng này cần tinh chỉnh gọi là Threshold
                return "anomaly_unseen", min_dist
            
            return "clean", min_dist

    def process_video(self, raw_video_path: str):
        logging.info(f"=== BẮT ĐẦU PHÁT HIỆN LỖI: {os.path.basename(raw_video_path)} ===")
        
        detected_markers = [] # Danh sách lỗi để tạo FCPXML

        # 1. Trích xuất Audio
        # (Dùng lại hàm cũ, hoặc viết hàm mới chỉ trích xuất 1 file)
        audio_path = file_handler.extract_audio(raw_video_path, self.workspace_dir)
        if not audio_path: return

        # 2. Phiên âm lấy Word Timestamps
        word_timestamps = transcriber.get_word_timestamps(audio_path)
        if not word_timestamps: return

        # Tải audio segment đầy đủ để cắt nhanh
        full_audio = file_handler.load_audio_segment(audio_path)

        # 3. Vòng lặp Phân tích từng từ
        for word_info in word_timestamps:
            word_text = word_info['word'].strip().lower()
            start_ms = int(word_info['start'] * 1000)
            end_ms = int(word_info['end'] * 1000)
            
            # Bỏ qua từ quá ngắn
            if end_ms - start_ms < 100: continue

            # --- BƯỚC PHÂN TÍCH TÍN HIỆU (SIGNAL ANALYSIS) ---
            # Cắt chunk tạm vào RAM hoặc file tạm
            temp_chunk_path = file_handler.extract_audio_chunk_memory(full_audio, start_ms, end_ms)
            
            if temp_chunk_path:
                # Kiểm tra lỗi kỹ thuật trước (Nhanh hơn vector)
                sig_result = self.signal_analyzer.analyze_chunk(temp_chunk_path)
                
                error_label = None
                note = ""

                if sig_result['is_clipping']:
                    error_label = "Technical: Clipping"
                    note = f"Max Amp: {sig_result['max_amplitude']:.2f}"
                elif sig_result['is_noise_spike']:
                    error_label = "Technical: Noise Spike"
                elif sig_result['is_silence']:
                    # Im lặng thì thôi, có thể là khoảng nghỉ
                    pass 
                else:
                    # --- BƯỚC PHÂN TÍCH VECTOR (AI / RAG) ---
                    # Chỉ chạy nếu tín hiệu tốt
                    
                    # A. Tạo vector cho từ hiện tại
                    vector = vectorizer.create_embedding(temp_chunk_path, self.embedding_model)
                    
                    # B. Lấy kiến thức từ DB
                    ref_vectors = db_manager.get_word_vectors(self.conn, word_text)
                    
                    # C. So sánh
                    ai_label, distance = self._classify_vector_knn(vector, ref_vectors)
                    
                    if ai_label != "clean":
                        error_label = f"AI: {ai_label}"
                        note = f"Distance: {distance:.2f}"

                # --- KẾT LUẬN CHO TỪ NÀY ---
                if error_label:
                    print(f"!!! DETECTED: {word_text} -> {error_label}")
                    detected_markers.append({
                        "start": word_info['start'],
                        "name": f"[{error_label}] {word_text}",
                        "note": note
                    })
                
                # Dọn dẹp file tạm
                if os.path.exists(temp_chunk_path):
                    os.remove(temp_chunk_path)

        # 4. Tạo Output FCPXML
        output_xml_path = os.path.join(self.workspace_dir, f"{os.path.basename(raw_video_path)}.fcpxml")
        
        # Lấy duration video (có thể dùng ffprobe, tạm thời lấy từ audio)
        video_duration = len(full_audio) / 1000.0
        
        gen = fcpxml_generator.FCPXMLGenerator(raw_video_path, video_duration)
        gen.generate(detected_markers, output_xml_path)
        
        logging.info(f"HOÀN TẤT. File To-Do Markers: {output_xml_path}")
        if self.conn: self.conn.close()

if __name__ == '__main__':
    # Test cục bộ
    detector = ErrorDetector("./workspace")
    detector.process_video("./data/test_raw.mp4")