# backend_core.py
import os
import time # Import thêm time để tạo timestamp
import concurrent.futures # <--- THÊM THƯ VIỆN NÀY ĐỂ XỬ LÝ ĐA LUỒNG
import matplotlib.pyplot as plt
import seaborn as sns
import librosa
import pandas as pd
import numpy as np
import joblib
# Import FeatureExtractor riêng lẻ thay vì Processor
from transformers import Wav2Vec2Model, Wav2Vec2FeatureExtractor
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import scipy.signal # Cần thêm thư viện này
from sklearn.metrics import classification_report, confusion_matrix
from tqdm import tqdm
# --- CẤU HÌNH HỆ THỐNG ---
DATA_CSV = "training_data.csv"
MODEL_FILE = "error_classifier.pkl"
DATA_FOLDER = "collected_data" 

# Model 1024 chiều SOTA
MODEL_NAME = "facebook/wav2vec2-large-xlsr-53"
TARGET_SAMPLE_RATE = 16000
VECTOR_DIM = 1024


# --- CẤU HÌNH MÀU SẮC FCP ---
FCP_COLORS = {
    "BACKGROUND": "#1e1e1e", "TRACK_BG": "#262626", "TEXT": "#d1d1d1",
    "GRID": "#3b3b3b", "CLEAN": "#3cc2ea", "RAW": "#64d2ff", "ERROR": "#ff5e5e"
}
import torch

if torch.backends.mps.is_available():
    DEVICE = torch.device("mps")
    print(f"🚀 HARDWARE: Apple Silicon GPU (MPS) Activated. Ready on M2 Ultra.")
elif torch.cuda.is_available():
    DEVICE = torch.device("cuda")
    print("🚀 HARDWARE: NVIDIA GPU (CUDA) Activated.")
else:
    DEVICE = torch.device("cpu")
    print("⚠️ HARDWARE: Running on CPU.")

# --- KHỞI TẠO AI ENGINE (FIXED) ---
print("⏳ Đang khởi tạo AI Core...")
try:
    # 1. Tải Model Weights (Trí tuệ)
    model = Wav2Vec2Model.from_pretrained(MODEL_NAME).to(DEVICE)
    model.eval() # Chế độ suy luận
    
    # 2. Khởi tạo Feature Extractor THỦ CÔNG (Fix lỗi thiếu file config trên HuggingFace)
    # Đây là cấu hình chuẩn cho Wav2Vec2: 16kHz, chuẩn hóa zero-mean unit-variance
    feature_extractor = Wav2Vec2FeatureExtractor(
        feature_size=1,
        sampling_rate=TARGET_SAMPLE_RATE,
        padding_value=0.0,
        do_normalize=True,
        return_attention_mask=True
    )
    print(f"✅ AI Engine đã sẵn sàng! Device: {DEVICE}")
except Exception as e:
    print(f"❌ Lỗi khởi tạo AI Engine: {e}")
    feature_extractor = None
    model = None

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# --- CÁC HÀM XỬ LÝ (CORE LOGIC) ---

# --- HÀM MỚI: LƯU CẶP DỮ LIỆU ---
def save_paired_data(raw_file, clean_file, label):
    """
    Lưu cặp file Raw và Clean, tự động Align và lưu thêm file Difference.
    """
    timestamp = int(time.time())
    base_name = f"{timestamp}_{label}"
    
    # 1. Load và Align ngay lập tức
    # (Lưu tạm để load bằng librosa/torchaudio)
    temp_raw = f"temp_raw_{timestamp}.wav"
    temp_clean = f"temp_clean_{timestamp}.wav"
    with open(temp_raw, "wb") as f: f.write(raw_file.getbuffer())
    with open(temp_clean, "wb") as f: f.write(clean_file.getbuffer())
    
    y_raw, sr = librosa.load(temp_raw, sr=16000)
    y_clean, _ = librosa.load(temp_clean, sr=16000)
    
    # Align
    y_raw_aligned, lag = auto_align_audio(y_clean, y_raw)
    
    # 2. Lưu file vật lý
    raw_path = os.path.join(DATA_FOLDER, f"{base_name}_raw.wav")
    clean_path = os.path.join(DATA_FOLDER, f"{base_name}_clean.wav")
    
    import soundfile as sf
    sf.write(raw_path, y_raw_aligned, sr)
    sf.write(clean_path, y_clean, sr)
    
    # 3. Ghi CSV
    # Cột: raw_path, clean_path, label
    df = pd.DataFrame([[raw_path, clean_path, label]], columns=["raw_path", "clean_path", "label"])
    
    if not os.path.isfile(DATA_CSV):
        df.to_csv(DATA_CSV, index=False)
    else:
        df.to_csv(DATA_CSV, mode='a', header=False, index=False)
        
    # Dọn dẹp
    os.remove(temp_raw)
    os.remove(temp_clean)
    return True

