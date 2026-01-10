Đã rõ. Dưới đây là **Bản Đặc Tả Kiến Trúc & Chức Năng Hoàn Chỉnh (Phiên bản Cuối cùng)** cho IA MEDIA APP v2.0.

Bản này đã tích hợp toàn bộ các tính năng hiện có, các tính năng nâng cấp, và các feedback chi tiết của bạn về Benchmark, Data Factory, và Quản lý thống kê. Đây là tài liệu duy nhất bạn cần tham khảo để bắt đầu code.

---

# IA MEDIA APP (VERSION 2.0) - ARCHITECTURE & SPECIFICATION (FINAL)

**Mục tiêu:** Xây dựng một Nền tảng Huấn luyện & Sản xuất Dữ liệu AI khép kín, từ thu thập dữ liệu thô, sản xuất dữ liệu giả lập chất lượng cao, đến huấn luyện và kiểm thử mô hình nhận diện lỗi.

### CẤU TRÚC HỆ THỐNG
*   **Frontend:** `app_ui.py` (Streamlit)
*   **Backend:** `backend_core.py` (Logic AI, Audio Processing, Database)
*   **Data Engine:** `data_factory.py` (Background Mining, Synthesis Algorithms)
*   **Utils:** `fcpxml_utils.py` (FCPXML Generation)
*   **Storage:** File System (NAS/Local) + CSV Metadata (`training_data.csv`)

---

### CHI TIẾT CHỨC NĂNG TỪNG TAB

#### **TAB 1: DEEP SCAN VIDEO (NHẬN DIỆN LỖI - NÂNG CẤP)**
*Tập trung vào trải nghiệm người dùng tương tác và kiểm soát chi tiết.*

*   **Logic Cốt lõi:**
    *   Input: Đường dẫn file video Raw (Local Path) hoặc Upload file.
    *   Engine: Sử dụng model đã train (`error_classifier_sota.pkl`) và thuật toán Sliding Window.

*   **Tính năng Mới - Chế độ Quét Từng Phần (Interactive Step Scan):**
    *   **Button "Quét 60s đầu tiên":**
        *   Cắt 60 giây video từ vị trí hiện tại.
        *   Chạy model detect trên đoạn này.
        *   **Hiển thị:** Vẽ biểu đồ Waveform FCP Style ngay trên giao diện.
        *   **Highlight:** Tô đỏ các vùng sóng âm bị AI đánh dấu là lỗi.
    *   **Button "Quét tiếp 60s":**
        *   Lưu trạng thái con trỏ thời gian (cursor).
        *   Tiếp tục xử lý 60s tiếp theo và cập nhật biểu đồ.
        *   Giúp người dùng kiểm tra nhanh độ chính xác của model mà không cần đợi cả tiếng đồng hồ.

*   **Tính năng Cũ - Quét Toàn bộ (Batch Scan):**
    *   **Button "Quét Toàn bộ & Xuất XML":**
        *   Chạy ngầm (background process) trên toàn bộ video.
        *   Tạo file `.fcpxml` với đầy đủ marker.
        *   Hiển thị log chi tiết tiến trình.

---

#### **TAB 2: THU THẬP DỮ LIỆU (COLLECT - CẢI TIẾN LỚN)**
*Chuyển từ thu thập file đơn lẻ sang thu thập cặp dữ liệu (Paired Data) để phục vụ Data Factory.*

*   **Giao diện Nhập liệu:**
    *   **Label Input:** Ô nhập tên lỗi (ví dụ: `error_click`).
    *   **Type Selection:** Checkbox `Is Fake Sample?` (Mặc định: False - tức là Real Sample).
    *   **Upload Cặp File (Paired Upload):**
        *   **Slot 1:** File Lỗi (Raw/Error) - *Bắt buộc*.
        *   **Slot 2:** File Sạch (Clean/Edited) tương ứng - *Bắt buộc để tính Diff*.
    *   **Metadata Bổ sung:** Người dùng có thể nhập thêm ghi chú (ví dụ: "Tiếng ho trong phòng kín").

