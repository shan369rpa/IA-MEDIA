# IA MEDIA - Data Strategy & Architecture (Version 2.0 - Final)
## Chiến lược và Kiến trúc Dữ liệu Dự án IA MEDIA (Phiên bản 2.0 - Hoàn chỉnh)

This document outlines an advanced, multi-layered strategy for creating a comprehensive and analysis-ready dataset. The architecture is designed to be robust, scalable, and capable of addressing the wide range of audio-visual challenges present in the source recordings.

Tài liệu này vạch ra một chiến lược nâng cao, đa lớp để tạo ra một bộ dữ liệu toàn diện và sẵn sàng cho việc phân tích. Kiến trúc được thiết kế để vững chắc, có khảრობ mở rộng và có khả năng giải quyết một phổ rộng các thách thức về âm thanh-hình ảnh có trong các bản ghi gốc.

---

## 1. Core Principle: Parallel Enrichment / Nguyên tắc Cốt lõi: Làm giàu Song song

Instead of a single, monolithic pipeline, we adopt a parallel processing approach. Core, computationally expensive steps are run only once, and their outputs are used as inputs for multiple, independent chunking and enrichment branches. This ensures efficiency and modularity.

Thay vì một pipeline đơn lẻ, nguyên khối, chúng ta áp dụng phương pháp xử lý song song. Các bước cốt lõi, tốn nhiều tài nguyên tính toán sẽ chỉ được chạy MỘT LẦN. Kết quả của chúng được sử dụng làm đầu vào cho nhiều nhánh chunking và làm giàu dữ liệu độc lập. Điều này đảm bảo hiệu quả và tính mô-đun hóa.

### Pipeline Overview / Tổng quan Pipeline
```
+------------------------------------------+
| Input: Video (Raw, Edited), FCPXML       |
+------------------------------------------+
                   |
                   V
+------------------------------------------+
| Shared Step 1: Extract Audio (.wav)      |
+------------------------------------------+
                   |
                   V
+------------------------------------------+
| Shared Step 2: Transcribe with Whisper   |
| (generates word & sentence timestamps)   |
+------------------------------------------+
                   |
                   |
+------------------+------------------+
|                  |                  |
V                  V                  V
+----------------+ +----------------+ +----------------+
| Branch A:      | | Branch B:      | | Branch C (Future):|
| MICRO CHUNKING | | SEMANTIC CHUNK.| | SLIDING WINDOW |
+----------------+ +----------------+ +----------------+
```

## 2. Advanced Chunking & Enrichment Techniques / Các Kỹ thuật Chunking & Làm giàu Nâng cao

We will implement a suite of contemporary techniques to capture a rich spectrum of audio-visual and linguistic characteristics.
Chúng ta sẽ triển khai một bộ các kỹ thuật đương đại để nắm bắt một phổ phong phú các đặc điểm về âm thanh-hình ảnh và ngôn ngữ.

### 2.1. Hierarchical Chunking / Chunking Phân cấp

-   **Description:** Instead of a single chunk size, we will segment the data at multiple levels of granularity: sentences, words, and specific sound events.
-   **Problem Solved:** Allows us to analyze the data from different perspectives. Word chunks are for pronunciation details, sentence chunks are for prosody and flow, and event chunks isolate specific noises. This layered approach enables highly specific error detection and targeted analysis.
-   **Mô tả:** Thay vì một kích thước chunk duy nhất, chúng ta sẽ phân đoạn dữ liệu ở nhiều cấp độ chi tiết: câu, từ, và các sự kiện âm thanh cụ thể.
-   **Vấn đề được Giải quyết:** Cho phép chúng ta phân tích dữ liệu từ các góc độ khác nhau. Chunk từ dùng cho chi tiết phát âm, chunk câu dùng cho ngữ điệu và sự trôi chảy, chunk sự kiện dùng để cô lập các tiếng ồn cụ thể. Cách tiếp cận phân lớp này cho phép phát hiện lỗi và phân tích mục tiêu một cách cực kỳ chính xác.

### 2.2. Audio Event Detection (AED) / Phát hiện Sự kiện Âm thanh