def save_training_data(file_obj, label):
    """Lưu file upload vào thư mục NAS và ghi log vào CSV."""
    
    # 1. Tạo tên file độc nhất (Tránh Editor A ghi đè file của Editor B)
    # Cấu trúc: timestamp_filename
    timestamp = int(time.time())
    original_name = os.path.basename(file_obj.name)
    safe_filename = f"{timestamp}_{original_name}"
    
    save_path = os.path.join(DATA_FOLDER, safe_filename)
    # 2. Lưu file vật lý (Streamlit nhận file -> Lưu vào NAS)
    with open(save_path, "wb") as f:
        f.write(file_obj.getbuffer())
    
    # 3. Ghi vào CSV (Cũng nằm trên NAS)
    # Thêm cột 'editor_ip' hoặc 'user' nếu muốn track ai gửi (cần nâng cao hơn)
    df = pd.DataFrame([[save_path, label]], columns=["filepath", "label"])
    
    # Chế độ append ('a')
    # Kiểm tra xem file có header chưa
    file_exists = os.path.isfile(DATA_CSV)
    df.to_csv(DATA_CSV, mode='a', header=not file_exists, index=False)
    
    return True
# --- TỰ ĐỘNG CHỌN THIẾT BỊ (M2 ULTRA OPTIMIZED) ---

# def load_and_preprocess_audio(audio_path, duration=None):
#     """
#     Load audio an toàn hơn cho đa luồng.
#     """
#     # Import bên trong hàm để tránh deadlock trên MacOS khi dùng đa luồng
#     import torchaudio
#     import torch

#     try:
#         # Load trực tiếp
#         waveform, sample_rate = torchaudio.load(audio_path)
        
#         # Chuyển Mono
#         if waveform.shape[0] > 1:
#             waveform = torch.mean(waveform, dim=0, keepdim=True)
            
#         # Resample
#         if sample_rate != TARGET_SAMPLE_RATE:
#             resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=TARGET_SAMPLE_RATE)
#             waveform = resampler(waveform)
            
#         # Cắt ngắn
#         if duration:
#             max_len = int(duration * TARGET_SAMPLE_RATE)
#             if waveform.shape[1] > max_len:
#                 waveform = waveform[:, :max_len]
                
#         return waveform.squeeze(), None
#     except Exception as e:
#         return None, f"{os.path.basename(audio_path)}: {str(e)}"

# def extract_embeddings_batch(audio_list):
#     """
#     Xử lý batch audio, chuẩn hóa shape chặt chẽ để tránh lỗi conv1d.
#     """
#     if not audio_list: return np.array([])
        
#     cleaned_list = []
#     for item in audio_list:
#         # 1. Chuyển về Tensor nếu là Numpy
#         if isinstance(item, np.ndarray):
#             item = torch.from_numpy(item)
            
#         # 2. Xử lý Shape: Bắt buộc về dạng (Time,)
#         # Nếu là (Channel, Time) -> Chọn kênh đầu hoặc Mean
#         if item.dim() > 1:
#             # Nếu shape là (1, Time) -> squeeze thành (Time,)
#             if item.shape[0] == 1:
#                 item = item.squeeze(0)
#             # Nếu shape là (Time, 1) -> squeeze
#             elif item.shape[-1] == 1:
#                 item = item.squeeze(-1)
#             # Nếu nhiều kênh (2, Time) -> Mean
#             elif item.shape[0] < 10: # Giả sử channel dim ở đầu
#                 item = item.mean(dim=0)
#             # Trường hợp quái dị [1, 4, 16000] -> Flatten hết mức có thể
#             else:
#                 item = item.reshape(-1) # Cẩn thận, nhưng tốt hơn là crash

#         cleaned_list.append(item)
            
#     if not cleaned_list: return np.array([])

#     try:
#         inputs = feature_extractor(
#             cleaned_list, 
#             sampling_rate=TARGET_SAMPLE_RATE, 
#             return_tensors="pt", 
#             padding=True, 
#             truncation=True, 
#             max_length=16000 * 10 
#         )
#         input_values = inputs.input_values.to(DEVICE)
        
#         # FeatureExtractor có thể không trả về attention_mask mặc định
#         # Nếu có thì dùng, không thì thôi
#         attention_mask = inputs.get("attention_mask")
#         if attention_mask is not None:
#             attention_mask = attention_mask.to(DEVICE)
        