*   **Logic Xử lý (Backend):**
    *   **Auto-Align:** Khi upload, hệ thống tự động chạy Cross-Correlation để đồng bộ hóa 2 file này chính xác từng mẫu.
    *   **Diff Calculation:** Tự động tính toán `Diff_Audio = Raw - Clean` và lưu trữ file `.wav` Diff này vào thư mục riêng (`diff_bank`).
    *   **Lưu trữ:** Lưu cả 3 file (Raw, Clean, Diff) vào cấu trúc thư mục mới, kèm file CSV quản lý siêu dữ liệu (`is_fake`, `source_video`, `timestamp`, `path_clean`, `path_diff`...).

---

#### **TAB 3: HUẤN LUYỆN & KIỂM THỬ (TRAIN & BENCHMARK - HOÀN THIỆN)**
*Tách biệt mục đích huấn luyện để tối ưu hóa model và đánh giá hiệu suất.*

*   **Sub-tab 1: Train Error Detection (Nhận diện Lỗi):**
    *   **Dữ liệu:** Chỉ sử dụng các mẫu có nhãn `error_*` và các mẫu `clean` (đối chứng).
    *   **Input:** Vector đặc trưng (Wav2Vec2 1024-dim hoặc MFCCs).
    *   **Mục tiêu:** Phân loại Binary (Lỗi/Sạch) hoặc Multi-class (Click/Noise/Silence).
    *   **Output:** Model `error_classifier.pkl`.

*   **Sub-tab 2: Benchmark Model (Đánh giá Hiệu suất - Đã hoàn thiện):**
    *   **Chức năng:** Chạy kiểm thử đánh giá độ chính xác của Model theo từng nhãn.
    *   **Phương pháp:** Train/Test Split (80/20).
    *   **Hiển thị:**
        *   **Bảng điểm chi tiết:** Precision (Độ chính xác), Recall (Độ nhạy), F1-Score cho từng loại lỗi. Tô màu xanh cho các chỉ số tốt (>90%).
        *   **Confusion Matrix:** Biểu đồ nhiệt hiển thị sự nhầm lẫn giữa các nhãn.
        *   **Phân tích nhanh:** Hiển thị Metric tổng thể (Overall Accuracy) và cảnh báo nếu Accuracy < 80%.

*   **Sub-tab 3: Train Auto-Correction (Placeholder):**
    *   Hiển thị thông báo: "Tính năng đang phát triển (Coming Soon)".

---

#### **TAB 4: QUẢN LÝ & THỐNG KÊ (MANAGE - NÂNG CẤP)**
*Thêm các thống kê chi tiết về nguồn gốc dữ liệu.*

*   **Thống kê Tổng quan:** Tổng số mẫu, số lượng Label.
*   **Thống kê Real vs Fake (Mới):**
    *   Cập nhật biểu đồ (Stacked Bar Chart) để hiển thị tỷ lệ `Real` vs `Fake` cho từng loại lỗi. Giúp cân bằng dữ liệu.
*   **Thống kê Background:** Hiển thị số lượng mẫu nền (background samples) đang có trong kho.
*   **Quản lý Dữ liệu:**
    *   Danh sách file trong CSV (có thể lọc/sort).
    *   **Chức năng Xóa:** Thêm nút "Xóa toàn bộ Fake Data" hoặc "Xóa theo Label" để dọn dẹp dữ liệu rác nhanh chóng.

---

#### **TAB 5: DATA FACTORY (NHÀ MÁY DỮ LIỆU - CHỨC NĂNG MỚI)**
*Trái tim của việc sinh dữ liệu giả lập chất lượng cao.*

