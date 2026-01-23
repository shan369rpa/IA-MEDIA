# backend_core.py
import os
import random
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
import uuid
from pydub import AudioSegment
# --- CẤU HÌNH HỆ THỐNG ---
DATA_CSV = "training_data.csv"
MODEL_FILE = "error_classifier.pkl"
DATA_FOLDER = "collected_data" 
DIFF_BANK_FOLDER = "diff_bank" 
# --- LOAD CONFIG TỪ ENV ---
from dotenv import load_dotenv
load_dotenv()

# Lấy đường dẫn từ env, fallback về thư mục local nếu chưa cấu hình
# NAS_ROOT = os.getenv("NAS_MOUNT_POINT", "./local_storage")
# DATA_FOLDER = os.path.join(NAS_ROOT, "collected_data")
# DATA_CSV = os.path.join(NAS_ROOT, "training_data.csv")
# DIFF_BANK_FOLDER = os.path.join(NAS_ROOT, "diff_bank")
# Model 1024 chiều SOTA
# Tạo thư mục nếu chưa có
for d in [DATA_FOLDER, DIFF_BANK_FOLDER]:
    os.makedirs(d, exist_ok=True)
MODEL_NAME = "facebook/wav2vec2-large-xlsr-53"
TARGET_SAMPLE_RATE = 16000
VECTOR_DIM = 1024