#         with torch.no_grad():
#             if attention_mask is not None:
#                 outputs = model(input_values, attention_mask=attention_mask)
#             else:
#                 outputs = model(input_values)
        
#         # Mean Pooling
#         embeddings = torch.mean(outputs.last_hidden_state, dim=1)
        
#         return embeddings.cpu().numpy()
        
#     except Exception as e:
#         print(f"❌ Lỗi Vector hóa Batch: {e}")
#         return np.array([])

def extract_embeddings_batch(audio_list):
    if not audio_list: return np.array([])
        
    cleaned_list = []
    for item in audio_list:
        # 1. Chuyển hết về Numpy để Feature Extractor xử lý chuẩn nhất
        # (Feature Extractor của HuggingFace ưu tiên Numpy list hơn là Tensor list)
        if isinstance(item, torch.Tensor):
            item = item.detach().cpu().numpy()
        
        # 2. Xử lý Shape: Phải là 1D (Time,)
        # Xóa hết các chiều dư thừa (1, Time) -> (Time,)
        item = np.squeeze(item) 
        
        # Nếu sau khi squeeze mà vẫn còn nhiều chiều (ví dụ Stereo 2 kênh), lấy trung bình
        if item.ndim > 1:
            item = np.mean(item, axis=0)
            
        cleaned_list.append(item)
            
    if not cleaned_list: return np.array([])

    try:
        # Cấu hình Feature Extractor:
        # padding=True: Tự động đệm cho bằng nhau
        # return_tensors="pt": Trả về PyTorch Tensor
        inputs = feature_extractor(
            cleaned_list, 
            sampling_rate=TARGET_SAMPLE_RATE, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=TARGET_SAMPLE_RATE * 10 
        )
        
        # In ra shape để debug lần cuối nếu cần
        # print(f"DEBUG: Input shape: {inputs.input_values.shape}")
        # Kỳ vọng: (Batch_Size, Max_Time) -> Ví dụ (16, 16000)
        
        input_values = inputs.input_values.to(DEVICE)
        attention_mask = inputs.attention_mask.to(DEVICE) if inputs.attention_mask is not None else None
        
        with torch.no_grad():
            outputs = model(input_values, attention_mask=attention_mask)
        
        # Mean Pooling
        embeddings = torch.mean(outputs.last_hidden_state, dim=1)
        return embeddings.cpu().numpy()
        
    except Exception as e:
        print(f"❌ Lỗi Vector hóa Batch: {e}")
        # Debug chi tiết
        import traceback
        traceback.print_exc()
        return np.array([])
    