-   **Description:** We will use a pre-trained model (e.g., YAMNet, PANNs) to scan the entire audio track and identify non-speech events.
-   **Problem Solved:** Automatically detects and isolates specific background noises like `[cough]`, `[laughter]`, `[writing_sound]`, and `[side_speech]`. This builds a rich database of noise samples and, more importantly, allows us to flag or exclude speech chunks that are contaminated by these noises, ensuring higher quality data for model training.
-   **Mô tả:** Chúng ta sẽ sử dụng một mô hình được huấn luyện sẵn (ví dụ: YAMNet, PANNs) để quét toàn bộ track âm thanh và xác định các sự kiện không phải lời nói.
-   **Vấn đề được Giải quyết:** Tự động phát hiện và cô lập các tiếng ồn nền cụ thể như `[tiếng ho]`, `[tiếng cười]`, `[tiếng viết bảng]`, và `[tiếng nói chuyện bên cạnh]`. Điều này xây dựng một cơ sở dữ liệu phong phú về các mẫu nhiễu, và quan trọng hơn, cho phép chúng ta đánh dấu hoặc loại bỏ các chunk lời nói bị nhiễm bẩn bởi những tiếng ồn này, đảm bảo dữ liệu chất lượng cao hơn cho việc huấn luyện mô hình.

### 2.3. Word-Level Language Identification / Nhận diện Ngôn ngữ Cấp độ Từ

-   **Description:** Each word chunk will be processed by a language identification model to tag it with its detected language.
-   **Problem Solved:** Solves the critical problem of false positives in pronunciation error detection. It allows the system to differentiate between a Vietnamese word with a final sound error (e.g., a "Westernized" ending) and a correctly pronounced foreign word (English, French, Pali) that naturally has a final consonant sound.
-   **Mô tả:** Mỗi chunk từ sẽ được xử lý bởi một mô hình nhận diện ngôn ngữ để gắn thẻ ngôn ngữ được phát hiện.
-   **Vấn đề được Giải quyết:** Giải quyết vấn đề cốt lõi về báo động giả trong việc phát hiện lỗi phát âm. Nó cho phép hệ thống phân biệt giữa một từ tiếng Việt bị lỗi âm đuôi (ví dụ: âm cuối bị "Tây hóa") và một từ ngoại ngữ (Anh, Pháp, Pali) được phát âm đúng mà vốn dĩ có âm phụ âm cuối.

### 2.4. Interpretable Acoustic Feature Extraction / Trích xuất Đặc trưng Âm học Có thể Diễn giải

-   **Description:** For every chunk, alongside the "black-box" deep learning embedding, we will compute and store a vector of traditional, interpretable acoustic features (RMS, MFCCs, Pitch, etc.).
-   **Problem Solved:** Provides "glass-box" insights into *why* an error is flagged. For example, a high RMS value directly points to a volume spike. These features can be used by simpler, faster machine learning models for initial error filtering and are invaluable for data analysis and visualization to understand the audio's characteristics.
-   **Mô tả:** Với mỗi chunk, bên cạnh vector embedding "hộp đen" từ học sâu, chúng ta sẽ tính toán và lưu trữ một vector các đặc trưng âm học truyền thống, có thể diễn giải được (RMS, MFCCs, Pitch...).
-   **Vấn đề được Giải quyết:** Cung cấp cái nhìn "hộp kính" về việc *tại sao* một lỗi bị đánh dấu. Ví dụ, một giá trị RMS cao chỉ thẳng đến một điểm âm lượng tăng vọt. Các đặc trưng này có thể được sử dụng bởi các mô hình học máy đơn giản, nhanh hơn để lọc lỗi ban đầu và là vô giá cho việc phân tích, trực quan hóa dữ liệu để hiểu các đặc điểm của âm thanh.

### 2.5. Comparative Spectrogram Analysis / Phân tích So sánh Phổ tần

