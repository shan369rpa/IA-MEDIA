# analyze_new_video.py
import os
import sys
import logging
import joblib
import numpy as np
import argparse # Dùng để nhận tham số dòng lệnh

# Fix import
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from dotenv import load_dotenv
from src.utils.environment import setup_environment
setup_environment()
from src.utils import file_handler, fcpxml_generator
from src.analysis import transcriber
from src.ai import vectorizer
from src.database import db_manager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s', force=True)

def analyze_video(video_path: str, output_path: str):
    """
    Pipeline hoàn chỉnh để phân tích một video RAW mới và tạo báo cáo lỗi FCPXML.
    """
    load_dotenv()
    
    if not os.path.exists(video_path):
        logging.error(f"File video không tồn tại: {video_path}")
        return

    # --- 1. Tải các "bộ não" cần thiết ---
    logging.info("Đang tải các model cần thiết...")
    # Tải model phân loại lỗi đã huấn luyện
    classifier_model = joblib.load("error_classifier.pkl")
    # Tải model embedding
    embedding_model = vectorizer.load_embedding_model()
    # Kết nối CSDL
    conn = db_manager.get_db_connection()

    if not all([classifier_model, embedding_model, conn]):
        logging.error("Không thể tải model hoặc kết nối CSDL. Dừng lại.")
        if conn: conn.close()
        return

    workspace_dir = "./workspace_inference"
    os.makedirs(workspace_dir, exist_ok=True)

    try:
        # --- 2. Trích xuất Audio và Phiên âm ---
        logging.info("Trích xuất audio từ video mới...")
        audio_path = file_handler.extract_audio(video_path, workspace_dir)
        if not audio_path: return

        logging.info("Phiên âm video mới để lấy word timestamps...")
        word_timestamps = transcriber.get_word_timestamps(audio_path)
        if not word_timestamps: return

        # --- 3. Phân tích Từng từ ---
        logging.info(f"Bắt đầu phân tích {len(word_timestamps)} từ trong video...")
        potential_errors = []
        
        # Tải audio vào bộ nhớ để cắt chunk nhanh hơn
        from pydub import AudioSegment
        full_audio = AudioSegment.from_wav(audio_path)

        for word_info in word_timestamps:
            start_sec = word_info['start']
            end_sec = word_info['end']
            
            # Cắt audio chunk của từ mới trong bộ nhớ
            word_chunk_audio = full_audio[int(start_sec * 1000):int(end_sec * 1000)]
            temp_chunk_path = os.path.join(workspace_dir, "temp_chunk.wav")
            word_chunk_audio.export(temp_chunk_path, format="wav")

            # Tạo embedding cho chunk mới
            new_embedding = vectorizer.create_embedding(temp_chunk_path, embedding_model)
            if new_embedding is None: continue
            
            # --- 4. So sánh và Phân loại ---
            with conn.cursor() as cur:
                # Tìm embedding 'clean' gần nhất trong CSDL
                cur.execute(
                    'SELECT embedding_clean FROM "words" ORDER BY embedding_clean <=> %s LIMIT 1',
                    (np.array(new_embedding),)
                )
                closest_clean_embedding = cur.fetchone()

                if closest_clean_embedding:
                    # Tính vector khác biệt giả định
                    diff_vector = np.array(new_embedding) - np.array(closest_clean_embedding[0])
                    
                    # Dùng model để dự đoán loại lỗi
                    # model.predict nhận vào một list các mẫu, nên ta cần reshape
                    predicted_label = classifier_model.predict([diff_vector])[0]
                    
                    # Chúng ta chỉ báo cáo những lỗi không phải là 'pronunciation' mặc định
                    # hoặc có thể báo cáo tất cả tùy theo chiến lược
                    if predicted_label != "error_pronunciation": # Tạm thời vẫn lọc
                        # --- TẠO NỘI DUNG MARKER MỚI ---
                        error_type_map = {
                            "error_clipping": "Vỡ Tiếng (Clipping)",
                            "error_noise_spike": "Nhiễu Đột ngột (Noise Spike)",
                            "error_low_volume": "Âm lượng Thấp (Low Volume)",
                            "error_missing_audio": "Mất Âm thanh (Silence)",
                            "error_pronunciation": "Phát âm (Pronunciation)"
                        }
                        error_description = error_type_map.get(predicted_label, "Lỗi không xác định")
                        
                        marker_text = f"AI | {error_description} | Từ: '{word_info['word']}'"
                        
                        error_info = {
                            "start_sec": start_sec,
                            "duration_sec": end_sec - start_sec,
                            "text": marker_text,
                            "completed": False,
                            "type": predicted_label # Thêm loại lỗi để tô màu
                        }
                        potential_errors.append(error_info)
                        logging.info(f"Phát hiện lỗi tiềm năng: {error_info['text']} lúc {start_sec:.2f}s")
        
        # --- 5. Tạo file FCPXML ---
        if potential_errors:
            logging.info(f"Tổng cộng phát hiện {len(potential_errors)} lỗi tiềm năng. Đang tạo báo cáo FCPXML...")
            # Lấy thông tin thời lượng video
            import ffmpeg
            probe = ffmpeg.probe(video_path)
            duration = float(probe['format']['duration'])
            
            fcpxml_generator.create_fcpxml_with_markers(
                output_path=output_path,
                video_path=video_path,
                video_duration_sec=duration,
                markers_list=potential_errors
            )
        else:
            logging.info("Không phát hiện lỗi kỹ thuật đáng kể nào.")

    except Exception as e:
        logging.exception("Lỗi trong quá trình phân tích video mới.")
    finally:
        if conn: conn.close()
        # Dọn dẹp thư mục tạm
        # import shutil
        # if os.path.exists(workspace_dir):
        #     shutil.rmtree(workspace_dir)

if __name__ == '__main__':
    # Tạo một parser để nhận tham số từ dòng lệnh
    parser = argparse.ArgumentParser(description="Phân tích video RAW và tạo báo cáo lỗi FCPXML.")
    parser.add_argument("video_path", type=str, help="Đường dẫn đến file video RAW cần phân tích.")
    parser.add_argument("-o", "--output", type=str, default="report.fcpxml", help="Đường dẫn file FCPXML đầu ra (mặc định: report.fcpxml).")
    
    args = parser.parse_args()
    
    analyze_video(args.video_path, args.output)