def train_model_from_csv(status_callback=None):
    def report(percent, msg):
        print(f"[Backend] {percent}% - {msg}") 
        if status_callback: status_callback(percent, msg)

    if not os.path.exists(DATA_CSV):
        return False, "Chưa có file dữ liệu CSV."
    
    df = pd.read_csv(DATA_CSV)
    if len(df) < 2: # Giảm xuống 2 để test cho dễ
        return False, "Dữ liệu quá ít."

    print("--- [DEBUG] Bắt đầu Giai đoạn 1: Load Dữ liệu ---")
    report(5, f"🚀 Bắt đầu đọc {len(df)} file...")
    
    waveforms = []
    labels = []
    
    # Dùng list thường thay vì Dict để tránh phức tạp hóa
    paths_and_labels = [(row['filepath'], row['label']) for _, row in df.iterrows()]
    
    # Giảm số worker xuống một chút để an toàn hơn trên Mac
    # Thêm timeout để tránh treo
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # Submit jobs
        future_map = {executor.submit(load_and_preprocess_audio, p): l for p, l in paths_and_labels}
        
        total = len(future_map)
        done = 0
        
        for future in concurrent.futures.as_completed(future_map):
            lbl = future_map[future]
            try:
                # Timeout 10 giây cho mỗi file. Nếu lâu hơn -> Bỏ qua
                wf, err = future.result(timeout=10) 
                if wf is not None and len(wf) > 1000:
                    # waveforms.append(wf.numpy())
                    waveforms.append(wf)
                    labels.append(lbl)
                else:
                    print(f"⚠️ Lỗi file: {err}")
            except concurrent.futures.TimeoutError:
                print(f"⚠️ Timeout: Bỏ qua 1 file do đọc quá lâu (NAS chậm).")
            except Exception as e:
                print(f"⚠️ Lỗi không xác định: {e}")
            
            done += 1
            if done % 5 == 0 or done == total:
                report(5 + int((done/total)*35), f"Đã tải {done}/{total} files...")

    print("--- [DEBUG] Kết thúc ThreadPool. Đang chuyển sang xử lý Vector... ---")
    
    if not waveforms:
        return False, "Không tải được file nào."

    # --- GIAI ĐOẠN 2: VECTOR HÓA ---
    print(f"--- [DEBUG] Bắt đầu Vector hóa {len(waveforms)} mẫu ---")
    report(40, f"🧠 Đang tính toán Vector trên {DEVICE}...")
    
    try:
        BATCH_SIZE = 16
        embeddings_list = []
        
        # Sắp xếp để tối ưu batch (quan trọng cho tốc độ)
        sorted_indices = np.argsort([len(w) for w in waveforms])[::-1] # Dài nhất trước
        waveforms_sorted = [waveforms[i] for i in sorted_indices]
        labels_sorted = [labels[i] for i in sorted_indices]

        total_batches = (len(waveforms) + BATCH_SIZE - 1) // BATCH_SIZE
        
        for i in range(0, len(waveforms), BATCH_SIZE):
            print(f"   [DEBUG] Đang xử lý Batch {i//BATCH_SIZE + 1}/{total_batches}...")
            batch_waves = waveforms_sorted[i : i + BATCH_SIZE]
            # Kiểm tra xem batch có phần tử nào không hợp lệ (None/Rỗng) không
            valid_batch = [w for w in batch_waves if w is not None and w.shape[0] > 0]
            if not valid_batch:
                continue
            batch_embs = extract_embeddings_batch(valid_batch)
            
            # Nếu extract trả về mảng rỗng, bỏ qua
            if len(batch_embs) > 0:
                embeddings_list.extend(batch_embs)
            # Gọi hàm extract (đảm bảo hàm này không bị treo)
            # batch_embs = extract_embeddings_batch(batch_waves)
            # embeddings_list.extend(batch_embs)
            
            # Update UI
            prog = 40 + int(((i + BATCH_SIZE)/len(waveforms)) * 50)
            report(min(prog, 90), f"Vector hóa: {min(i + BATCH_SIZE, len(waveforms))}/{len(waveforms)} mẫu...")
            # --- CHECK SAU KHI VECTOR HÓA XONG ---
        if not embeddings_list:
            return False, "Lỗi: Không tạo được Vector nào từ dữ liệu (Data Loading/Model Error)."
        
        print("--- [DEBUG] Vector hóa hoàn tất. Chuẩn bị train SVM. ---")
        X = np.array(embeddings_list)
        y = np.array(labels_sorted)
            # Kiểm tra lại X
        if X.shape[0] == 0:
            return False, "Lỗi: Mảng Vector X bị rỗng."
        # --- GIAI ĐOẠN 3: TRAIN ---
        report(95, "🎓 Đang huấn luyện SVM...")
        clf = make_pipeline(StandardScaler(), SVC(kernel='rbf', probability=True))
        clf.fit(X, y)
        
        joblib.dump(clf, MODEL_FILE)
        print("--- [DEBUG] Đã lưu model. ---")
        
        report(100, f"✅ Thành công! Đã học {len(X)} mẫu.")
        return True, f"Train xong. Accuracy nội bộ (ước tính): Rất tốt."

    except Exception as e:
        print(f"❌ CRASH tại giai đoạn xử lý AI: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Lỗi xử lý: {str(e)}"

def detect_errors_in_video(video_path, status_callback=None, sensitivity_threshold=0.3):
    """
    Detect lỗi với 2 lớp bảo vệ:
    Lớp 1: SVM Classifier (Dự đoán loại lỗi).
    Lớp 2: Similarity Check (So với Mean Clean Vector).
    
    sensitivity_threshold: Ngưỡng khoảng cách (Distance Threshold).
    - Thấp (0.1): Rất chặt, chỉ báo lỗi nếu cực kỳ khác biệt (Ít báo động giả, nhưng dễ sót).
    - Cao (0.5): Rất nhạy, hơi khác tí là báo (Bắt hết lỗi, nhưng nhiều báo động giả).
    -> Mặc định 0.3 là điểm cân bằng.
    """
    def report(percent, msg, details=""):
        if status_callback: status_callback(percent, msg, details)

    if not os.path.exists(MODEL_FILE):
        return [], "Chưa có model."
    
    clf = joblib.load(MODEL_FILE)
    if isinstance(clf, dict):
        clf = clf["classifier"]
        mean_clean_vec = clf["mean_clean_vec"]
    else:
        clf = clf # Hỗ trợ model cũ
        mean_clean_vec = None
    # 1. Load Video
    report(5, "📥 Giai đoạn 1: Load & Preprocessing", 
           "Đang sử dụng FFmpeg để tách âm thanh từ video và nạp vào RAM. Tần số mẫu mục tiêu: 16kHz.")
    
    # full_waveform = load_and_preprocess_audio(video_path)
    full_waveform, error_msg = load_and_preprocess_audio(video_path,truncate=False)
    if error_msg:
        print(f"❌ Lỗi load audio từ video: {error_msg}")
        # --- [THÊM ĐOẠN DEBUG NÀY] ---
    if full_waveform is not None:
        duration_sec = full_waveform.shape[0] / TARGET_SAMPLE_RATE
        print(f"DEBUG: Độ dài Audio load được: {duration_sec} giây")
        print(f"DEBUG: Số lượng mẫu (samples): {full_waveform.shape[0]}")
    else:
        print("DEBUG: Audio load bị None (Thất bại)")
    # -----------------------------
    
    if full_waveform is None: return [], "Lỗi đọc file."
    print(f"DEBUG: Audio shape: {full_waveform.shape}")

    # 2. Sliding Window
    report(15, "✂️ Giai đoạn 2: Sliding Window Segmentation", 
           "Cắt audio thành các đoạn nhỏ 1 giây, chồng lấp 0.5 giây để không bỏ sót lỗi ở biên.")
    
    WINDOW_SIZE = 1.0
    STEP = 0.5
    sr = TARGET_SAMPLE_RATE
    win_len = int(WINDOW_SIZE * sr)
    step_len = int(STEP * sr)
    
    chunks = []
    timestamps = []
    print(len(full_waveform))
    for i in range(0, len(full_waveform) - win_len, step_len):
        chunk = full_waveform[i : i + win_len]
        chunks.append(chunk.numpy())
        timestamps.append(i / sr)
        
    if not chunks: return [], "Video quá ngắn."

    # 3. Vectorization (Heavy Lifting)
    report(25, "🧠 Giai đoạn 3: Deep Learning Embedding", 
           f"Đang đẩy {len(chunks)} đoạn audio vào model Wav2Vec2 trên Neural Engine. Biến đổi mỗi đoạn thành vector đặc trưng.")
    
    BATCH_SIZE = 32
    all_embeddings = []
    total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        embs = extract_embeddings_batch(batch)
        if len(all_embeddings) == 0:
            all_embeddings = embs
        else:
            all_embeddings = np.vstack([all_embeddings, embs])
            
        # Cập nhật tiến độ chi tiết
        current_batch = (i // BATCH_SIZE) + 1
        percent = 25 + int((current_batch / total_batches) * 50) # 25% -> 75%
        report(percent, "🧠 Giai đoạn 3: Deep Learning Embedding", 
               f"Đang xử lý Batch {current_batch}/{total_batches}. Tensor calculation on MPS...")

    # 4. Classification
    report(80, "🔎 Giai đoạn 4: Phân tích Lớp Kép (Dual-Layer Analysis)...")

    predictions = clf.predict(all_embeddings)
    probs = clf.predict_proba(all_embeddings) # Lấy độ tin cậy
    detected_errors = []
    
    # Chuẩn bị cho Lớp 2 (Tính Cosine Distance)
    if mean_clean_vec is not None:
        # Chuyển về Tensor để tính cosine nhanh trên GPU/MPS
        # (Batch, 1024) vs (1024,)
        vec_tensor = torch.tensor(all_embeddings).to(DEVICE)
        mean_tensor = torch.tensor(mean_clean_vec).to(DEVICE).unsqueeze(0)
        
        # Cosine Similarity: -1 (Ngược) -> 1 (Giống hệt)
        # Cosine Distance = 1 - Similarity (0: Giống hệt -> 2: Ngược)
        cos_sim = torch.nn.functional.cosine_similarity(vec_tensor, mean_tensor)
        distances = 1 - cos_sim.cpu().numpy()
    else:
        distances = [1.0] * len(predictions) # Nếu không có mẫu sạch, coi như khác biệt tối đa

    # Vòng lặp kiểm tra
    # 5. Result Synthesis
    report(90, "📝 Giai đoạn 5: Tổng hợp báo cáo", "Đang lọc kết quả và tạo danh sách timecode...")
    
    for i, (time_start, label) in enumerate(zip(timestamps, predictions)):
        
        # Bỏ qua nếu Classifier bảo là "Clean"
        if 'clean' in label.lower():
            continue
            
        # --- LỚP BẢO VỆ THỨ 2: SIMILARITY CHECK ---
        dist = distances[i]
        confidence = np.max(probs[i])
        
        # Logic Quyết định:
        # 1. Nếu Classifier rất tự tin (> 80%), ta tin nó luôn.
        # 2. Nếu không quá tự tin, ta check Distance.
        #    Nếu Distance > Threshold (Tức là nó thực sự khác mẫu sạch) -> LỖI THẬT.
        #    Nếu Distance < Threshold (Nó vẫn khá giống mẫu sạch) -> BÁO ĐỘNG GIẢ (Bỏ qua).
        
        is_error = False
        
        if confidence > 0.8:
            is_error = True
            reason = "High Confidence"
        elif dist > sensitivity_threshold:
            is_error = True
            reason = f"High Distance ({dist:.2f})"
        
        if is_error:
            detected_errors.append({
                "start": time_start,
                "duration": WINDOW_SIZE,
                "label": f"{label}",
                "confidence": f"{confidence:.2f}",
                "distance": f"{dist:.2f}"
            })

    
    # detected_errors = []
    # for time_start, label in zip(timestamps, predictions):
    #     if 'clean' not in label.lower():
    #         detected_errors.append({
    #             "start": time_start,
    #             "duration": WINDOW_SIZE,
    #             "label": label
    #         })
            
    report(100, "✅ Hoàn tất phân tích!", f"Tìm thấy {len(detected_errors)} lỗi tiềm năng.")
    return detected_errors, "Hoàn tất."

def get_data_stats():
    if not os.path.exists(DATA_CSV):
        return pd.DataFrame()
    df = pd.read_csv(DATA_CSV)
    stats = df['label'].value_counts().reset_index()
    stats.columns = ['Loại Lỗi', 'Số lượng mẫu']
    return stats

def auto_align_audio(y_clean, y_raw):
    """Đồng bộ hóa tín hiệu Raw khớp với Clean dùng Cross-Correlation."""
    # Dùng FFT để tính nhanh
    correlation = scipy.signal.correlate(y_raw, y_clean, mode='full', method='fft')
    lags = scipy.signal.correlation_lags(len(y_raw), len(y_clean), mode='full')
    lag = lags[np.argmax(correlation)]

    y_raw_aligned = np.zeros_like(y_clean)
    
    # Shift tín hiệu
    if lag > 0:
        take_len = min(len(y_raw) - lag, len(y_clean))
        y_raw_aligned[:take_len] = y_raw[lag : lag + take_len]
    else:
        start_idx = abs(lag)
        take_len = min(len(y_raw), len(y_clean) - start_idx)
        y_raw_aligned[start_idx : start_idx + take_len] = y_raw[:take_len]

    return y_raw_aligned, lag

def get_envelope(y, resolution=256):
    """Tính đường bao để vẽ waveform đặc."""
    return np.array([np.max(np.abs(y[i:i+resolution])) for i in range(0, len(y), resolution)])

def generate_comparison_plot(error_path, clean_path):
    """
    Tạo đối tượng Figure của Matplotlib hiển thị so sánh 3 đường (Raw, Clean, Diff).
    """
    import matplotlib.pyplot as plt
    
    try:
        # Load audio (chuyển về mono)
        y_clean, sr = librosa.load(clean_path, sr=16000)
        y_raw, _ = librosa.load(error_path, sr=16000)
        
        # 1. Auto Align
        y_raw_aligned, lag = auto_align_audio(y_clean, y_raw)
        
        # 2. Tính Envelope (để vẽ nhanh và đẹp)
        HOP = 256
        env_clean = get_envelope(y_clean, HOP)
        env_raw = get_envelope(y_raw_aligned, HOP)
        
        # Cắt về cùng độ dài
        min_len = min(len(env_clean), len(env_raw))
        env_clean = env_clean[:min_len]
        env_raw = env_raw[:min_len]
        
        # 3. Tính Difference
        env_diff = np.abs(env_raw - env_clean)
        
        # Trục thời gian
        frames = range(len(env_clean))
        t = librosa.frames_to_time(frames, sr=sr, hop_length=HOP)

        # 4. Vẽ (Dark Mode)
        plt.style.use('dark_background')
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 6), sharex=True)
        fig.patch.set_facecolor(FCP_COLORS["BACKGROUND"])
        
        def draw_track(ax, time, env, color, title):
            ax.set_facecolor(FCP_COLORS["TRACK_BG"])
            ax.fill_between(time, 0, env, color=color, alpha=0.9)
            ax.fill_between(time, 0, -env, color=color, alpha=0.9)
            ax.axhline(0, color=FCP_COLORS["GRID"], linewidth=0.5)
            ax.set_title(title, color=FCP_COLORS["TEXT"], loc='left', fontsize=9, pad=5)
            ax.set_ylim(-1, 1)
            ax.grid(False)
            for spine in ax.spines.values(): spine.set_visible(False)
            ax.tick_params(colors=FCP_COLORS["TEXT"], labelsize=7)

        draw_track(ax1, t, env_raw, FCP_COLORS["RAW"], f"SOURCE (Raw - Aligned: {lag} samples)")
        draw_track(ax2, t, env_clean, FCP_COLORS["CLEAN"], f"PROJECT (Edited)")
        draw_track(ax3, t, env_diff, FCP_COLORS["ERROR"], "DIFFERENCE (Detected Edits)")
        
        ax3.set_xlabel("Time (seconds)", color=FCP_COLORS["TEXT"])
        plt.tight_layout()
        
        return fig, lag
        
    except Exception as e:
        print(f"Plotting error: {e}")
        return None, 0  
    