-   **Description:** For each `clean`/`error` pair, we will generate spectrogram images and compute a "difference image" that highlights the spectral changes made during editing.
-   **Problem Solved:** This technique visualizes the exact nature of an audio error. The "difference image" can be a powerful input for Convolutional Neural Networks (CNNs) to learn to classify error types based on their visual patterns (e.g., a clipping error has a distinct visual signature). It transforms an audio problem into an image analysis problem.
-   **Mô tả:** Với mỗi cặp `clean`/`error`, chúng ta sẽ tạo ra hình ảnh biểu đồ phổ tần và tính toán một "hình ảnh khác biệt" làm nổi bật những thay đổi về phổ được thực hiện trong quá trình chỉnh sửa.
-   **Vấn đề được Giải quyết:** Kỹ thuật này trực quan hóa bản chất chính xác của một lỗi âm thanh. "Hình ảnh khác biệt" có thể là một đầu vào mạnh mẽ cho Mạng Nơ-ron Tích chập (CNN) để học cách phân loại các loại lỗi dựa trên "hoa văn" hình ảnh của chúng (ví dụ: lỗi clipping có một dấu hiệu hình ảnh đặc trưng). Nó biến một bài toán âm thanh thành một bài toán phân tích hình ảnh.

---

## 3. Database Architecture: Relational Multi-Table Schema / Kiến trúc CSDL: Lược đồ Đa bảng Quan hệ

To support this rich, multi-faceted data model, we will adopt a normalized, multi-table schema. This design ensures data integrity, minimizes redundancy, and provides maximum flexibility for complex queries.

Để hỗ trợ mô hình dữ liệu đa diện, phong phú này, chúng ta sẽ áp dụng một lược đồ đa bảng, được chuẩn hóa. Thiết kế này đảm bảo tính toàn vẹn của dữ liệu, giảm thiểu sự dư thừa và cung cấp sự linh hoạt tối đa cho các truy vấn phức tạp.

### Schema Visualization / Trực quan hóa Lược đồ
```
+-----------+       +----------------+       +-----------+
|  sources  | (1) --< (N) |   sentences    | (1) --< (N) |   words   |
+-----------+       +----------------+       +-----------+
      | (1)
      |
      `----< (N) +-------------+
                 |  anomalies  |
                 +-------------+
