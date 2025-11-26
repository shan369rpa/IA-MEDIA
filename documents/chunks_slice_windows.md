Quyết định rất "máu lửa"! Nếu bạn muốn triển khai **Cửa sổ trượt (Sliding Window)** ngay bây giờ, chúng ta sẽ nâng cấp hệ thống lên mức độ phân tích chi tiết nhất ("Pixel-peeping" cho âm thanh).

Hãy nhớ rằng: Kỹ thuật này sẽ sinh ra **rất nhiều vector**. Ví dụ: 1 từ dài 0.5 giây sẽ sinh ra khoảng 5-10 vector con.

Dưới đây là kế hoạch triển khai chi tiết.

---

### **1. Nguyên lý Hoạt động (Cách dùng)**

Chúng ta sẽ không cắt file audio ra thành các file nhỏ hơn nữa (vì quá nhiều file rác). Thay vào đó, chúng ta sẽ **xử lý trong bộ nhớ (In-memory processing)**:

1.  **Input:** File audio của 1 từ (ví dụ: `hanhphuc.wav`, dài 0.6s).
2.  **Window:** Cửa sổ rộng `0.1s` (100ms).
3.  **Step (Stride):** Trượt mỗi `0.05s` (50ms).
4.  **Process:**
    *   Lấy 0.0 - 0.1s -> Vector 1
    *   Lấy 0.05 - 0.15s -> Vector 2
    *   ...
5.  **Output:** Một danh sách các vector `[v1, v2, v3, ...]`.

---

### **Bước 2: Cập nhật `src/ai/vectorizer.py`**

Chúng ta cần thêm hàm `create_sliding_window_embeddings` vào module này.

**Hành động:** Mở file `src/ai/vectorizer.py` và thêm đoạn code sau vào cuối (nhưng trước phần `if __name__ == ...`):

```python
# ... (Các import cũ giữ nguyên) ...
import math

def create_sliding_window_embeddings(
    audio_path: str, 
    model: EncoderClassifier, 
    window_len: float = 0.1, # Độ rộng cửa sổ (giây)
    step: float = 0.05 # Bước nhảy (giây)
) -> list | None:
    """
    Tạo một chuỗi các vector embedding bằng cách trượt cửa sổ trên file audio.
    
    Args:
        audio_path: Đường dẫn file audio.
        model: Model SpeechBrain.
        window_len: Độ dài cửa sổ tính bằng giây (mặc định 100ms).
        step: Bước trượt tính bằng giây (mặc định 50ms).
        
    Returns:
        list: Danh sách các vector (List[List[float]]). 
              Mỗi phần tử là một vector 192 chiều.
    """
    if not os.path.exists(audio_path):
        return None

    try:
        device = _get_device()
        
        # 1. Tải toàn bộ tín hiệu audio
        signal, fs = torchaudio.load(audio_path)
        
        # Đảm bảo signal ở dạng (1, time) - mono
        if signal.shape[0] > 1:
            signal = signal.mean(dim=0, keepdim=True)
            
        # Resample nếu cần (Model ECAPA cần 16000Hz)
        if fs != 16000:
            resampler = torchaudio.transforms.Resample(fs, 16000).to(device)
            signal = signal.to(device)
            signal = resampler(signal)
            fs = 16000
        else:
            signal = signal.to(device)

        # 2. Tính toán kích thước cửa sổ theo mẫu (samples)
        window_samples = int(window_len * fs)
        step_samples = int(step * fs)
        total_samples = signal.shape[1]

        # Nếu file ngắn hơn 1 cửa sổ, lấy luôn cả file
        if total_samples < window_samples:
            embeddings = model.encode_batch(signal)
            vector = embeddings.squeeze().cpu().numpy().tolist()
            return [vector]

        # 3. Cắt lát và Vector hóa (Batch Processing để nhanh hơn)
        slices = []
        
        # Dùng unfold để tạo cửa sổ trượt cực nhanh trên Tensor
        # signal có dạng [1, time]
        # unfold tạo ra dạng [1, num_windows, window_size]
        # dimension 1 là chiều thời gian
        try: 
            # unfold(dimension, size, step)
            windows = signal.unfold(1, window_samples, step_samples)
            # windows đang là [1, N, window_samples] -> chuyển thành [N, 1, window_samples] để vào model
            windows = windows.permute(1, 0, 2) 
            
            # Đưa vào model theo batch (xử lý cùng lúc)
            embeddings = model.encode_batch(windows)
            
            # embeddings ra dạng [N, 1, 192] -> chuyển thành list [N, 192]
            vectors = embeddings.squeeze(1).cpu().numpy().tolist()
            
            return vectors

        except Exception as e:
            logging.error(f"Lỗi khi unfold/encode sliding window: {e}")
            return None

    except Exception as e:
        logging.error(f"Lỗi xử lý audio sliding window: {e}")
        return None
```

---

