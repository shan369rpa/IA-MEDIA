import logging
import numpy as np
from typing import Dict, List, Union, Optional

# Import module quản lý DB theo đúng hướng dẫn của bạn
from src.database import db_manager

# --- CẤU HÌNH NGƯỠNG (THRESHOLDS) ---
# 1. Ngưỡng độ tương đồng vector (0.0 - 1.0)
# Nếu độ giống nhau thấp hơn mức này -> Đánh dấu là Lỗi phát âm
THRESHOLD_SIMILARITY = 0.82 

# 2. Ngưỡng âm lượng thấp (RMS)
# Nếu RMS thấp hơn mức này -> Đánh dấu là Lỗi âm lượng (quá nhỏ)
THRESHOLD_VOLUME_LOW = 0.005 

# 3. Ngưỡng tiếng ồn (RMS)
# Nếu không có chữ (Whisper rỗng) nhưng RMS cao hơn mức này -> Đánh dấu là Tiếng ồn
THRESHOLD_VOLUME_NOISE = 0.03 

logger = logging.getLogger(__name__)

class ErrorDetector:
    def __init__(self):
        """
        Khởi tạo bộ phát hiện lỗi.
        Định nghĩa danh sách các âm đuôi tiếng Việt dễ bị lai tiếng Anh hoặc phát âm sai
        trong các bài pháp thoại của Sư Ông (ví dụ: bát -> bash, pháp -> phap_s).
        """
        self.problematic_endings = ['t', 'd', 'p', 'c', 'ch', 's', 'x', 'sh', 'th', 'k']

    def analyze(self, word_text: str, embedding: Union[List[float], np.ndarray], audio_stats: Dict) -> Dict:
        """
        Hàm phân tích chính. Kết hợp 3 yếu tố: Kỹ thuật (Audio Stats), Ngữ nghĩa (Text) và AI (Vector).
        
        Args:
            word_text (str): Từ được Whisper nhận diện.
            embedding (list): Vector đặc trưng âm thanh 192 chiều.
            audio_stats (dict): Chứa thông tin như {'rms': 0.05, 'max_amp': 0.8...}
            
        Returns:
            dict: Kết quả chuẩn hóa chứa keys: is_error, type, label, note, confidence.
        """
        
        # 0. Chuẩn hóa dữ liệu đầu vào
        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()
        
        # Làm sạch từ: bỏ dấu câu, chuyển thường
        word_clean = word_text.lower().strip(".,?!:;\"'-")
        rms = audio_stats.get('rms', 0)

        # ---------------------------------------------------------
        # 1. KIỂM TRA LỖI ÂM LƯỢNG (VOLUME CHECK)
        # ---------------------------------------------------------
        if rms < THRESHOLD_VOLUME_LOW:
            return self._create_result(
                is_error=True,
                error_type="[VOL]",
                label="Âm lượng quá nhỏ",
                note=f"RMS: {rms:.4f} < {THRESHOLD_VOLUME_LOW}. Cần tăng gain.",
                confidence=1.0
            )

        # ---------------------------------------------------------
        # 2. KIỂM TRA TIẾNG ỒN (NOISE CHECK)
        # ---------------------------------------------------------
        # Whisper trả về rỗng (hoặc toàn dấu câu) NHƯNG âm thanh lại lớn
        if not word_clean and rms > THRESHOLD_VOLUME_NOISE:
            return self._create_result(
                is_error=True,
                error_type="[NOISE]",
                label="Tiếng ồn/Tạp âm",
                note=f"Không có lời thoại nhưng âm lượng lớn (RMS: {rms:.4f}). Có thể là tiếng ho, gõ bàn, viết bảng.",
                confidence=0.8
            )

        # Nếu là khoảng lặng thực sự (không chữ, âm lượng nhỏ) -> Bỏ qua
        if not word_clean:
            return self._create_result(is_error=False)

        # ---------------------------------------------------------
        # 3. KIỂM TRA LỖI PHÁT ÂM (PRONUNCIATION CHECK)
        # ---------------------------------------------------------
        
        # Truy vấn Database để so sánh vector này với các vector chuẩn
        similarity_score = self._check_vector_similarity(word_clean, embedding)

        # Trường hợp 3a: Từ này chưa từng xuất hiện trong DB (Từ mới)
        if similarity_score is None:
            # Tạm thời bỏ qua, có thể log warning
            return self._create_result(
                is_error=False, 
                note="Chưa có dữ liệu mẫu trong DB để so sánh."
            )

        # Trường hợp 3b: Độ tương đồng thấp hơn ngưỡng cho phép
        if similarity_score < THRESHOLD_SIMILARITY:
            # Kiểm tra xem từ này có kết thúc bằng các âm đuôi nhạy cảm không
            ending = next((end for end in self.problematic_endings if word_clean.endswith(end)), None)
            
            if ending:
                # Nếu có đuôi nhạy cảm -> Gán lỗi cụ thể
                return self._create_result(
                    is_error=True,
                    error_type="[PRON]",
                    label=f"Lỗi âm đuôi /-{ending}/ - '{word_clean}'",
                    note=f"Độ giống chuẩn thấp ({similarity_score:.2f}). Có thể bị bật hơi hoặc lai tiếng Anh.",
                    confidence=1 - similarity_score
                )
            else:
                # Lỗi phát âm chung chung
                return self._create_result(
                    is_error=True,
                    error_type="[PRON]",
                    label=f"Phát âm lạ - '{word_clean}'",
                    note=f"Độ giống chuẩn: {similarity_score:.2f} (Ngưỡng: {THRESHOLD_SIMILARITY}). Cần kiểm tra lại.",
                    confidence=1 - similarity_score
                )

        # ---------------------------------------------------------
        # 4. KHÔNG CÓ LỖI (PASS)
        # ---------------------------------------------------------
        return self._create_result(is_error=False, confidence=similarity_score)

    def _check_vector_similarity(self, word_text: str, embedding: list, k: int = 5) -> Optional[float]:
        """
        Truy vấn DB để so sánh vector hiện tại với K vector 'sạch' nhất của từ đó.
        Trả về điểm tương đồng trung bình (0.0 -> 1.0).
        """
        conn = None
        try:
            # SỬ DỤNG DB MANAGER ĐÚNG CÁCH
            conn = db_manager.get_db_connection()
            if not conn:
                logger.error("Không thể kết nối DB để kiểm tra vector.")
                return None
            
            cursor = conn.cursor()
            
            # Truy vấn tìm K vector gần nhất trong bảng words
            # Lưu ý: embedding_clean là vector chuẩn từ video edited
            # Toán tử <=> trả về Cosine Distance (0=giống, 1=khác, 2=đối nghịch)
            # Similarity = 1 - Distance
            query = """
                SELECT 1 - (embedding_clean <=> %s::vector) as similarity
                FROM words
                WHERE word_text = %s
                ORDER BY embedding_clean <=> %s::vector ASC
                LIMIT %s;
            """
            
            # Chuyển list thành chuỗi format vector cho pgvector ('[0.1,0.2,...]')
            embedding_str = str(embedding)
            
            cursor.execute(query, (embedding_str, word_text, embedding_str, k))
            rows = cursor.fetchall()

            if not rows:
                return None

            # Tính trung bình cộng độ tương đồng của K hàng xóm
            similarities = [row[0] for row in rows]
            avg_similarity = sum(similarities) / len(similarities)
            
            return avg_similarity

        except Exception as e:
            logger.error(f"Lỗi truy vấn vector similarity cho từ '{word_text}': {e}")
            return None
        finally:
            if conn:
                conn.close()

    def _create_result(self, is_error: bool, error_type: str = "", label: str = "", note: str = "", confidence: float = 0.0) -> Dict:
        """Helper function để đảm bảo cấu trúc output luôn nhất quán."""
        return {
            "is_error": is_error,
            "type": error_type,     # Ví dụ: [PRON], [VOL]
            "label": label,         # Tên hiển thị trên Marker
            "note": note,           # Ghi chú chi tiết bên trong Marker
            "confidence": round(confidence, 2)
        }