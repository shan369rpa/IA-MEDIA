import os
import logging
from dotenv import load_dotenv

# --- SỬA IMPORT ---
# Thay vì import AudioVectorizer, ta import module vectorizer
from src.utils import file_handler
from src.analysis import transcriber
from src.ai import vectorizer  # <--- Thay đổi ở đây
from src.ai.inference import ErrorDetector
from src.utils.fcpxml_generator import FCPXMLGenerator
from pydub import AudioSegment

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- CẤU HÌNH INPUT CHO DEMO ---
INPUT_RAW_VIDEO = "./data/Batch_01/demo_test_raw.mp4" 
OUTPUT_XML_PATH = "./workspace/Batch_01/demo_result.fcpxml"
WORKSPACE_DIR = "./workspace/inference"

def main():
    logger.info(f"🕵️ BẮT ĐẦU QUÁ TRÌNH PHÁT HIỆN LỖI: {INPUT_RAW_VIDEO}")
    
    if not os.path.exists(INPUT_RAW_VIDEO):
        logger.error(f"❌ Không tìm thấy file input: {INPUT_RAW_VIDEO}")
        return

    os.makedirs(WORKSPACE_DIR, exist_ok=True)

    # 1. Extract Audio từ Video Raw
    logger.info("🔊 Bước 1: Trích xuất Audio...")
    # raw_audio_path = os.path.join(WORKSPACE_DIR, "temp_inference.wav")
    raw_audio_path = file_handler.extract_audio(INPUT_RAW_VIDEO, WORKSPACE_DIR)
    # Lấy độ dài video để làm XML
    duration = file_handler.get_audio_duration(raw_audio_path)

    # 2. Transcribe (Lấy timestamp từng từ)
    logger.info("📝 Bước 2: Transcribe (Whisper)...")
    words = transcriber.get_word_timestamps(raw_audio_path)
    logger.info(f"   -> Tìm thấy {len(words)} từ.")

    # 3. Khởi tạo các Engine
    # vectorizer = AudioVectorizer()  <--- BỎ DÒNG KHỞI TẠO NÀY
    detector = ErrorDetector()
    xml_gen = FCPXMLGenerator(INPUT_RAW_VIDEO, duration)

    # 4. Vòng lặp phân tích từng từ
    logger.info("🧠 Bước 3: Phân tích từng từ (Inference)...")
    error_count = 0
    
    # Load audio vào RAM một lần để cắt cho nhanh
    audio_segment = AudioSegment.from_wav(raw_audio_path)

    for i, word in enumerate(words):
        word_text = word['word'].strip().lower()
        start_ms = int(word['start'] * 1000)
        end_ms = int(word['end'] * 1000)
        
        if end_ms - start_ms < 100: continue

        # 4.1. Cắt chunk ảo (trong RAM)
        chunk_audio = audio_segment[start_ms:end_ms]
        
        # 4.2. Tính toán Audio Stats (RMS) cho logic phát hiện lỗi Volume/Noise
        audio_stats = {
            'rms': chunk_audio.rms / 32768.0,  # Chuẩn hóa về 0.0 - 1.0 (cho 16-bit audio)
            'max_amp': chunk_audio.max_dBFS
        }

        # Lưu tạm ra disk vì SpeechBrain cần file path
        temp_chunk_path = os.path.join(WORKSPACE_DIR, "temp_chunk.wav")
        chunk_audio.export(temp_chunk_path, format="wav")
        model = vectorizer.load_embedding_model()  # Load model ở đây để tránh lỗi
        # 4.3. Vector hóa (GỌI TRỰC TIẾP TỪ MODULE)
        embedding = vectorizer.create_embedding(temp_chunk_path,model) # <--- Thay đổi ở đây

        # 4.4. Phán đoán (Inference)
        # Truyền thêm audio_stats vào hàm analyze mới
        result = detector.analyze(word_text, embedding, audio_stats)

        # 4.5. Nếu là lỗi -> Thêm vào XML
        if result['is_error']:
            error_count += 1
            timestamp_sec = word['start']
            label = result['label']
            note = f"{result['type']} {result['note']} (Confidence: {result['confidence']})"
            
            xml_gen.add_marker(timestamp_sec, label, note)
            logger.info(f"   🚩 {label} tại {timestamp_sec:.2f}s")

    # 5. Xuất file XML
    logger.info(f"💾 Bước 4: Tạo file FCPXML...")
    xml_gen.generate_xml(OUTPUT_XML_PATH)
    
    logger.info(f"✅ HOÀN TẤT! Đã phát hiện {error_count} lỗi.")
    logger.info(f"📂 File kết quả: {OUTPUT_XML_PATH}")

if __name__ == "__main__":
    main()