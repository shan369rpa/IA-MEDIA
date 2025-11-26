Bạn đang đặt những câu hỏi rất sát sườn về **Chất lượng sản phẩm đầu ra (Product Quality)**. Đúng là nếu chỉ báo "Lỗi" chung chung thì Editor sẽ không thấy "wow".

Để giải quyết vấn đề này, tôi sẽ thực hiện 3 phần việc trong câu trả lời này:
1.  **Cung cấp Unit Tests** chuẩn cho 2 module mới.
2.  **Mô tả Output FCPXML** (Editor sẽ thấy gì).
3.  **Giải quyết bài toán "Đặt tên lỗi"**: Nâng cấp logic `inference.py` để phân loại lỗi cụ thể hơn ngay trong Demo.

---

### PHẦN 1: UNIT TESTS (Chuẩn Modular)

Chúng ta sẽ tạo 2 file test trong thư mục `tests/`.

#### 1. `tests/test_fcpxml_generator.py`
Kiểm tra xem file XML sinh ra có đúng cấu trúc mà Final Cut Pro yêu cầu không.

```python
import unittest
import os
import xml.etree.ElementTree as ET
from src.utils.fcpxml_generator import FCPXMLGenerator

class TestFCPXMLGenerator(unittest.TestCase):
    def setUp(self):
        self.output_path = "test_output.fcpxml"
        self.generator = FCPXMLGenerator("test_video.mp4", 100.0)

    def tearDown(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_seconds_to_frame_str(self):
        # 1 giây ở 60fps = 6000 frames (do hệ số nhân 100) / 6000 timescale
        res = self.generator._seconds_to_frame_str(1.0)
        # Kiểm tra logic tính toán frame (tùy thuộc vào implementation của bạn)
        self.assertIn("/6000s", res) 

    def test_add_marker(self):
        self.generator.add_marker(10.5, "[AI] Test", "Note test")
        self.assertEqual(len(self.generator.markers), 1)
        self.assertEqual(self.generator.markers[0]['start'], 10.5)

    def test_generate_xml_structure(self):
        self.generator.add_marker(5.0, "Error 1", "Note 1")
        self.generator.generate_xml(self.output_path)
        
        # Parse lại file vừa tạo để kiểm tra
        tree = ET.parse(self.output_path)
        root = tree.getroot()
        
        self.assertEqual(root.tag, "fcpxml")
        # Kiểm tra có thẻ asset-clip không
        asset_clip = root.find(".//asset-clip")
        self.assertIsNotNone(asset_clip)
        # Kiểm tra có marker không
        marker = asset_clip.find("marker")
        self.assertIsNotNone(marker)
        self.assertEqual(marker.attrib['value'], "Error 1")
        self.assertEqual(marker.attrib['note'], "Note 1")
```

#### 2. `tests/test_inference.py`
Kiểm tra logic phán đoán. Chúng ta sẽ dùng `unittest.mock` để giả lập Database, không cần kết nối DB thật.

```python
import unittest
from unittest.mock import MagicMock, patch
from src.ai.inference import ErrorDetector

class TestErrorDetector(unittest.TestCase):
    def setUp(self):
        # Mock DBManager để không kết nối DB thật
        self.patcher = patch('src.ai.inference.DBManager')
        self.MockDB = self.patcher.start()
        self.detector = ErrorDetector()

    def tearDown(self):
        self.patcher.stop()

    def test_analyze_word_clean(self):
        # Giả lập DB trả về vector rất giống (khoảng cách 0.1)
        # Cấu trúc trả về: (chunk_type, similarity)
        # Vì query trả về '1 - distance' -> similarity cao là giống.
        # Giả sử threshold của ta là 0.85
        mock_cursor = self.detector.db.get_connection().cursor.return_value
        mock_cursor.fetchall.return_value = [('clean', 0.95), ('clean', 0.92)]
        
        result = self.detector.analyze_word("test", [0.1]*192)
        
        self.assertFalse(result['is_error'])
        self.assertEqual(result['reason'], "OK")

    def test_analyze_word_error(self):
        # Giả lập DB trả về vector rất khác (khoảng cách lớn -> similarity thấp)
        mock_cursor = self.detector.db.get_connection().cursor.return_value
        mock_cursor.fetchall.return_value = [('clean', 0.40), ('clean', 0.50)]
        
        result = self.detector.analyze_word("test", [0.1]*192)
        
        self.assertTrue(result['is_error'])
        self.assertIn("Phát âm lạ", result['reason'])
```

---

### PHẦN 2: OUTPUT THỰC TẾ TRÔNG NHƯ THẾ NÀO?

Khi Editor import file `.fcpxml` vào Final Cut Pro, đây là những gì họ nhận được:

1.  **Trên Timeline:** Một dòng các **vạch màu (Markers)** nằm trên clip video gốc.
2.  **Thông tin Marker (Khi click vào):**
    *   **Tên Marker (Value):** Hiển thị ngắn gọn loại lỗi.
        *   *Ví dụ:* `[AI] Pronunciation` hoặc `[AI] Silence`.
    *   **Ghi chú (Note):** Hiển thị chi tiết và gợi ý.
        *   *Ví dụ:* `Word: 'kết thúc' | Confidence: 89% | Suggestion: Check final 'c' sound.`

**Cấu trúc XML thực tế:**
```xml
<marker start="360360/6000s" duration="100/6000s" value="[AI] Pronunciation: 'pháp'" note="Độ lệch chuẩn: High. Gợi ý: Kiểm tra âm đuôi /p/." />
```

---

### PHẦN 3: GIẢI QUYẾT BÀI TOÁN "ĐẶT TÊN LỖI" (CRITICAL)

Bạn hỏi: *"Làm sao biết chính xác là lỗi gì (âm vị, ồn, volume...) để đặt tên?"*

**Thực trạng hiện tại (Pure Vector Logic):**
Nếu chỉ dùng Vector Distance (`embedding <=> embedding`), AI chỉ biết: *"Đoạn này KHÁC với giọng chuẩn"*. Nó **không biết** tại sao khác (do ồn hay do nói sai). Nếu chỉ dùng logic này, ta chỉ có thể đặt tên là `[AI] Anomaly` (Bất thường).

**Giải pháp Nâng cấp cho Demo (Hybrid Logic):**
Để Demo ấn tượng và "thông minh" hơn, chúng ta sẽ kết hợp **Vector AI** với **Heuristics (Luật dựa trên thông số âm thanh)** trong file `inference.py`.

Tôi sẽ cập nhật logic `inference.py` để phân loại được 3 loại lỗi sau:

1.  **Lỗi Khoảng lặng (Silence/Dead Air):** Dựa vào âm lượng (Volume/RMS).
2.  **Lỗi Tiếng ồn/Click (Noise):** Dựa vào độ ngắn của chunk và cường độ đột ngột.
3.  **Lỗi Phát âm (Pronunciation):** Nếu âm lượng bình thường nhưng Vector lại khác xa chuẩn.

**Cập nhật Code `src/ai/inference.py` (Thông minh hơn):**

```python
import logging
import numpy as np
# Cần thêm thư viện để tính âm lượng
import librosa 

logger = logging.getLogger(__name__)

class ErrorDetector:
    def __init__(self):
        self.db = DBManager()

    def analyze_audio_segment(self, audio_path: str, word_text: str, embedding: list) -> dict:
        """
        Phân tích kết hợp: Âm thanh vật lý + Vector AI
        """
        # 1. KIỂM TRA VẬT LÝ (HEURISTICS)
        try:
            y, sr = librosa.load(audio_path, sr=16000)
            duration = librosa.get_duration(y=y, sr=sr)
            rms = librosa.feature.rms(y=y)[0]
            avg_volume = np.mean(rms)
            
            # Rule A: Khoảng lặng bất thường (Volume quá nhỏ)
            if avg_volume < 0.005: 
                return {
                    "is_error": True,
                    "label": "[AI] Silence",
                    "reason": "Âm lượng quá nhỏ (nghi ngờ mất tiếng/khoảng lặng thừa)."
                }
                
            # Rule B: Tiếng ồn ngắn (Duration quá ngắn + Volume lớn)
            # Ví dụ: Tiếng click chuột, tiếng ho ngắn
            if duration < 0.2 and avg_volume > 0.1:
                return {
                    "is_error": True,
                    "label": "[AI] Noise/Click",
                    "reason": "Âm thanh ngắn và lớn đột ngột."
                }
                
        except Exception as e:
            logger.warning(f"Không thể phân tích vật lý file {audio_path}: {e}")

        # 2. KIỂM TRA VECTOR AI (SEMANTIC/PHONETIC)
        # (Logic so sánh DB như cũ)
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # ... (Query DB lấy neighbors) ...
        # Giả sử lấy được avg_similarity
        
        threshold_pronunciation = 0.82
        
        if avg_similarity < threshold_pronunciation:
            return {
                "is_error": True,
                "label": f"[AI] Pronunciation: '{word_text}'",
                "reason": f"Khác biệt so với giọng chuẩn ({avg_similarity:.2f}). Có thể do âm đuôi hoặc giọng địa phương."
            }
            
        return {"is_error": False, "label": "OK", "reason": "OK"}
```

**Kết luận:**
Với bản cập nhật `inference.py` kết hợp này, marker của chúng ta sẽ có tên cụ thể:
*   `[AI] Silence`
*   `[AI] Noise/Click`
*   `[AI] Pronunciation: 'pháp'`

Điều này đã giải quyết vấn đề bạn lo lắng: **Chúng ta biết chính xác (hoặc đoán rất sát) loại lỗi là gì.** Bạn có đồng ý với logic kết hợp này không?