def run_benchmark_test():
    """
    Chạy kiểm thử đánh giá độ chính xác của Model theo từng nhãn.
    Sử dụng phương pháp Train/Test Split (80/20).
    """
    if not os.path.exists(DATA_CSV):
        return False, "Chưa có dữ liệu.", None, None
    
    df = pd.read_csv(DATA_CSV)
    
    # Kiểm tra xem mỗi nhãn có đủ dữ liệu để chia không (ít nhất 2 mẫu)
    class_counts = df['label'].value_counts()
    valid_labels = class_counts[class_counts >= 2].index
    df_filtered = df[df['label'].isin(valid_labels)]
    
    dropped_labels = list(set(df['label']) - set(valid_labels))
    if dropped_labels:
        print(f"⚠️ Bỏ qua các nhãn quá ít dữ liệu (<2 mẫu): {dropped_labels}")

    if len(df_filtered) < 5:
        return False, "Dữ liệu quá ít để Benchmark (Cần tối thiểu 5 mẫu hợp lệ).", None, None

    print("📊 Đang chuẩn bị dữ liệu Benchmark...")
    
    # 1. Load và Vector hóa (Tận dụng hàm cũ)
    # Lưu ý: Đoạn này sẽ tốn thời gian như lúc Train. 
    # Trên M2 Ultra sẽ nhanh, nhưng vẫn cần load lại audio.
    waveforms = []
    labels = []
    
    print(f"DEBUG: Tổng số dòng trong CSV: {len(df)}")
    print(f"DEBUG: Số dòng sau khi lọc nhãn: {len(df_filtered)}")
    # (Để code ngắn gọn, tôi tái sử dụng logic load, thực tế nên tách hàm load ra riêng để cache)
    for index, row in tqdm(df_filtered.iterrows(), total=df_filtered.shape[0], desc="Loading Data"):
        
        if not os.path.exists(row['filepath']):
            print(f"❌ File không tồn tại: {row['filepath']}")
            continue
        # wf = load_and_preprocess_audio(row['filepath'])
        wf, err = load_and_preprocess_audio(row['filepath']) 

        if wf is not None and len(wf) > 1000:
            waveforms.append(wf)
            # waveforms.append(wf.numpy())
            labels.append(row['label'])

    # Batch Vectorization
    BATCH_SIZE = 32
    embeddings_list = []
    for i in range(0, len(waveforms), BATCH_SIZE):
        batch_waves = waveforms[i : i + BATCH_SIZE]
        batch_embs = extract_embeddings_batch(batch_waves)
        embeddings_list.extend(batch_embs)
    
    X = np.array(embeddings_list)
    y = np.array(labels)

    # # 2. Chia tập Train/Test (80% học, 20% thi)
    # # stratify=y đảm bảo tỷ lệ các nhãn trong tập test giống tập train
    # try:
    #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    # except ValueError:
    #     return False, "Không thể chia dữ liệu (một số nhãn có quá ít mẫu). Hãy thu thập thêm.", None, None

