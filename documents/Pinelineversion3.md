
Đây sẽ là "kim chỉ nam" cho các bước phát triển tiếp theo của chúng ta.

---

### **IA MEDIA - Luồng Công việc Toàn diện (phiên bản 3.0)**

#### **Giai đoạn 1: Thu thập và Làm giàu Dữ liệu (Data Ingestion & Enrichment)**
*(Đây là phiên bản nâng cấp của `main.py` và `vectorize.py`)*

**Mục tiêu:** Xử lý một cặp video `raw`/`edited` và file `FCPXML` để tạo ra một cơ sở dữ liệu đa bảng, được làm giàu với nhiều lớp thông tin.

**Bước 1.1: Phân tích FCPXML (FCPXML Deep Analysis)**
*   **Module:** `fcpxml_parser.py`
*   **Hành động:**
    1.  Đọc file FCPXML.
    2.  **Trích xuất Time Map:** Xây dựng bản đồ alignment `raw` vs. `edited` (như cũ).
    3.  **Trích xuất "Edit Events":** Bóc tách và định vị tất cả các hành động chỉnh sửa âm thanh có thể tìm thấy (ví dụ: `noise_reduction`, `EQ`, `compressor`, `volume_mute_keyframe`, `gap`).
*   **Đầu ra:** Một đối tượng dữ liệu chứa `time_map` và `edit_events_list`.

**Bước 1.2: Phiên âm (Transcription)**
*   **Module:** `transcriber.py`
*   **Hành động:** Chạy `WhisperX` trên file audio `edited` để lấy transcript và word timestamps cực kỳ chính xác.
*   **Đầu ra:** Danh sách các `word_timestamps`.

**Bước 1.3: Chunking & Feature Extraction (Bước Cốt lõi)**
*   **Module:** `chunker.py` (sẽ được nâng cấp mạnh mẽ)
*   **Hành động:**
    1.  Lặp qua danh sách `word_timestamps` từ WhisperX.
    2.  Với mỗi từ, cắt ra một cặp audio chunk `(word_clean.wav, word_error.wav)` sử dụng `time_map`.
    3.  **Làm giàu Dữ liệu (Enrichment):** Với mỗi cặp chunk vừa tạo:
        a.  **FCPXML Context:** Kiểm tra xem timestamp của từ này có nằm trong vùng ảnh hưởng của bất kỳ "Edit Event" nào không (từ Bước 1.1).
        b.  **Signal Analysis:** Gọi module `signal_analyzer.py` để tính toán một bộ đầy đủ các **đặc trưng âm học** (Acoustic Features) từ cả 3 miền (Time, Frequency, Time-Frequency) cho cả `word_clean.wav` và `word_error.wav`.
        c.  **Language ID:** (Tùy chọn nâng cao) Chạy mô hình nhận diện ngôn ngữ trên chunk.
    4.  **Tổ chức Dữ liệu:** Tổng hợp tất cả thông tin vào một file `metadata.csv` duy nhất, với mỗi hàng đại diện cho một cặp từ, chứa đầy đủ các cột (`word_text`, `start_ms`, `clean_path`, `error_path`, `fcpxml_events`, `clean_features`, `error_features`...).

**Bước 1.4: Nhập liệu vào CSDL (Database Ingestion)**
*   **Module:** `vectorize.py` (hoặc `ingest.py`)
*   **Hành động:**
    1.  Đọc file `metadata.csv`.
    2.  **Tạo Embedding:** Với mỗi cặp audio chunk, tạo `embedding_clean` và `embedding_error`.
    3.  **Chèn Dữ liệu:**
        *   Kết nối CSDL.
        *   Chèn thông tin video vào bảng `sources`.
        *   Chèn thông tin về các "Edit Events" từ FCPXML vào bảng `edit_events`.
        *   Chèn thông tin chi tiết của từng từ (bao gồm `word_text`, timestamps, 2 embeddings, 2 bộ features, và các khóa ngoại liên kết đến `sources` và `edit_events`) vào bảng `words`.

**Kết quả của Giai đoạn 1:** Một CSDL được điền đầy đủ dữ liệu, cực kỳ phong phú và sẵn sàng cho việc huấn luyện.

---

#### **Giai đoạn 2: Xây dựng Mô hình Phân loại Lỗi (Error Classifier Training)**

**Mục tiêu:** Xây dựng và huấn luyện "bộ não" AI.

**Bước 2.1: Kỹ thuật Đặc trưng (Feature Engineering)**
*   **Module:** `train_classifier.py`
*   **Hành động:**
    1.  Truy vấn CSDL để lấy dữ liệu từ bảng `words`.
    2.  Tạo **Input Vector (X)** bằng cách kết hợp nhiều nguồn bằng chứng:
        *   `diff_vector = embedding_error - embedding_clean` (192 chiều).
        *   `feature_vector_clean` (ví dụ: 20 chiều từ `features_clean`).
        *   `feature_vector_error` (ví dụ: 20 chiều từ `features_error`).
        *   **X = concatenate([diff_vector, feature_vector_clean, feature_vector_error])** (tổng cộng 192 + 20 + 20 = 232 chiều).
    3.  Tạo **Output (y):** Đây là `error_label` được xác định bởi "Quy trình Loại trừ Logic" (sẽ được hiện thực hóa trong module `PronunciationErrorDetector`).

**Bước 2.2: Huấn luyện và Đánh giá**
*   **Module:** `train_classifier.py`
*   **Hành động:**
    1.  Chia dữ liệu (X, y) thành tập train/test.
    2.  Thử nghiệm các mô hình khác nhau (`KNN`, `SVM`, `RandomForest`...).
    3.  Sử dụng các kỹ thuật xử lý dữ liệu mất cân bằng (SMOTE) nếu cần.
    4.  Đánh giá và chọn ra mô hình tốt nhất.
*   **Đầu ra:** File `error_classifier.pkl`.
->Để khai thác triệt để, áp dụng học máy hoàn chỉnh:
> **Data Loading $\rightarrow$ Feature Engineering $\rightarrow$ Handling Imbalance (SMOTE) $\rightarrow$ Hyperparameter Tuning (GridSearchCV) $\rightarrow$ Model Training (Thử nhiều model) $\rightarrow$ Evaluation $\rightarrow$ Save Best Model.**

---

#### **Giai đoạn 3: Suy luận và Tạo Báo cáo (Inference & Reporting)**

**Mục tiêu:** Áp dụng mô hình đã huấn luyện để phân tích video mới.

**Bước 3.1: Pipeline Suy luận**
*   **Module:** `analyze_new_video.py`
*   **Hành động:**
    1.  Nhận một video `raw` mới.
    2.  Thực hiện các bước tương tự Phase 1 để cắt chunk và trích xuất embedding + features cho từng từ.
    3.  Với mỗi từ, tạo `diff_vector` giả định và xây dựng **Input Vector (X_new)** như ở Bước 2.1.
    4.  Đưa `X_new` vào model `error_classifier.pkl` để nhận về dự đoán `predicted_label`.
    5.  Lọc ra danh sách các từ bị lỗi tiềm năng.

**Bước 3.2: Tạo Báo cáo FCPXML**
*   **Module:** `fcpxml_generator.py`
*   **Hành động:** Nhận danh sách lỗi từ bước trước và tạo ra file `.fcpxml` To-Do List với các marker được tô màu và ghi chú chi tiết.

Luồng công việc này là sự kết tinh của tất cả các thảo luận của chúng ta, đảm bảo tính toàn diện, chính xác và mạnh mẽ cho toàn bộ hệ thống.