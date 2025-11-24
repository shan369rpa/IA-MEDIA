import unittest
from unittest.mock import MagicMock
from src.ai.inference import ErrorDetector

class TestErrorDetector(unittest.TestCase):
    def setUp(self):
        self.detector = ErrorDetector()
        # Mock DB để không cần kết nối thật khi test
        self.detector.db = MagicMock()
        self.detector._check_vector_similarity = MagicMock(return_value=0.9) # Mặc định là giống

    def test_low_volume_error(self):
        """Test phát hiện lỗi âm lượng nhỏ"""
        dummy_embedding = [0.1] * 192
        # Giả lập âm thanh cực nhỏ (rms = 0.001 < 0.005)
        audio_stats = {'rms': 0.001} 
        
        result = self.detector.analyze("test", dummy_embedding, audio_stats)
        
        self.assertTrue(result['is_error'])
        self.assertEqual(result['type'], "[VOL]")
        self.assertIn("Âm lượng quá nhỏ", result['label'])

    def test_pronunciation_error_t_ending(self):
        """Test phát hiện lỗi phát âm đuôi /t/"""
        dummy_embedding = [0.1] * 192
        audio_stats = {'rms': 0.1} # Volume ổn
        
        # Giả lập vector rất khác so với chuẩn (0.6 < 0.82)
        self.detector._check_vector_similarity = MagicMock(return_value=0.6)
        
        # Từ 'bát' kết thúc bằng 't'
        result = self.detector.analyze("bát", dummy_embedding, audio_stats)
        
        self.assertTrue(result['is_error'])
        self.assertEqual(result['type'], "[PRON]")
        # --- ĐÃ SỬA DÒNG NÀY: Thêm dấu gạch ngang /-t/ ---
        self.assertIn("Lỗi âm đuôi /-t/", result['label'])

    def test_noise_detection(self):
        """Test phát hiện tiếng ồn (âm thanh lớn nhưng không có chữ)"""
        dummy_embedding = [0.1] * 192
        # Volume lớn (rms > 0.03) nhưng text rỗng
        audio_stats = {'rms': 0.2} 
        
        result = self.detector.analyze("", dummy_embedding, audio_stats)
        
        self.assertTrue(result['is_error'])
        self.assertEqual(result['type'], "[NOISE]")
        self.assertIn("Tiếng ồn", result['label'])

    def test_clean_word(self):
        """Test từ sạch bình thường"""
        dummy_embedding = [0.1] * 192
        audio_stats = {'rms': 0.1}
        self.detector._check_vector_similarity = MagicMock(return_value=0.95) # Rất giống (> 0.82)
        
        result = self.detector.analyze("pháp", dummy_embedding, audio_stats)
        
        self.assertFalse(result['is_error'])

if __name__ == '__main__':
    unittest.main()