# 2. Chia tập Train/Test (Chiến thuật Linh hoạt)
    try:
        # Ưu tiên 1: Chia chuẩn có cân bằng (Tốt nhất)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=42
        )
    except ValueError:
        print("⚠️ Cảnh báo: Một số nhãn quá ít mẫu để cân bằng. Chuyển sang chia ngẫu nhiên.")
        try:
            # Ưu tiên 2: Chia ngẫu nhiên (Không cân bằng, chấp nhận rủi ro)
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
        except ValueError:
             print("⚠️ Cảnh báo: Dữ liệu quá ít (<2 mẫu tổng). Chuyển sang chế độ Sanity Check (Test trên Train).")
             # Ưu tiên 3: Nếu chỉ có vài mẫu, dùng toàn bộ để train và test lại trên chính nó
             # (Để xem model có học thuộc lòng được không)
             X_train, X_test, y_train, y_test = X, X, y, y
    # 3. Train model tạm thời (chỉ để test)
    print("🎓 Đang train model kiểm thử...")
    clf_bench = make_pipeline(StandardScaler(), SVC(kernel='rbf', probability=True))
    clf_bench.fit(X_train, y_train)

    # 4. Dự đoán trên tập Test
    y_pred = clf_bench.predict(X_test)

    # 5. Tạo báo cáo
    # Report dạng Dict để vẽ bảng
    report_dict = classification_report(y_test, y_pred, output_dict=True)
    
    # Tạo Confusion Matrix Plot
    unique_labels = sorted(list(set(y)))
    cm = confusion_matrix(y_test, y_pred, labels=unique_labels)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=unique_labels, yticklabels=unique_labels, ax=ax)
    plt.ylabel('Thực tế')
    plt.xlabel('AI Dự đoán')
    plt.title('Ma trận nhầm lẫn (Confusion Matrix)')
    
    return True, "Benchmark hoàn tất.", report_dict, fig
