# IA MEDIA Project - Technical Overview
## Dự án IA MEDIA - Tổng quan Kỹ thuật

**Version:** 1.0
**Date:** 2025-12-15

---

## 1. Project Goal / Mục tiêu Dự án

**EN:** The goal of the IA MEDIA project is to build an open-source pipeline that automates the detection and classification of audio defects in a large corpus of dharma talk videos. The system leverages a unique dataset of `raw` vs. human-`edited` video pairs to learn error signatures. The final deliverable for a new video is an FCPXML file with colored "To-Do Markers" that pinpoints potential errors, significantly accelerating the manual editing workflow.

***VI:** Mục tiêu của dự án IA MEDIA là xây dựng một pipeline mã nguồn mở giúp tự động hóa việc phát hiện và phân loại các lỗi âm thanh trong một kho video pháp thoại lớn. Hệ thống tận dụng một bộ dữ liệu độc đáo gồm các cặp video `thô` và đã được con người `chỉnh sửa` để học các "dấu hiệu lỗi". Sản phẩm đầu ra cuối cùng cho một video mới là một file FCPXML với các "Marker Công việc" được tô màu, chỉ ra chính xác các lỗi tiềm ẩn, giúp tăng tốc đáng kể quy trình chỉnh sửa thủ công.*

---

## 2. Core Technologies / Công nghệ Cốt lõi

-   **Language:** Python 3.10
-   **AI Frameworks:** PyTorch, Transformers, SpeechBrain
-   **Key Libraries:** `WhisperX` (for Transcription & Alignment), `psycopg2-binary` (DB), `pydub`, `librosa` (Audio), `scikit-learn` (ML).
-   **Database:** PostgreSQL + `pgvector`
-   **Compute:** Local NVIDIA GPU (RTX 4070 Ti), Google Colab (for community).

---

## 3. Current Status: Phase 1 Demo Completed / Trạng thái Hiện tại: Demo Giai đoạn 1 Hoàn thành

We have successfully completed a full end-to-end demonstration of the pipeline.
*Chúng ta đã thực thi thành công một bản demo hoàn chỉnh từ đầu đến cuối của pipeline.*

### What We Have Done / Những gì Đã làm được:

1.  **Data Ingestion Pipeline (SUCCESS):**
    -   Successfully processed a sample video pair using `main.py`. The pipeline correctly parsed the FCPXML, ran WhisperX (`large-v2`) for transcription and alignment, and generated **2,290 pairs** of `clean`/`error` audio chunks.
    -   Successfully ran the `vectorize.py` pipeline. It generated `SpeechBrain` embeddings (192-dim) for all chunks and successfully ingested **2,290 records** into our multi-table PostgreSQL database.