```

### Table Definitions / Định nghĩa các Bảng

#### 1. `sources` Table
*   **Purpose:** Stores metadata about the original video files. This is the root table.
*   **Mục đích:** Lưu trữ metadata về các file video gốc. Đây là bảng gốc.

| Tên Cột | Kiểu Dữ liệu (PostgreSQL) | Mô tả |
| :--- | :--- | :--- |
| `id` | `SERIAL PRIMARY KEY` | ID tự tăng, khóa chính. |
| `video_name` | `TEXT UNIQUE NOT NULL` | Tên định danh duy nhất cho video (ví dụ: 'phap_thoai_001'). |
| `duration_sec`| `FLOAT` | Tổng thời lượng của video gốc (tính bằng giây). |
| `path_to_raw` | `TEXT` | Đường dẫn đến file video `raw` trong hệ thống lưu trữ. |
| `path_to_edited`| `TEXT` | Đường dẫn đến file video `edited`. |
| `fcpxml_path` | `TEXT` | Đường dẫn đến file `FCPXML` tương ứng. |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | Dấu thời gian khi bản ghi được tạo. |

---

#### 2. `sentences` Table
*   **Purpose:** Stores sentence-level chunks and their macro-level analyses.
*   **Mục đích:** Lưu trữ các chunk cấp độ câu và các phân tích vĩ mô của chúng.

| Tên Cột | Kiểu Dữ liệu (PostgreSQL) | Mô tả |
| :--- | :--- | :--- |
| `id` | `SERIAL PRIMARY KEY` | ID tự tăng, khóa chính. |
| `source_id` | `INTEGER REFERENCES sources(id)` | Khóa ngoại, liên kết đến video nguồn. |
| `transcript` | `TEXT` | Nội dung văn bản đầy đủ của câu. |
| `start_time_ms`| `BIGINT NOT NULL` | Thời điểm bắt đầu của câu trong video `edited`. |
| `end_time_ms` | `BIGINT NOT NULL` | Thời điểm kết thúc của câu trong video `edited`. |
| `embedding` | `VECTOR(1024)` | Vector embedding đại diện cho toàn bộ câu (cho tìm kiếm ngữ nghĩa). |
| `acoustic_features` | `JSONB` | Một đối tượng JSON chứa các đặc trưng âm học (RMS, Pitch F0...). |
| `emotion_label`| `VARCHAR(50)` | Nhãn cảm xúc được phát hiện (ví dụ: 'calm', 'neutral'). |
| `audio_path_clean` | `TEXT UNIQUE` | Đường dẫn đến file audio `.wav` sạch của câu này. |
| `video_path_clean` | `TEXT UNIQUE` | Đường dẫn đến file video `.mp4` sạch của câu này. |

---

#### 3. `words` Table
*   **Purpose:** The core table for micro-level analysis of `clean` vs. `error` pairs.
*   **Mục đích:** Bảng cốt lõi cho việc phân tích vi mô các cặp `clean` và `error`.

| Tên Cột | Kiểu Dữ liệu (PostgreSQL) | Mô tả |
| :--- | :--- | :--- |
| `id` | `SERIAL PRIMARY KEY` | ID tự tăng, khóa chính. |
| `sentence_id` | `INTEGER REFERENCES sentences(id)` | Khóa ngoại, liên kết đến câu chứa từ này. |
| `word_text` | `TEXT NOT NULL` | Nội dung văn bản của từ. |
| `language` | `VARCHAR(5) NOT NULL` | Mã ngôn ngữ được phát hiện (ví dụ: 'vie', 'eng', 'fra'). |
| `start_time_ms_edited` | `BIGINT NOT NULL` | Thời điểm bắt đầu của từ trong video `edited`. |
| `end_time_ms_edited` | `BIGINT NOT NULL` | Thời điểm kết thúc của từ trong video `edited`. |
| `embedding_clean` | `VECTOR(1024)` | Vector embedding của chunk audio `clean`. |
| `embedding_error` | `VECTOR(1024)` | Vector embedding của chunk audio `error`. |
| `acoustic_features_diff` | `JSONB` | Một đối tượng JSON chứa sự khác biệt về đặc trưng âm học giữa `clean` và `error`. |
| `audio_path_clean` | `TEXT UNIQUE` | Đường dẫn đến file audio `.wav` sạch của từ này. |
| `audio_path_error` | `TEXT UNIQUE` | Đường dẫn đến file audio `.wav` lỗi của từ này. |
| `video_path_clean` | `TEXT UNIQUE` | Đường dẫn đến file video `.mp4` sạch của từ này. |
| `video_path_error` | `TEXT UNIQUE` | Đường dẫn đến file video `.mp4` lỗi của từ này. |
| `spectrogram_diff_path`| `TEXT` | (Tùy chọn) Đường dẫn đến file ảnh "phổ tần khác biệt". |

---

#### 4. `anomalies` Table
*   **Purpose:** A dedicated log for all detected non-speech events and technical errors.
*   **Mục đích:** Một bảng ghi chuyên dụng cho tất cả các sự kiện không phải lời nói và các lỗi kỹ thuật được phát hiện.

| Tên Cột | Kiểu Dữ liệu (PostgreSQL) | Mô tả |
| :--- | :--- | :--- |
| `id` | `SERIAL PRIMARY KEY` | ID tự tăng, khóa chính. |
| `source_id` | `INTEGER REFERENCES sources(id)` | Khóa ngoại, liên kết đến video nguồn. |
| `start_time_ms`| `BIGINT NOT NULL` | Thời điểm bắt đầu của sự kiện bất thường. |
| `end_time_ms` | `BIGINT NOT NULL` | Thời điểm kết thúc của sự kiện bất thường. |
| `anomaly_type` | `TEXT NOT NULL` | Loại bất thường (ví dụ: `cough`, `clipping`, `laughter`, `noise_spike`). |
| `confidence_score`| `FLOAT` | Độ tin cậy của mô hình khi phát hiện sự kiện này (0.0 đến 1.0). |
| `details` | `JSONB` | (Tùy chọn) Một đối tượng JSON chứa thêm chi tiết về lỗi. |
| `related_word_id` | `INTEGER REFERENCES words(id)` | (Nullable) Khóa ngoại, liên kết đến từ bị ảnh hưởng trực tiếp bởi lỗi này. |
| `related_sentence_id` | `INTEGER REFERENCES sentences(id)`| (Nullable) Khóa ngoại, liên kết đến câu bị ảnh hưởng bởi lỗi này. |

This detailed, relational schema provides maximum flexibility for complex queries and ensures data integrity as the project scales.
Lược đồ quan hệ chi tiết này cung cấp sự linh hoạt tối đa cho các truy vấn phức tạp và đảm bảo tính toàn vẹn của dữ liệu khi dự án mở rộng.