### **Bước 3: Cập nhật CSDL (Tạo bảng `word_slices`)**

Chúng ta không thể nhét hàng chục vector con vào bảng `words` được. Cần một bảng con chuyên dụng.

**Hành động:** Tạo file `update_schema_slices.sql` và chạy nó trên server (upload và exec giống như các file sql trước).

```sql
-- update_schema_slices.sql

-- Tạo bảng lưu các lát cắt (slices) của từ
CREATE TABLE IF NOT EXISTS "word_slices" (
    "id" SERIAL PRIMARY KEY,
    "word_id" INTEGER NOT NULL REFERENCES "words"("id") ON DELETE CASCADE,
    
    -- Xác định slide này thuộc về bản clean hay error của từ đó
    "source_type" VARCHAR(10) CHECK ("source_type" IN ('clean', 'error')),
    
    "slice_index" INTEGER NOT NULL, -- Thứ tự của lát cắt (0, 1, 2...)
    "start_offset_ms" INTEGER,      -- Thời điểm bắt đầu tương đối trong file chunk (ms)
    
    "embedding" VECTOR(192),        -- Vector của lát cắt này
    
    "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tạo index để tìm kiếm nhanh trên các lát cắt
CREATE INDEX ON "word_slices" USING ivfflat ("embedding" vector_cosine_ops) WITH (lists = 100);
CREATE INDEX ON "word_slices" ("word_id");
```

---

### **Bước 4: Cập nhật `db_manager.py`**

Thêm hàm để chèn dữ liệu vào bảng mới.

```python
# src/database/db_manager.py

def insert_word_slices(conn, slices_data: list):
    """
    Chèn dữ liệu sliding window vào bảng word_slices.
    slices_data: list of tuples (word_id, source_type, slice_index, start_offset_ms, embedding)
    """
    if not slices_data:
        return False
    
    query = """
        INSERT INTO "word_slices" 
        (word_id, source_type, slice_index, start_offset_ms, embedding)
        VALUES %s
    """
    try:
        with conn.cursor() as cur:
            execute_values(cur, query, slices_data)
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Lỗi insert word_slices: {e}")
        conn.rollback()
        return False
```

---

### **Bước 5: Tích hợp vào `vectorize.py`**

Sửa file `vectorize.py` để gọi hàm trượt cửa sổ. Lưu ý: Việc này sẽ làm quá trình chạy **lâu hơn khoảng 5-10 lần**, nên chúng ta cần cân nhắc.

```python
# Trong vòng lặp xử lý từng từ trong vectorize.py

                # ... (Code cũ tạo embedding cho cả từ) ...
                # embedding_clean = vectorizer.create_embedding(...)
                
                # 1. Chèn Word vào bảng 'words' và LẤY LẠI ID vừa tạo
                # (Cần sửa db_manager.insert_words_data để hỗ trợ RETURNING id, 
                # hoặc chèn từng dòng để lấy ID. Để đơn giản cho demo, ta giả sử đã có ID)
                # *Lưu ý kỹ thuật: insert batch khó lấy ID tương ứng.
                # Cách tốt nhất: Chèn Word trước -> Query lấy ID -> Chèn Slices.
                
                # --- LOGIC SLIDING WINDOW (MỚI) ---
                
                # Tạo slices cho Clean Audio
                clean_slices_vecs = vectorizer.create_sliding_window_embeddings(clean_audio_path, embedding_model)
                
                # Tạo slices cho Error Audio
                error_slices_vecs = vectorizer.create_sliding_window_embeddings(error_audio_path, embedding_model)
                
                # Chuẩn bị dữ liệu để chèn (Cần Word ID thật từ DB)
                # Đây là đoạn khó nhất khi làm batch processing.
```

### **Lời khuyên Thực tế cho Giai đoạn Demo**

Việc chèn **Slices** vào CSDL đòi hỏi bạn phải biết `word_id` của từ cha. Nhưng vì chúng ta đang chèn `words` theo lô (`execute_values`) để nhanh, nên việc lấy lại ID của từng từ vừa chèn là khá phức tạp.

**Giải pháp cho Demo Phase 1:**
Tôi khuyên bạn **KHOAN** hãy chèn Slices vào Database vội. Thay vào đó:
1.  Hãy chắc chắn rằng hàm `create_sliding_window_embeddings` trong `vectorizer.py` hoạt động đúng (viết Unit Test cho nó).
2.  Trong `vectorize.py`, bạn có thể **tính toán thử** các slice này và in ra log (ví dụ: "Word 'hạnh phúc' generated 12 slices") để chứng minh tính năng.
3.  Để dành việc Insert vào DB cho **Phase 1.5**, khi chúng ta tối ưu hóa logic insert (chuyển sang insert từng item hoặc dùng cơ chế ID thông minh hơn).

**Bạn có đồng ý chỉ cài logic tính toán (bước 2) và tạo bảng (bước 3) trước, chưa dùng cho pipeline chính không?**