*   **Khu vực 1: Background Mining (Khai thác Nền):**
    *   **Input:** Đường dẫn video dài (ví dụ: video bài giảng 1 tiếng).
    *   **Validation:** Kiểm tra định dạng, âm thanh.
    *   **Settings:**
        *   `Clip Duration`: Độ dài mẫu nền (mặc định 1s).
        *   `Max Samples`: Số lượng tối đa muốn cắt.
    *   **Process & Quality Check:**
        *   Cắt video thành các đoạn nhỏ.
        *   Tự động loại bỏ các đoạn quá ồn hoặc chứa giọng nói quá lớn (để lấy nền tĩnh) hoặc ngược lại tùy mục đích.
        *   Lưu vào kho `background_bank`.

*   **Khu vực 2: Synthesis Engine (Cấy Lỗi):**
    *   **Input:**
        *   **Dropdown "Chọn Loại Lỗi":** Load danh sách các label lỗi hiện có (lọc từ CSV).
        *   **Table View:** Hiển thị danh sách các mẫu Diff (đã trích xuất ở Tab 2) của label đó. Chọn 1 mẫu để cấy.
    *   **Algorithm Selection (Dropdown):**
        1.  **Mix (Trộn cơ bản):** Cộng tín hiệu + Random vị trí + Random Gain.
        2.  **Time Stretch:** Thay đổi tốc độ lỗi (0.9x - 1.1x).
        3.  **Frequency Shift:** Dịch chuyển cao độ.
        4.  **Room Impulse Response (RIR):** Convolve với Impulse Response để giả lập vang phòng.
        5.  **Feature Grafting (Cao cấp):** Áp dụng thuật toán STFT -> Spectral Shaping -> Masking -> Inverse STFT để hòa trộn tần số lỗi vào nền.
        6.  **Shuffle:** Random chọn 1 trong 5 thuật toán trên cho mỗi mẫu sinh ra.
    *   **Input SNR:** Slider chọn khoảng độ to của nhiễu (ví dụ: từ -5dB đến +5dB so với nền).
    *   **Process:**
        *   Button "Sinh thử" -> Nghe thử audio kết quả.
        *   **Quality Grading:** Hệ thống tự động chấm điểm độ chân thực (ví dụ: dựa trên độ mượt phổ tần hoặc SNR).
    *   **Output:**
        *   Button "Lưu vào Kho" -> Ghi vào CSV với `is_fake=True`, sẵn sàng cho Tab 3 huấn luyện.

---

Đây là bản kế hoạch cuối cùng. Bạn có thể copy toàn bộ nội dung này vào file `TODO.md` hoặc tài liệu dự án để bắt đầu triển khai code.

tomorrow:
THÊM CHỨC NĂNG SAU VÀO TAB 2:
1. # Nút vẽ
    if st.button("🎨 Vẽ Biểu đồ So sánh", type="primary"):
        if f_raw and f_clean:
            with st.spinner("Đang đồng bộ hóa và vẽ sóng âm..."):
                # Gọi hàm vẽ từ backend
                fig, lag = backend_core.generate_comparison_plot(f_raw, f_clean)
                
                if fig:
                    st.pyplot(fig)
                    st.success(f"Đã tự động đồng bộ. Độ lệch: {lag} samples.")
                    
                    # Cho nghe thử
                    c1, c2 = st.columns(2)
                    with c1: 
                        st.write("🔊 Nghe Lỗi:")
                        st.audio(f_raw)
                    with c2: 
                        st.write("🔊 Nghe Sạch:")
                        st.audio(f_clean)
                else:
                    st.error("Không thể vẽ biểu đồ. Kiểm tra lại file âm thanh.")
        else:
            st.warning("Vui lòng chọn đủ cả file lỗi và file sạch.")

2. IMPLEMENT PHẦN UPDATE, CHO PHÉP UPLOAD MULTIPLE, CÓ THỂ SO SÁNH KHỚP DỰA VÀO TÊN FILES, ví drr ẻ
3. CHO UPLOAD CÁC FILE TYPE KHÁC NHƯ MOV