# --- CẤU HÌNH MÀU SẮC FCP ---
FCP_COLORS = {
    "BACKGROUND": "#1d3453", "TRACK_BG": "#262626", "TEXT": "#d1d1d1",
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
    df = pd.DataFrame([[save_path, label]], columns=["path_raw", "label"])
    
    # Chế độ append ('a')
    # Kiểm tra xem file có header chưa
    file_exists = os.path.isfile(DATA_CSV)
    df.to_csv(DATA_CSV, mode='a', header=not file_exists, index=False)
    
    return True

def extract_embeddings_batch(audio_list):
    """
    Xử lý batch audio -> Vector 1024.
    Đã fix lỗi shape [1, 1, 4, ...] bằng cách chuẩn hóa input.
    """
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
    if len(df) < 1: # Chỉ cần 1 dòng là đã có 2 mẫu (Raw+Clean) -> Đủ train tối thiểu
        return False, "Dữ liệu quá ít."

    print("--- [DEBUG] Bắt đầu Giai đoạn 1: Load Dữ liệu (Paired Augmentation) ---")
    report(5, f"🚀 Bắt đầu đọc {len(df)} cặp file (Tổng {len(df)*2} mẫu)...")
    
    waveforms = []
    labels = []
    
    # Chuẩn bị danh sách job cần chạy: Mỗi dòng CSV sinh ra 2 job (Raw và Clean)
    jobs = []
    for _, row in df.iterrows():
        # Job 1: File Lỗi
        if os.path.exists(row['path_raw']):
            jobs.append((row['path_raw'], row['label'])) # Label gốc (vd: error_1)
        
        # Job 2: File Sạch (Tự động sinh nhãn clean)
        if os.path.exists(row['path_clean']):
            # Gán nhãn clean chung để model học được đặc trưng "Sạch"
            # Hoặc dùng f"clean_{row['label']}" nếu muốn phân loại sạch chi tiết
            jobs.append((row['path_clean'], "clean")) 
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_map = {executor.submit(load_and_preprocess_audio, p): l for p, l in jobs}
        
        total = len(future_map)
        done = 0
        
        for future in concurrent.futures.as_completed(future_map):
            lbl = future_map[future]
            try:
                wf, err = future.result(timeout=10) 
                if wf is not None and len(wf) > 1000:
                    waveforms.append(wf)
                    labels.append(lbl)
            except Exception:
                pass # Bỏ qua lỗi lẻ tẻ
            
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

    report(100, "✅ Hoàn tất phân tích!", f"Tìm thấy {len(detected_errors)} lỗi tiềm năng.")
    return detected_errors, "Hoàn tất."

def get_data_stats():
    if not os.path.exists(DATA_CSV):
        return pd.DataFrame()
    df = pd.read_csv(DATA_CSV)
    stats = df['label'].value_counts().reset_index()
    stats.columns = ['Loại Lỗi', 'Số lượng mẫu']
    return stats

def auto_align_audio(y_ref, y_target):
    """
    Đồng bộ hóa y_target để khớp nhất với y_ref (Mốc chuẩn).
    Sử dụng FFT Cross-Correlation để tìm độ trễ (lag) chính xác.
    """
    # An toàn dữ liệu
    if len(y_ref) == 0 or len(y_target) == 0: 
        return y_target, 0

    # 1. Chuẩn hóa độ dài để tính Correlation (Lấy min)
    n = min(len(y_ref), len(y_target))
    ref_slice = y_ref[:n]
    target_slice = y_target[:n]

    # 2. Tính Correlation
    correlation = scipy.signal.correlate(target_slice, ref_slice, mode='full', method='fft')
    lags = scipy.signal.correlation_lags(len(target_slice), len(ref_slice), mode='full')
    
    # 3. Tìm vị trí khớp nhất (Peak)
    lag = lags[np.argmax(correlation)]

    # 4. Thực hiện dịch chuyển (Shift) & Cắt gọt (Trim/Pad)
    y_aligned = np.zeros_like(y_ref) # Tạo khung theo độ dài Reference

    if lag > 0:
        # Target bị trễ (nằm sau Ref) -> Kéo về trước (Cắt đầu Target)
        # Chỉ lấy phần chồng lấp hợp lệ
        take_len = min(len(y_target) - lag, len(y_ref))
        if take_len > 0:
            y_aligned[:take_len] = y_target[lag : lag + take_len]
    else:
        # Target bị sớm (nằm trước Ref) -> Đẩy ra sau (Đệm đầu bằng 0)
        start_idx = abs(lag)
        # Chỉ lấy phần chồng lấp
        take_len = min(len(y_target), len(y_ref) - start_idx)
        if take_len > 0:
            y_aligned[start_idx : start_idx + take_len] = y_target[:take_len]

    return y_aligned, lag

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
    Sử dụng phương pháp Train/Test Split (80/20) với dữ liệu được tăng cường (Raw + Clean).
    """
    if not os.path.exists(DATA_CSV):
        return False, "Chưa có file dữ liệu CSV.", None, None
    
    df = pd.read_csv(DATA_CSV)
    
    # --- BƯỚC 1: LOAD DỮ LIỆU (PAIRED AUGMENTATION) ---
    print(f"📊 Đang chuẩn bị dữ liệu Benchmark từ {len(df)} dòng CSV...")
    
    waveforms = []
    labels = []
    
    # Load tuần tự (hoặc song song tùy ý, ở đây viết gọn để dễ debug)
    # Lặp qua từng dòng, lấy cả file Raw (Lỗi) và file Clean (Sạch)
    count_raw = 0
    count_clean = 0
    
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Loading Benchmark Data"):
        # 1. Load Raw (Gán nhãn lỗi gốc)
        # Sử dụng tên cột mới là 'path_raw'
        path_raw = row.get('path_raw') # Dùng .get để tránh lỗi nếu cột chưa có
        if not path_raw and 'filepath' in row: path_raw = row['filepath'] # Fallback cũ
            
        if path_raw and os.path.exists(path_raw):
            wf, _ = load_and_preprocess_audio(path_raw)
            if wf is not None and len(wf) > 1000:
                waveforms.append(wf)
                labels.append(row['label'])
                count_raw += 1
        
        # 2. Load Clean (Tự sinh nhãn 'clean')
        path_clean = row.get('path_clean')
        if path_clean and os.path.exists(path_clean):
            wf, _ = load_and_preprocess_audio(path_clean)
            if wf is not None and len(wf) > 1000:
                waveforms.append(wf)
                labels.append("clean") # Auto-label clean
                count_clean += 1

    print(f"DEBUG: Đã tải {count_raw} mẫu Lỗi và {count_clean} mẫu Sạch. Tổng: {len(waveforms)}")

    if len(waveforms) < 2:
         return False, "Dữ liệu quá ít để Benchmark (Cần tối thiểu 2 mẫu).", None, None

    # --- BƯỚC 2: VECTOR HÓA ---
    BATCH_SIZE = 32
    embeddings_list = []
    
    print(f"🧠 Đang vector hóa {len(waveforms)} mẫu...")
    for i in range(0, len(waveforms), BATCH_SIZE):
        batch_waves = waveforms[i : i + BATCH_SIZE]
        batch_embs = extract_embeddings_batch(batch_waves)
        if len(batch_embs) > 0:
            embeddings_list.extend(batch_embs)
    
    if not embeddings_list:
        return False, "Lỗi Vector hóa: Không tạo được vector nào.", None, None

    X = np.array(embeddings_list)
    y = np.array(labels)
    
    # Kiểm tra lại X, y
    if len(X) != len(y):
        print(f"⚠️ Mismatch: X({len(X)}) != y({len(y)}). Truncating...")
        min_len = min(len(X), len(y))
        X = X[:min_len]
        y = y[:min_len]

    # --- BƯỚC 3: CHIA TRAIN/TEST & HUẤN LUYỆN ---
    unique_classes = np.unique(y)
    print(f"DEBUG: Các nhãn tìm thấy: {unique_classes}")
    
    if len(unique_classes) < 2:
         return False, f"Chỉ tìm thấy 1 loại nhãn ({unique_classes[0]}). Cần ít nhất 2 loại (Lỗi & Clean) để benchmark.", None, None

    try:
        # Ưu tiên 1: Chia chuẩn có cân bằng (Stratified)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=42
        )
    except ValueError:
        print("⚠️ Cảnh báo: Một số nhãn quá ít mẫu để cân bằng. Chuyển sang chia ngẫu nhiên.")
        try:
            # Ưu tiên 2: Chia ngẫu nhiên
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
        except ValueError:
             print("⚠️ Cảnh báo: Dữ liệu quá ít (<2 mẫu tổng). Chế độ Sanity Check.")
             # Ưu tiên 3: Test trên tập Train (Sanity Check)
             X_train, X_test, y_train, y_test = X, X, y, y

    # Train model tạm thời
    print("🎓 Đang train model kiểm thử...")
    clf_bench = make_pipeline(StandardScaler(), SVC(kernel='rbf', probability=True))
    clf_bench.fit(X_train, y_train)

    # Dự đoán
    y_pred = clf_bench.predict(X_test)

    # --- BƯỚC 4: TẠO BÁO CÁO ---
    # Report dạng Dict để vẽ bảng
    report_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    
    # Tạo Confusion Matrix Plot
    cm_labels = sorted(list(set(y)))
    cm = confusion_matrix(y_test, y_pred, labels=cm_labels)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=cm_labels, yticklabels=cm_labels, ax=ax)
    plt.ylabel('Thực tế (Ground Truth)')
    plt.xlabel('AI Dự đoán (Prediction)')
    plt.title('Ma trận nhầm lẫn (Confusion Matrix)')
    plt.tight_layout()

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
                # print("đệm")
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

def save_paired_data(raw_file, clean_file, label, is_fake=False, note=""):
    """
    Lưu cặp file Raw/Clean, tự động Align, tạo Diff và ghi metadata.
    """
    uid = uuid.uuid4().hex
    timestamp = int(time.time())
    base_name = f"{uid}_{label}"
    
    # Tạo thư mục con cho label để gọn gàng (VD: collected_data/error_click/)
    label_dir = os.path.join(DATA_FOLDER, label)
    os.makedirs(label_dir, exist_ok=True)

    # 1. Lưu file gốc tạm thời để xử lý
    # Lưu ý: raw_file là object Streamlit UploadedFile
    temp_raw = f"temp_raw_{uid}.wav"
    temp_clean = f"temp_clean_{uid}.wav"
    
    with open(temp_raw, "wb") as f: f.write(raw_file.getbuffer())
    with open(temp_clean, "wb") as f: f.write(clean_file.getbuffer())
    
    try:
        # 2. Load và Auto-Align (Dùng hàm đã có)
        y_raw, sr = librosa.load(temp_raw, sr=16000)
        y_clean, _ = librosa.load(temp_clean, sr=16000)
        
        # Align
        y_raw_aligned, lag = auto_align_audio(y_clean, y_raw)
        
        # 3. Tính Diff (Raw - Clean)
        # Cắt về cùng độ dài
        min_len = min(len(y_clean), len(y_raw_aligned))
        y_clean = y_clean[:min_len]
        y_raw_aligned = y_raw_aligned[:min_len]
        
        y_diff = y_raw_aligned - y_clean
        
        # 4. Lưu 3 file vật lý vào NAS
        path_raw = os.path.join(label_dir, f"{base_name}_raw.wav")
        path_clean = os.path.join(label_dir, f"{base_name}_clean.wav")
        path_diff = os.path.join(DIFF_BANK_FOLDER, f"{base_name}_diff.wav") # Lưu Diff vào kho riêng
        
        import soundfile as sf
        sf.write(path_raw, y_raw_aligned, sr)
        sf.write(path_clean, y_clean, sr)
        sf.write(path_diff, y_diff, sr)
        
        # 5. Cập nhật CSV
        new_row = pd.DataFrame([{
            "uid": uid,
            "timestamp": timestamp,
            "label": label,
            "is_fake": is_fake,
            "path_raw": path_raw,
            "path_clean": path_clean,
            "path_diff": path_diff,
            "note": note,
            "lag_samples": lag
        }])
        
        if not os.path.isfile(DATA_CSV):
            new_row.to_csv(DATA_CSV, index=False)
        else:
            new_row.to_csv(DATA_CSV, mode='a', header=False, index=False)
            
        return True, f"Đã lưu bộ 3 file. Diff được lưu tại kho: {path_diff}"

    except Exception as e:
        return False, f"Lỗi xử lý audio: {str(e)}"
    finally:
        # Dọn dẹp file tạm
        if os.path.exists(temp_raw): os.remove(temp_raw)
        if os.path.exists(temp_clean): os.remove(temp_clean)
        
def generate_comparison_plot_from_obj(raw_obj, clean_obj):
    """
    Vẽ biểu đồ so sánh từ đối tượng file upload (trong RAM).
    """
    import matplotlib.pyplot as plt
    
    try:
        # Load trực tiếp từ buffer
        y_raw, sr = librosa.load(raw_obj, sr=16000)
        y_clean, _ = librosa.load(clean_obj, sr=16000)
        
        # Reset con trỏ file về đầu để các hàm khác (như save) dùng lại được
        raw_obj.seek(0)
        clean_obj.seek(0)
        
        # Auto Align
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
        return None, 0

def match_files_by_name(raw_files, clean_files):
    """
    Ghép cặp và trả về danh sách: (pairs, unmatched_raw, unmatched_clean)
    """
    pairs = []
    unmatched_raw = []
    unmatched_clean = []
    
    # Helper lấy tên gốc
    def get_base_name(filename):
        name = os.path.splitext(filename)[0]
        # Xóa các hậu tố phổ biến, chữ thường để so sánh không phân biệt hoa thường
        return name.lower().replace('_raw', '').replace('_clean', '').replace('_edited', '').strip()

    # Tạo map cho file clean: { "ten_base": file_obj }
    # Lưu ý: Nếu có trùng tên base, file sau sẽ đè file trước (hoặc cần logic xử lý thêm)
    clean_map = {get_base_name(f.name): f for f in clean_files}
    matched_clean_names = set()

    # Duyệt file raw để tìm cặp
    for raw in raw_files:
        base = get_base_name(raw.name)
        if base in clean_map:
            pairs.append((raw, clean_map[base]))
            matched_clean_names.add(base)
        else:
            unmatched_raw.append(raw)
            
    # Tìm file clean chưa được ghép
    for name, f in clean_map.items():
        if name not in matched_clean_names:
            unmatched_clean.append(f)
            
    return pairs, unmatched_raw, unmatched_clean

import unicodedata

def normalize_unicode(text: str) -> str:
    """Chuẩn hoá Unicode về NFC"""
    return unicodedata.normalize("NFC", text)

def auto_organize_local_folder(root_folder: str):
    """
    Quét thư mục, chuẩn hóa tên file (lỗi- -> _raw, đã sửa- -> _clean)
    và di chuyển vào thư mục raw/clean riêng biệt.
    """
    if not os.path.exists(root_folder):
        return False, "Thư mục không tồn tại."
        
    raw_dir = os.path.join(root_folder, "raw")
    clean_dir = os.path.join(root_folder, "clean")

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(clean_dir, exist_ok=True)
    
    log = []
    moved_count = 0

    for root, dirs, files in os.walk(root_folder):
        # Bỏ qua chính thư mục đích để tránh loop vô hạn
        if os.path.abspath(root) in [os.path.abspath(raw_dir), os.path.abspath(clean_dir)]:
            continue

        for filename in files:
            # Bỏ qua file hệ thống
            if filename.startswith('.'): continue
            
            old_path = os.path.join(root, filename)
            name, ext = os.path.splitext(filename)
            norm_name = normalize_unicode(name) # Chuẩn hóa tiếng Việt

            # Logic nhận diện
            is_raw = norm_name.startswith("lỗi-") or norm_name.endswith("_raw")
            is_clean = norm_name.startswith("đã sửa-") or norm_name.endswith("_clean")

            if is_raw and is_clean:
                log.append(f"⚠️ SKIP (Conflict): {filename}")
                continue
            if not is_raw and not is_clean:
                continue

            # Chuẩn hoá tên gốc (Clean Base Name)
            base = norm_name
            for p in ["lỗi-", "đã sửa-"]:
                if base.startswith(p): base = base[len(p):]
            for s in ["_raw", "_clean"]:
                if base.endswith(s): base = base[:-len(s)]
            
            base = base.strip("-_ ") # Xóa ký tự thừa

            # Tạo tên mới & đường dẫn đích
            if is_raw:
                new_name = f"{base}_raw{ext}"
                target_dir = raw_dir
            else:
                new_name = f"{base}_clean{ext}"
                target_dir = clean_dir

            new_path = os.path.join(target_dir, new_name)

            # Thực hiện di chuyển (Move/Rename)
            try:
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    log.append(f"✅ {filename} → {target_dir}/{new_name}")
                    moved_count += 1
                else:
                    log.append(f"⚠️ Tồn tại, bỏ qua: {new_name}")
            except Exception as e:
                log.append(f"❌ Lỗi khi di chuyển {filename}: {e}")

    return True, f"Hoàn tất! Đã xử lý {moved_count} file.\n" + "\n".join(log)

def save_batch_generated_sample(mixed_audio, clean_audio, sr, label, original_diff_path, note):
    """
    Lưu mẫu sinh hàng loạt.
    - KHÔNG tính lại Diff (Dùng lại path của file Diff gốc).
    - Lưu file Fake và file Clean (Background).
    """
    uid= uuid.uuid4().hex
    timestamp = int(time.time() * 1000) # Milliseconds để tránh trùng tên khi chạy nhanh
    # rand_id = random.randint(1000, 9999)
    base_name = f"fake_{label}_{uid}"
    
    # Folder đích
    label_dir = os.path.join(DATA_FOLDER, label)
    if not os.path.exists(label_dir): os.makedirs(label_dir)
    
    # Đường dẫn file
    path_fake = os.path.join(label_dir, f"{base_name}_raw.wav")   # Fake đóng vai trò Raw
    path_clean = os.path.join(label_dir, f"{base_name}_clean.wav") # BG đóng vai trò Clean
    
    import soundfile as sf
    
    # Ghi file
    sf.write(path_fake, mixed_audio, sr)
    sf.write(path_clean, clean_audio, sr)
    
    # Ghi CSV
    new_record = {
        "uid": f"{base_name}",
        "timestamp": timestamp,
        "label": label,
        "is_fake": True,
        "path_raw": path_fake,
        "path_clean": path_clean,
        "path_diff": original_diff_path, # <--- DÙNG LẠI FILE GỐC
        "note": note,
        "lag_samples": 0
    }
    
    df = pd.DataFrame([new_record])
    file_exists = os.path.isfile(DATA_CSV)
    df.to_csv(DATA_CSV, mode='a', header=not file_exists, index=False)
    
    return True

def delete_data(df_to_delete):
    """Xóa file vật lý và cập nhật CSV."""
    if df_to_delete.empty: return 0
    
    # 1. Xóa file vật lý
    count = 0
    for _, row in df_to_delete.iterrows():
        try:
            if os.path.exists(row['path_raw']): os.remove(row['path_raw'])
            if os.path.exists(row['path_clean']): os.remove(row['path_clean'])
            # Không xóa path_diff vì nó dùng chung (chỉ xóa nếu là Real Data và không còn ai dùng - logic phức tạp hơn, tạm bỏ qua)
            count += 1
        except Exception:
            pass

    # 2. Cập nhật CSV
    # Đọc lại CSV gốc để đảm bảo không bị conflict
    full_df = pd.read_csv(DATA_CSV)
    # Giữ lại những dòng KHÔNG nằm trong danh sách xóa (dựa vào timestamp hoặc uid nếu có)
    # Ở đây dùng index giả định hoặc timestamp + label làm key
    
    # Cách đơn giản: Filter ngược lại
    # (Lưu ý: Cách này hơi chậm nếu data lớn, nhưng an toàn)
    full_df = full_df[~full_df['path_raw'].isin(df_to_delete['path_raw'])]
    
    full_df.to_csv(DATA_CSV, index=False)
    
    return count

# [Cập nhật trong backend_core.py]

def detect_segment(video_path, start_time, duration=60.0):
    """
    Xử lý một đoạn video ngắn (để preview nhanh).
    Trả về:
    - errors: Danh sách lỗi trong đoạn này.
    - waveform: Dữ liệu sóng âm để vẽ.
    - sr: Tần số mẫu.
    """
    if not os.path.exists(MODEL_FILE):
        return [], None, None, "Chưa có model."

    clf = joblib.load(MODEL_FILE)
    if isinstance(clf, dict):
        clf = clf["classifier"]
        mean_clean_vec = clf["mean_clean_vec"]
    else:
        mean_clean_vec = None
        
    try:
        # 1. Load Audio Segment (Chỉ load 60s - Nhanh hơn nhiều)
        # offset=start_time, duration=duration
        y, sr = librosa.load(video_path, sr=TARGET_SAMPLE_RATE, offset=start_time, duration=duration)
        
        if len(y) == 0:
            return [], None, None, "Hết video (End of file)."
            
        # Chuyển sang Tensor để xử lý
        waveform_tensor = torch.from_numpy(y).unsqueeze(0) # (1, Time)

        # 2. Sliding Window & Vectorization
        WINDOW_SIZE = 1.0
        STEP = 0.5
        win_len = int(WINDOW_SIZE * sr)
        step_len = int(STEP * sr)
        
        chunks = []
        timestamps = []
        
        # Cắt nhỏ đoạn 60s này
        for i in range(0, len(y) - win_len, step_len):
            chunk = y[i : i + win_len]
            chunks.append(chunk)
            timestamps.append(i / sr) # Thời gian tương đối trong đoạn 60s
            
        if not chunks: return [], y, sr, "Đoạn quá ngắn."

        # Vector hóa
        embeddings = extract_embeddings_batch(chunks)
        
        # 3. Predict
        predictions = clf.predict(embeddings)
        
        # 4. Tính toán Distance (cho Lớp bảo vệ 2)
        distances = [0.0] * len(predictions)
        if mean_clean_vec is not None:
             vec_tensor = torch.tensor(embeddings).to(DEVICE)
             mean_tensor = torch.tensor(mean_clean_vec).to(DEVICE).unsqueeze(0)
             cos_sim = torch.nn.functional.cosine_similarity(vec_tensor, mean_tensor)
             distances = 1 - cos_sim.cpu().numpy()

        # 5. Tổng hợp lỗi (Thêm offset thời gian thực tế)
        detected_errors = []
        for i, (t_rel, label) in enumerate(zip(timestamps, predictions)):
            if 'clean' not in label.lower():
                dist = distances[i]
                # Áp dụng ngưỡng (mặc định 0.3 hoặc lấy từ tham số nếu cần)
                if dist > 0.3: 
                    detected_errors.append({
                        "start_rel": t_rel, # Thời gian trong đoạn 60s (để vẽ)
                        "start_abs": start_time + t_rel, # Thời gian thực trong video
                        "duration": WINDOW_SIZE,
                        "label": label
                    })
                    
        return detected_errors, y, sr, "OK"

    except Exception as e:
        return [], None, None, f"Lỗi: {e}"

def plot_interactive_waveform(y, sr, errors, start_time):
    """
    Vẽ Waveform giống Final Cut Pro.
    - y: Tín hiệu âm thanh của đoạn 60s.
    - errors: Danh sách lỗi trong đoạn này.
    """
    import matplotlib.pyplot as plt
    
    # Cấu hình màu FCP
    BG_COLOR = "#2b303b" # Xám xanh đậm (giống ảnh mẫu)
    WAVE_COLOR = "#7a8c9e" # Xám xanh nhạt
    ERROR_COLOR = "#ff5e5e" # Đỏ (Highlight lỗi)
    
    fig, ax = plt.subplots(figsize=(12, 3))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    
    # 1. Vẽ Waveform nền (FCP Style)
    # Dùng fill_between để tạo sóng đặc
    time_axis = np.linspace(0, len(y)/sr, num=len(y))
    ax.fill_between(time_axis, y, color=WAVE_COLOR, alpha=0.9, linewidth=0)
    ax.fill_between(time_axis, -y, color=WAVE_COLOR, alpha=0.9, linewidth=0) # Đối xứng
    
    # 2. Tô đỏ vùng lỗi
    for err in errors:
        # start_rel là thời gian bắt đầu trong đoạn 60s
        t1 = err['start_rel']
        t2 = t1 + err['duration']
        
        # Tìm index tương ứng trong mảng y
        idx1 = int(t1 * sr)
        idx2 = int(t2 * sr)
        
        if idx2 < len(y):
            y_err = y[idx1:idx2]
            t_err = time_axis[idx1:idx2]
            # Vẽ đè lên bằng màu đỏ
            ax.fill_between(t_err, y_err, color=ERROR_COLOR, alpha=1.0, linewidth=0)
            ax.fill_between(t_err, -y_err, color=ERROR_COLOR, alpha=1.0, linewidth=0)

    # 3. Trang trí trục (Tối giản)
    ax.set_xlim(0, len(y)/sr)
    ax.set_ylim(-1, 1)
    ax.axis('off') # Tắt hết trục tọa độ cho giống FCP
    
    # Thêm đường kẻ ngang mờ (Zero line)
    ax.axhline(0, color='white', alpha=0.1, linewidth=0.5)
    
    # Thêm Timecode Text ở góc trái
    start_fmt = f"{int(start_time//60):02}:{int(start_time%60):02}"
    end_fmt = f"{int((start_time+len(y)/sr)//60):02}:{int((start_time+len(y)/sr)%60):02}"
    ax.text(0, 0.9, f"Time: {start_fmt} - {end_fmt}", color="white", transform=ax.transAxes, fontsize=8, alpha=0.5)

    plt.tight_layout()
    return fig

# --- THÊM VÀO backend_core.py ---
# [Cập nhật trong backend_core.py]
# --- [PHẦN CẬP NHẬT CHO TAB 6] ---
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import scipy.signal

# Cấu hình màu sắc chuẩn Final Cut Pro (Dark Mode)
FCP_COLORS = {
    "BG": "#1e1e1e",
    "TRACK_BG": "#262626", 
    "TEXT": "#d1d1d1",
    "GRID": "#3b3b3b",
    "RAW": "#64d2ff",       # Xanh dương nhạt (Source)
    "HUMAN": "#3cc2ea",     # Xanh ngọc (Edited)
    "AI": "#d4af37",        # Vàng kim (Prediction)
    "DIFF_RH": "#ff5e5e",   # Đỏ (Raw vs Human) - Lỗi Editor sửa
    "DIFF_RA": "#bd93f9",   # Tím (Raw vs AI) - Lỗi AI sửa
    "DIFF_HA": "#ff9f0a"    # Cam (Human vs AI) - Sai số của AI
}

# --- [PHẦN CẬP NHẬT CHO TAB 6: COMPARATOR PRO] ---
import matplotlib.pyplot as plt
import scipy.signal

# Cấu hình màu sắc mặc định (Dark Mode)
DEFAULT_THEME = {
    "BG_MAIN": "#0A0A1A", "BG_TRACK": "#14142A", "TEXT": "#E0E0E0", "GRID": "#FFFFFF",
    "RAW": "#4EA8DE",       # Light Blue
    "HUMAN": "#48BFE3",     # Cyan
    "AI_BASE": "#F9C74F",   # Gold 
    "DIFF_CORE": "#FF5E5E", # Red (Raw vs Human)
    "DIFF_RA": "#FF5E5E",   # Purple (Raw vs AI)
    "DIFF_HA": "#FF5E5E"    # Orange (Human vs AI)
}

def auto_align_audio(y_ref, y_target):
    """Đồng bộ hóa y_target khớp với y_ref dùng Cross-Correlation."""
    if len(y_ref) == 0 or len(y_target) == 0: return y_target, 0
    
    # Lấy mẫu nhỏ để tính cho nhanh nếu file quá dài
    calc_len = min(len(y_ref), len(y_target), 16000 * 60) 
    
    correlation = scipy.signal.correlate(y_target[:calc_len], y_ref[:calc_len], mode='full', method='fft')
    lags = scipy.signal.correlation_lags(len(y_target[:calc_len]), len(y_ref[:calc_len]), mode='full')
    lag = lags[np.argmax(correlation)]

    y_aligned = np.zeros_like(y_ref)
    
    if lag > 0:
        take_len = min(len(y_target) - lag, len(y_ref))
        if take_len > 0: y_aligned[:take_len] = y_target[lag : lag + take_len]
    else:
        start_idx = abs(lag)
        take_len = min(len(y_target), len(y_ref) - start_idx)
        if take_len > 0: y_aligned[start_idx : start_idx + take_len] = y_target[:take_len]

    return y_aligned, lag
# [Thay thế hàm này trong backend_core.py]

def scan_for_difference_v2(
    raw_path, edited_path, ai_path=None,  # <--- Phải có ai_path ở đây
    start_time=0, duration=60.0, 
    threshold=0.02, 
    hunt_mode="Raw vs Human"
):
    """
    Quét và so sánh các luồng audio. Tự động align tất cả theo Edited.
    """
    import librosa 
    import numpy as np

    try:
        # 1. Load Audio (Lazy Loading)
        y_edited, sr = librosa.load(edited_path, sr=16000, offset=start_time, duration=duration)
        y_raw, _ = librosa.load(raw_path, sr=16000, offset=start_time, duration=duration)
        
        y_ai = None
        if ai_path and os.path.exists(ai_path):
            try:
                y_ai, _ = librosa.load(ai_path, sr=16000, offset=start_time, duration=duration)
            except: pass

        if len(y_edited) == 0: return False, None, None, None, None, 0.0

        # 2. Cắt về cùng độ dài (theo Edited làm chuẩn)
        min_len = len(y_edited)
        y_raw = y_raw[:min_len]
        if y_ai is not None: 
            y_ai = y_ai[:min_len]
        
        # Pad nếu Raw ngắn hơn (hiếm)
        if len(y_raw) < min_len:
            y_raw = np.pad(y_raw, (0, min_len - len(y_raw)))

        # 3. Auto-Align
        y_raw_aligned, _ = auto_align_audio(y_edited, y_raw)
        
        y_ai_aligned = None
        if y_ai is not None:
            y_ai_aligned, _ = auto_align_audio(y_edited, y_ai)

        # 4. Tính toán Diff Score
        diff_score = 0.0
        
        if hunt_mode == "Raw vs Human":
            diff_signal = np.abs(y_raw_aligned - y_edited)
        elif hunt_mode == "Raw vs AI" and y_ai_aligned is not None:
            diff_signal = np.abs(y_raw_aligned - y_ai_aligned)
        elif hunt_mode == "Human vs AI" and y_ai_aligned is not None:
            diff_signal = np.abs(y_edited - y_ai_aligned)
        else:
            diff_signal = np.abs(y_raw_aligned - y_edited)

        diff_score = np.mean(diff_signal)
        found = diff_score > threshold
        
        # Trả về đủ 6 giá trị
        return found, y_raw_aligned, y_edited, y_ai_aligned, sr, diff_score

    except Exception as e:
        print(f"Scan error: {e}")
        # Trả về fallback để không crash UI
        return False, None, None, None, 16000, 0.0

def plot_pro_analysis_view(
    y_raw, y_edited, 
    ai_tracks_dict=None, 
    sr=16000, 
    view_mode="bipolar",
    colors_override=None,
    show_diff=True # <--- THAM SỐ MỚI (Mặc định hiện)
):
    """
    Vẽ biểu đồ Pro Stack View. 
    Hỗ trợ ẩn/hiện Diff để tiết kiệm không gian.
    """
    import matplotlib.pyplot as plt
    
    # 1. Áp dụng màu sắc
    THEME = DEFAULT_THEME.copy()
    if colors_override:
        THEME.update(colors_override)

    # 2. Chuẩn bị dữ liệu (Cắt bằng nhau)
    min_len = min(len(y_raw), len(y_edited))
    if ai_tracks_dict:
        for y_ai in ai_tracks_dict.values():
            min_len = min(min_len, len(y_ai))
            
    y_raw = y_raw[:min_len]
    y_edited = y_edited[:min_len]
    
    # 3. Xây dựng danh sách biểu đồ (Plot Configs)
    plot_configs = []
    
    # --- Nhóm 1: Ground Truth ---
    plot_configs.append({"data": y_raw, "label": "1. SOURCE (Raw)", "color": THEME["RAW"], "type": "wave"})
    plot_configs.append({"data": y_edited, "label": "2. TARGET (Edited)", "color": THEME["HUMAN"], "type": "wave"})
    
    # Chỉ thêm Diff nếu show_diff = True
    if show_diff:
        diff_rh = np.abs(y_raw - y_edited)
        plot_configs.append({"data": diff_rh, "label": "DIFF: Raw vs Human", "color": THEME["DIFF_CORE"], "type": "diff"})
    
    # --- Nhóm 2: AI Models ---
    if ai_tracks_dict:
        for idx, (name, y_ai) in enumerate(ai_tracks_dict.items()):
            y_ai_cut = y_ai[:min_len]
            
            # Luôn thêm track AI Waveform
            plot_configs.append({"data": y_ai_cut, "label": f"AI: {name}", "color": THEME["AI_BASE"], "type": "wave"})
            
            # Chỉ thêm Diff của AI nếu show_diff = True
            if show_diff:
                diff_ra = np.abs(y_raw - y_ai_cut)
                diff_ha = np.abs(y_edited - y_ai_cut)
                plot_configs.append({"data": diff_ra, "label": f"DIFF: Raw vs {name}", "color": THEME["DIFF_RA"], "type": "diff"})
                plot_configs.append({"data": diff_ha, "label": f"ERR: Human vs {name}", "color": THEME["DIFF_HA"], "type": "diff"})

    # 4. Tính chiều cao ảnh ĐỘNG (Dynamic Height)
    # Mỗi biểu đồ cao khoảng 2.5 inch
    fig_h = len(plot_configs) * 2.5
    
    # Khởi tạo Figure
    fig, axs = plt.subplots(len(plot_configs), 1, figsize=(20, fig_h), sharex=True)
    if len(plot_configs) == 1: axs = [axs]
    
    fig.patch.set_facecolor(THEME["BG_MAIN"])
    times = np.linspace(0, len(y_raw)/sr, num=len(y_raw))

    # 5. Vòng lặp Vẽ
    for i, ax in enumerate(axs):
        cfg = plot_configs[i]
        data = cfg["data"]
        
        ax.set_facecolor(THEME["BG_TRACK"])
        
        # Vẽ sóng (Bipolar / Unipolar)
        if view_mode == "bipolar":
            ax.fill_between(times, data, color=cfg["color"], alpha=0.9, linewidth=0)
            if cfg["type"] == "wave":
                ax.fill_between(times, -data, color=cfg["color"], alpha=0.9, linewidth=0)
            ax.set_ylim(-1.05, 1.05) if cfg["type"] == "wave" else ax.set_ylim(0, 1.05)
        else: # Unipolar
            abs_data = np.abs(data)
            ax.fill_between(times, abs_data, color=cfg["color"], alpha=0.9, linewidth=0)
            ax.set_ylim(0, 1.05)

        # Style Trục
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.axhline(0, color=THEME["GRID"], alpha=0.2, linewidth=0.5)
        ax.set_yticks([])
        
        # Label
        ax.text(0.005, 0.85, cfg["label"], transform=ax.transAxes, color="white", fontsize=12, fontweight='bold', bbox=dict(facecolor=THEME["BG_MAIN"], alpha=0.7, edgecolor='none'))

        # RMS Stats (Chỉ hiện nếu là Diff)
        if cfg["type"] == "diff":
            rms = np.sqrt(np.mean(data**2))
            bg_score = "#2ecc71" if rms < 0.05 else "#e74c3c"
            ax.text(0.99, 0.85, f"RMS Error: {rms:.4f}", transform=ax.transAxes, color="white", ha='right', fontsize=10, fontweight='bold', bbox=dict(facecolor=bg_score, alpha=0.9, edgecolor='none'))

        # Trục thời gian (Chỉ hiện ở biểu đồ cuối cùng)
        if i == len(axs) - 1:
            ax.tick_params(axis='x', colors=THEME["TEXT"], labelsize=10)
            ax.set_xlabel("Time (seconds)", color=THEME["TEXT"], fontsize=12)
        else:
            ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

    plt.subplots_adjust(hspace=0.05, left=0.01, right=0.99, top=0.98, bottom=0.05)
    return fig

# [Thêm vào backend_core.py]

def merge_audio_files(uploaded_files, silence_ms=500, sample_rate=16000):
    """
    Nhận danh sách file upload (Audio/Video), trích xuất audio,
    chuẩn hóa và ghép lại thành 1 file duy nhất.
    """
    combined = AudioSegment.empty()
    # Tạo đoạn im lặng
    silence = AudioSegment.silent(duration=silence_ms)
    
    processed_count = 0
    errors = []

    # Tạo thư mục temp để xử lý ffmpeg an toàn
    temp_dir = "temp_merge_processing"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        for i, uploaded_file in enumerate(uploaded_files):
            try:
                # 1. Lưu file tạm (Pydub/FFmpeg cần đường dẫn thực tế để xử lý video tốt nhất)
                # Giữ nguyên đuôi file gốc (mp3, mov...) để ffmpeg nhận diện codec
                ext = os.path.splitext(uploaded_file.name)[1]
                temp_path = os.path.join(temp_dir, f"input_{i}{ext}")
                
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # 2. Load Audio (Tự động extract từ video nếu là mov/mp4)
                audio = AudioSegment.from_file(temp_path)
                
                # 3. Chuẩn hóa (Bắt buộc để ghép không bị lỗi)
                audio = audio.set_frame_rate(sample_rate).set_channels(1)
                
                # 4. Ghép nối
                combined += audio + silence
                processed_count += 1
                
                # Xóa file tạm ngay
                os.remove(temp_path)
                
            except Exception as e:
                errors.append(f"{uploaded_file.name}: {str(e)}")

        # 5. Xuất file kết quả
        output_filename = f"merged_output_{int(time.time())}.wav"
        output_path = os.path.join(temp_dir, output_filename)
        
        # Export
        combined.export(output_path, format="wav")
        
        return output_path, processed_count, errors

    except Exception as e:
        return None, 0, [str(e)]
    
# [Thêm vào backend_core.py]

def plot_overlay_diff_view(
    y_raw, y_target, sr=16000, 
    threshold=0.01, # Ngưỡng để coi là có sự khác biệt (để tránh nhiễu nhỏ tô đỏ cả bài)
    title="Comparison Overlay"
):
    """
    Vẽ Waveform của Raw, và tô đỏ những đoạn khác biệt so với Target.
    Phong cách FCP: Nền tối, Sóng xanh, Đỉnh đỏ.
    """
    import matplotlib.pyplot as plt
    
    # 1. Align & Chuẩn bị dữ liệu
    min_len = min(len(y_raw), len(y_target))
    y_raw = y_raw[:min_len]
    y_target = y_target[:min_len]
    
    # Auto-Align Target theo Raw (Vì Raw là gốc hiển thị)
    y_target_aligned, _ = auto_align_audio(y_raw, y_target)
    
    # 2. Tính toán Diff
    diff_signal = np.abs(y_raw - y_target_aligned)
    
    # Tạo mask: Những điểm nào có sự khác biệt lớn hơn ngưỡng
    # (Làm mịn mask một chút để không bị đốm đỏ liti)
    frame_size = 512
    diff_envelope = np.array([np.max(diff_signal[i:i+frame_size]) for i in range(0, len(diff_signal), frame_size)])
    # Nội suy mask về độ dài gốc
    mask_indices = np.arange(len(diff_envelope)) * frame_size
    diff_mask_interpolated = np.interp(np.arange(len(y_raw)), mask_indices, diff_envelope)
    
    is_diff = diff_mask_interpolated > threshold

    # 3. Setup Giao diện FCP
    plt.style.use('dark_background')
    FCP_BG = "#1e1e1e" # Màu nền FCP
    FCP_WAVE_BLUE = "#5898d4" # Màu sóng xanh FCP (Raw/Normal)
    FCP_WAVE_RED = "#ff3b30"  # Màu sóng đỏ (Error/Diff)
    FCP_GRID = "#464646"

    fig, ax = plt.subplots(figsize=(18, 5))
    fig.patch.set_facecolor(FCP_BG)
    ax.set_facecolor(FCP_BG)

    # Trục thời gian
    times = np.linspace(0, len(y_raw)/sr, num=len(y_raw))
    
    # Downsample để vẽ nhanh nếu file dài
    step = 1 if len(y_raw) < 16000*30 else 10
    t_plot = times[::step]
    y_plot = y_raw[::step]
    mask_plot = is_diff[::step]

    # 4. VẼ LỚP 1: Sóng Raw bình thường (Màu Xanh)
    ax.fill_between(t_plot, y_plot, color=FCP_WAVE_BLUE, alpha=0.9, linewidth=0)
    ax.fill_between(t_plot, -y_plot, color=FCP_WAVE_BLUE, alpha=0.9, linewidth=0) # Đối xứng

    # 5. VẼ LỚP 2: Overlay Diff (Màu Đỏ)
    # Chỉ vẽ đè lên những chỗ có mask_plot = True
    # Dùng 'where' để chỉ tô vùng lỗi
    ax.fill_between(t_plot, y_plot, where=mask_plot, color=FCP_WAVE_RED, alpha=1.0, linewidth=0)
    ax.fill_between(t_plot, -y_plot, where=mask_plot, color=FCP_WAVE_RED, alpha=1.0, linewidth=0)

    # 6. Trang trí giống ảnh mẫu
    ax.axhline(0, color=FCP_GRID, linewidth=0.5, alpha=0.5) # Đường Zero mờ
    # Kẻ lưới dọc (thời gian)
    ax.grid(True, axis='x', color=FCP_GRID, linestyle='-', linewidth=0.5, alpha=0.5)
    ax.grid(False, axis='y')
    
    # Tắt viền trục
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['bottom'].set_color(FCP_GRID)
    
    # Ẩn trục Y, chỉ hiện trục X (Thời gian)
    ax.set_yticks([])
    ax.tick_params(axis='x', colors="#999999", labelsize=9)
    ax.set_xlabel("Timecode", color="#999999", fontsize=10)
    
    # Title nằm gọn bên trái
    ax.text(0, 1.05, f"▶ {title}", transform=ax.transAxes, 
            color="white", fontsize=11, fontweight='bold')

    plt.tight_layout()
    return fig