2.  **Initial Data Analysis (SUCCESS):**
    -   We analyzed the generated vector data and visualized the distributions, which confirmed the presence of a strong signal for training a model.
    -   *Chúng tôi đã phân tích dữ liệu vector được tạo ra và trực quan hóa các phân bố, xác nhận sự hiện diện của một tín hiệu mạnh mẽ để huấn luyện mô hình.*

    **Distance Distribution between Clean/Error Pairs:**
    *Phân bố Khoảng cách giữa các cặp Clean/Error:*
    ![Distance Distribution](https://raw.githubusercontent.com/shan369rpa/IA-MEDIA/dev/distance_distribution.png)

    **PCA Visualization of Difference Vectors:**
    *Trực quan hóa PCA của các Vector Khác biệt:*
    ![PCA Visualization](https://raw.githubusercontent.com/shan369rpa/IA-MEDIA/dev/diff_vector_pca.png)

3.  **Model Training (SUCCESS):**
    -   Successfully trained a `KNeighborsClassifier` model using `scikit-learn` on the difference vectors (`embedding_error` - `embedding_clean`).
    -   The trained model has been saved to **`error_classifier.pkl`**. Initial tests show an overall accuracy of 96%, with excellent performance on the majority class (`error_pronunciation`).
    -   *Đã huấn luyện thành công mô hình `KNeighborsClassifier` và lưu ra file **`error_classifier.pkl`**. Các kiểm thử ban đầu cho thấy độ chính xác tổng thể 96%, với hiệu suất xuất sắc trên lớp đa số.*
    
4.  **Inference & Report Generation (SUCCESS):**
    -   Successfully ran the `analyze_new_video.py` script on a new raw video.
    -   The script correctly used the trained `error_classifier.pkl` model to predict error types.
    -   It successfully generated a final **FCPXML To-Do List** with colored markers indicating potential errors.
    -   *Đã chạy thành công script `analyze_new_video.py` trên một video thô mới, sử dụng model đã huấn luyện để dự đoán lỗi, và đã tạo ra thành công một **file FCPXML To-Do List** cuối cùng.*

    **Example FCPXML Output:**
    *Ví dụ về File FCPXML Đầu ra:*
    ```xml
    ...
    <marker start="287588/600s" duration="48/600s" value="Lỗi volume tại từ: 'trẻ'" completed="0" note="Marker ID: 6">
        <keyword start="287588/600s" duration="48/600s" value="AI-Volume" note="Blue"/>
    </marker>
    <marker start="713075/600s" duration="1009/600s" value="Lỗi noise_spike tại từ: 'tư'" completed="0" note="Marker ID: 15">
        <keyword start="713075/600s" duration="1009/600s" value="AI-Noise" note="Purple"/>
    </marker>
    ...
    ```

---

## 4. Next Steps / Các Bước Tiếp theo

While the initial demo was successful, there are clear areas for improvement before scaling up.
*Mặc dù bản demo ban đầu đã thành công, có những lĩnh vực rõ ràng cần cải thiện trước khi mở rộng quy mô.*

### Immediate Tasks / Các Công việc Trước mắt:

1.  **Human Feedback Loop / Vòng lặp Phản hồi Con người:**
    -   **Action:** Send the generated FCPXML report to the Media Team for verification.
    -   **Goal:** Collect their feedback (which markers are correct/incorrect) to create a "ground truth" validation set. We need to build a script (`scripts/parse_feedback.py`) to parse their exported FCPXML feedback file.

2.  **Model Improvement / Cải thiện Mô hình:**
    -   **Problem:** The current KNN model performs poorly on minority error classes (e.g., `clipping`, `noise_spike`) due to severe data imbalance.
    -   **Action:** Begin experimenting with techniques to handle imbalanced data.
    -   **Next Branch:** `feature/improve-classifier-with-smote`.
    -   *Vấn đề: Mô hình KNN hiện tại hoạt động kém trên các lớp lỗi thiểu số do dữ liệu mất cân bằng. Hành động: Bắt đầu thử nghiệm các kỹ thuật xử lý dữ liệu mất cân bằng.*

3.  **Refine Feature Engineering / Tinh chỉnh Kỹ thuật Đặc trưng:**
    -   **Problem:** The current input feature is a simple vector difference.
    -   **Action:** Experiment with alternative features. For example, concatenate `[clean_embedding, error_embedding]` or use a combination of vector difference and acoustic features from `signal_analyzer.py`.
    -   **Next Branch:** `feature/experiment-new-input-features`.
    -   *Vấn đề: Đặc trưng đầu vào hiện tại là một vector hiệu đơn giản. Hành động: Thử nghiệm với các đặc trưng thay thế.*

### Long-term Goals (Phase 2) / Mục tiêu Dài hạn (Giai đoạn 2):

-   **Implement Sentence-level Chunking:** To analyze prosody and prepare data for TTS.
-   **Implement Word-level Language ID:** To correctly handle foreign words.
-   **Publish Dataset v0.1:** Prepare and upload the first version of our dataset (metadata + Internet Archive links) to the Hugging Face Hub.

---