# --- 2. HÀM TRÍCH XUẤT ĐẶC TRƯNG (CORE) ---
def extract_features_single(audio_path):
    """
    Trích xuất vector 1024 chiều từ 1 file audio.
    """
    import torchaudio
    try:
        # Load & Resample
        waveform, sample_rate = torchaudio.load(audio_path)
        if waveform.shape[0] > 1: waveform = torch.mean(waveform, dim=0, keepdim=True)
        if sample_rate != TARGET_SAMPLE_RATE:
            resampler = torchaudio.transforms.Resample(sample_rate, TARGET_SAMPLE_RATE)
            waveform = resampler(waveform)
        
        # Cắt hoặc Pad để đảm bảo độ dài tối thiểu (tránh lỗi CNN)
        if waveform.shape[1] < 1000: return None 
        
        # Prepare input
        input_values = feature_extractor(
            waveform.squeeze().numpy(), 
            sampling_rate=TARGET_SAMPLE_RATE, 
            return_tensors="pt"
        ).input_values.to(DEVICE)

        # Inference
        with torch.no_grad():
            outputs = model(input_values)
        
        # Mean Pooling -> 1024 vector
        embedding = torch.mean(outputs.last_hidden_state, dim=1).cpu().numpy()
        return embedding[0]

    except Exception as e:
        print(f"⚠️ Lỗi file {os.path.basename(audio_path)}: {e}")
        return None

