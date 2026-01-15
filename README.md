# IA MEDIA Project - Intelligent Audio Restoration Platform
## Dự án IA MEDIA - Nền tảng Phục hồi Âm thanh Thông minh

**Version:** 1.0 (MVP Completed)
**Status:** ✅ Stable / Researching v2.0
**Hardware:** Optimized for Apple Silicon (M2 Ultra)

---

## 1. Executive Summary / Tóm tắt Dự án

**IA MEDIA** is a specialized AI-powered application designed to automate the post-production workflow for dharma talk videos. It leverages advanced deep learning models to detect, classify, and visualize audio defects such as clipping, noise, and pronunciation errors.

The project has successfully transitioned from a concept to a fully functional MVP running locally on macOS, featuring a seamless integration with Final Cut Pro via FCPXML.

*IA MEDIA là một ứng dụng AI chuyên dụng được thiết kế để tự động hóa quy trình hậu kỳ cho các video pháp thoại. Nó tận dụng các mô hình học sâu tiên tiến để phát hiện, phân loại và trực quan hóa các lỗi âm thanh như vỡ tiếng, nhiễu và lỗi phát âm. Dự án đã chuyển đổi thành công từ ý tưởng sang một MVP hoạt động hoàn chỉnh trên macOS, tích hợp mượt mà với Final Cut Pro thông qua FCPXML.*

---

## 2. Key Features (v1.0) / Tính năng Chính

The current application provides a comprehensive suite of tools for audio analysis:
*Ứng dụng hiện tại cung cấp bộ công cụ toàn diện để phân tích âm thanh:*

### 🔍 Deep Scan Video (Interactive Inference)
-   **Interactive Waveform:** Real-time visualization of audio signals with Final Cut Pro-style UI.
-   **Smart Hunting:** Automatically skips clean segments to find and highlight errors instantly.
-   **Output:** Generates precision FCPXML reports with colored markers for immediate import.

### 📥 Data Collection & Factory
-   **Paired Data Ingestion:** Systematically collects Raw/Clean pairs to build a ground-truth dataset.
-   **Auto-Alignment:** Uses Cross-Correlation to synchronize audio samples with millisecond accuracy.
-   **Difference Extraction:** Automatically isolates noise artifacts (clicks, pops) for training.

### 🧠 Model Training & Benchmarking
-   **Engine:** Wav2Vec 2.0 (XLSR-53) for feature extraction + SVM Classifier.
-   **Benchmark Suite:** Built-in tools to evaluate model performance (Precision, Recall, Confusion Matrix).

### 📊 Management Dashboard
-   **Data Analytics:** Visualizes the distribution of Real vs. Fake samples.
-   **Asset Management:** Tools to manage and clean the training dataset.

---

## 3. Technical Architecture / Kiến trúc Kỹ thuật

-   **Platform:** Python 3.10 + Streamlit (Frontend).
-   **Compute:** PyTorch (MPS Accelerated for Apple Silicon).
-   **Models:**
    -   *Embedding:* `facebook/wav2vec2-large-xlsr-53` (1024-dim).
    -   *Transcription:* WhisperX (Large-v2) with Forced Alignment.
-   **Storage:** Local Filesystem (NAS Support) + CSV Metadata.
-   **Processing:**
    -   Batch Processing for high-throughput ingestion.
    -   Sliding Window with Adaptive Stride for inference.

---

## 4. Research & Future Direction (v2.0 Roadmap) / Hướng đi Nghiên cứu & Tương lai

While v1.0 establishes a solid foundation, initial benchmarks on small datasets (100 samples) indicate the need for a strategic shift to achieve >98% accuracy. We are moving towards a **"Synthetic Data First"** approach.
*Trong khi v1.0 thiết lập một nền tảng vững chắc, các kiểm thử ban đầu trên tập dữ liệu nhỏ (100 mẫu) cho thấy cần một sự thay đổi chiến lược để đạt độ chính xác >98%. Chúng tôi đang chuyển sang hướng tiếp cận **"Ưu tiên Dữ liệu Giả lập"**.*

### Strategic Pivots for v2.0:

1.  **Data Factory Revolution (Synthetic Data):**
    -   Instead of relying solely on scarce real-world errors, we will build a **Data Synthesizer**.
    -   **Method:** Mathematically inject isolated noise artifacts (from Diff bank) into clean backgrounds using DSP techniques (Mixing, Spectral Grafting).
    -   **Goal:** Generate 10,000+ high-quality training samples to teach the model the "physics" of audio errors.

2.  **Hybrid Detection Architecture:**
    -   **Vision AI (Spectrograms):** Use CNNs (ResNet/EfficientNet) to "see" technical errors (clicks, pops, clipping) on Mel-Spectrogram images.
    -   **Audio AI (Wav2Vec2):** Use Transformers to "hear" linguistic and prosodic errors.
    -   **Fusion:** Combine both signals for robust decision-making.

3.  **MLX Migration:**
    -   Migrate core inference logic to Apple's **MLX framework** to fully exploit the 800GB/s memory bandwidth of the M2 Ultra.

---

## 5. Getting Started / Bắt đầu

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    brew install ffmpeg # Required for audio processing
    ```
2.  **Run the App:**
    ```bash
    streamlit run app_ui.py
    ```
3.  **Workflow:**
    -   Go to **Tab 2** to ingest initial Raw/Clean pairs.
    -   Go to **Tab 5** (Future) to synthesize massive training data.
    -   Go to **Tab 3** to train the model.
    -   Go to **Tab 1** to scan new videos.

---

**Repository Maintainer:** [Tên của bạn]
**Last Updated:** Jan 2026