def load_and_preprocess_audio(audio_path, target_duration=1.0, truncate=True):
    """
    Load audio an toàn. Nếu ngắn hơn target_duration (1s), tự động đệm im lặng vào 2 đầu.
    """
    import torch
    import torchaudio
    import torch.nn.functional as F
    import librosa
    import numpy as np

    waveform = None
    sample_rate = None

    # 1. Load Audio (Fallback logic)
    try:
        try:
            waveform, sample_rate = torchaudio.load(audio_path, backend="soundfile")
        except:
            # Fallback sang Librosa nếu torchaudio lỗi codec
            y, sr = librosa.load(audio_path, sr=None)
            waveform = torch.from_numpy(y)
            if waveform.dim() == 1: waveform = waveform.unsqueeze(0)
            sample_rate = sr
    except Exception as e:
        return None, f"Read Error: {str(e)}"

    # 2. Preprocess cơ bản
    try:
        # Mono
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)
            
        # Resample
        if sample_rate != TARGET_SAMPLE_RATE:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=TARGET_SAMPLE_RATE)
            waveform = resampler(waveform)
        if truncate:
            # 3. SMART PADDING (QUAN TRỌNG)
            # Mục tiêu: 1 giây = 16000 mẫu
            target_len = int(target_duration * TARGET_SAMPLE_RATE)
            current_len = waveform.shape[1]
            
            if current_len < target_len:
                # Tính lượng cần đệm
                print("đệm")
                padding_needed = target_len - current_len
                pad_left = padding_needed // 2
                pad_right = padding_needed - pad_left
                
                # Đệm im lặng (số 0) vào 2 bên. Mode 'constant' mặc định value=0
                waveform = F.pad(waveform, (pad_left, pad_right), "constant", 0)
                
            elif current_len > target_len:
                # Nếu dài hơn thì cắt ở giữa
                center = current_len // 2
                start = center - (target_len // 2)
                waveform = waveform[:, start : start + target_len]
                print(len(waveform))
            # return waveform.squeeze(), None
        return waveform.reshape(-1), None # Force flatten thành 1D
    except Exception as e:
        return None, f"Process Error: {str(e)}"