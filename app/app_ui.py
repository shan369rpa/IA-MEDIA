# app_ui.py
import streamlit as st
import pandas as pd
import os
import time
import backend_core
import fcpxml_utils
st.set_page_config(page_title="IA MEDIA Pro", page_icon="🎛️", layout="wide")

st.title("🎛️ IA MEDIA - Professional Audio Analysis")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 1. Phân tích & Log Chi tiết", 
    "📥 2. Thu thập Dữ liệu", 
    "🧠 3. Huấn luyện AI", 
    "📊 4. Phòng Lab"
])

# --- HÀM UI LOGGING CHUYÊN NGHIỆP ---
def ui_logger(status_container, log_container, progress_bar):
    """
    Tạo ra một hàm callback để truyền vào backend.
    """
    # Khởi tạo session state cho log nếu chưa có
    if 'process_logs' not in st.session_state:
        st.session_state.process_logs = []

    def callback(percent, title, details=""):
        # Cập nhật thanh tiến trình
        progress_bar.progress(percent)
        
        # Cập nhật trạng thái lớn
        status_container.markdown(f"### {title}")
        
        # Thêm log chi tiết vào danh sách
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {title}"
        if details:
            log_entry += f" - {details}"
            # Cập nhật text nhỏ bên dưới
            status_container.caption(details)
            
        st.session_state.process_logs.append(log_entry)
        
        # Hiển thị log (cuộn xuống cuối)
        log_text = "\n".join(st.session_state.process_logs)
        log_container.code(log_text, language="bash")
        
    return callback
# --- TAB 1: NHẬN DIỆN VỚI LOG CHI TIẾT (ĐÃ SỬA LỖI) ---
with tab1:
    st.subheader("Deep Scan Video")
    with st.expander("📖 HƯỚNG DẪN SỬ DỤNG", expanded=False):
        st.markdown(
        """
        Detect lỗi với 2 lớp bảo vệ:
        Lớp 1: SVM Classifier (Dự đoán loại lỗi).
        Lớp 2: Similarity Check (So với Mean Clean Vector).
        
        sensitivity_threshold: Ngưỡng khoảng cách (Distance Threshold).
        - Thấp (0.1): Rất chặt, chỉ báo lỗi nếu cực kỳ khác biệt (Ít báo động giả, nhưng dễ sót).
        - Cao (0.5): Rất nhạy, hơi khác tí là báo (Bắt hết lỗi, nhưng nhiều báo động giả).
        -> Mặc định 0.3 là điểm cân bằng.
        """
        )
    col_input, col_log = st.columns([1, 1.5])
            # Thêm vào cột Input
    st.markdown("#### ⚙️ Cấu hình Nâng cao")
    sensitivity = st.slider(
        "Độ nhạy (Similarity Threshold)", 
        min_value=0.0, max_value=1.0, value=0.3, step=0.05,
        help="Càng thấp càng chặt (ít báo lỗi sai). Càng cao càng nhạy (bắt nhiều lỗi hơn)."
    )
    with col_input:
        input_method = st.radio("Nguồn dữ liệu:", ["Upload File", "Đường dẫn File (Local Path)"])
        video_path = None
        
        # --- 1. XỬ LÝ ĐẦU VÀO ---
        if input_method == "Upload File":
            v_file = st.file_uploader("Video File", type=["mp4", "mov"])
            if v_file:
                video_path = f"temp_{v_file.name}"
                with open(video_path, "wb") as f: f.write(v_file.getbuffer())
        else:
            # Nhập đường dẫn
            raw_path = st.text_input("Nhập đường dẫn tuyệt đối:", placeholder="/Users/name/video.mp4")
            
            if raw_path:
                # Xử lý làm sạch đường dẫn (xóa ngoặc kép, khoảng trắng thừa)
                clean_path = raw_path.strip().strip('"').strip("'")
                
                # Kiểm tra tồn tại
                if os.path.exists(clean_path):
                    if os.path.isfile(clean_path):
                        video_path = clean_path
                        st.success(f"✅ Đã tìm thấy file: {os.path.basename(video_path)}")
                        st.caption(f"Path: `{video_path}`") # Debug path
                    else:
                        st.error("❌ Đường dẫn này là Thư mục, không phải File!")
                else:
                    st.error("❌ File không tồn tại! Vui lòng kiểm tra lại đường dẫn.")

        # --- 2. KIỂM TRA ĐIỀU KIỆN CHẠY ---
        # Kiểm tra xem file model đã có chưa
        model_exists = os.path.exists(backend_core.MODEL_FILE)
        
        if not model_exists:
            st.warning("⚠️ Chưa tìm thấy 'Bộ não' (Model). Vui lòng sang **Tab 3: Huấn luyện AI** để train model trước khi phân tích.")
            btn_analyze = st.button("🚀 Kích hoạt AI Engine", disabled=True) # Khóa nút nếu chưa có model
        else:
            btn_analyze = st.button("🚀 Kích hoạt AI Engine", type="primary", width='stretch')

    with col_log:
        st.markdown("#### 📟 Live Operations Log")
        status_box = st.empty()
        p_bar = st.progress(0)
        log_box = st.empty()

    # --- 3. XỬ LÝ SỰ KIỆN NÚT BẤM ---
    if btn_analyze:
        if not video_path:
            st.error("⚠️ Vui lòng chọn file hoặc nhập đường dẫn hợp lệ trước.")
        else:
            st.session_state.process_logs = [] # Reset log
            
            # Tạo callback kết nối UI
            logger_cb = ui_logger(status_box, log_box, p_bar)
            
            try:
                # Chạy Backend
                # errors, msg = backend_core.detect_errors_in_video(video_path, status_callback=logger_cb)
                errors, msg = backend_core.detect_errors_in_video(
                    video_path, 
                    status_callback=logger_cb,
                    sensitivity_threshold=sensitivity # <--- THAM SỐ MỚI
        )
                # --- 4. XỬ LÝ KẾT QUẢ TRẢ VỀ (LOGIC QUAN TRỌNG) ---
                with col_input:
                    # Trường hợp 1: Có lỗi được tìm thấy
                    if errors and len(errors) > 0:
                        st.success(f"✅ Tìm thấy {len(errors)} vấn đề!")
                        
                        # Nút tải XML
                        xml_name = os.path.basename(video_path) + ".fcpxml"
                        ok, xml_msg = fcpxml_utils.create_fcpxml(xml_name, video_path, errors)
                        if ok:
                            with open(xml_name, "rb") as f:
                                st.download_button("⬇️ Tải FCPXML Report", f, file_name=xml_name)
                        
                        st.dataframe(pd.DataFrame(errors)[['start', 'label']], height=300)
                    
                    # Trường hợp 2: Trả về rỗng nhưng thông báo lỗi (Backend return early)
                    elif "Lỗi" in msg or "Chưa có" in msg or "quá ngắn" in msg:
                        st.error(f"❌ Phân tích thất bại: {msg}")
                        st.error("Vui lòng kiểm tra Log bên phải để biết chi tiết.")
                    
                    # Trường hợp 3: Chạy thành công hết nhưng không tìm thấy lỗi nào
                    else:
                        st.balloons()
                        st.info("🎉 Video sạch sẽ! (AI không tìm thấy lỗi nào khớp với dữ liệu đã học)")
                        st.caption("Gợi ý: Nếu bạn chắc chắn video có lỗi, hãy nạp thêm dữ liệu mẫu vào Tab 2 và Train lại.")

            except Exception as e:
                st.error(f"🔥 Lỗi hệ thống nghiêm trọng: {e}")
# --- TAB 2: THU THẬP DỮ LIỆU ---
with tab2:
    with st.expander("📖 HƯỚNG DẪN SỬ DỤNG - THU THẬP DỮ LIỆU", expanded=False):
        st.markdown("""
        **Chức năng:** Dạy cho AI biết thế nào là "Lỗi" và thế nào là "Sạch".
        *   **Quan trọng:** Dữ liệu càng nhiều, AI càng thông minh.
        *   **Định dạng:** Chỉ chấp nhận file âm thanh (`.wav`, `.mp3`) đã được cắt ngắn (2-5 giây).
        """)

    st.subheader("Đóng góp dữ liệu huấn luyện")
    
    # Chia làm 2 cột hoặc 2 tab con để tách biệt rõ ràng
    tab_error, tab_clean = st.tabs(["❌ Thu thập MẪU LỖI (Raw)", "✅ Thu thập MẪU SẠCH (Edited)"])
    
    # --- SUB-TAB: THU THẬP LỖI ---
    with tab_error:
        st.markdown("### Dạy AI nhận biết lỗi")
        st.info("Upload các đoạn âm thanh chứa tiếng ồn, tiếng click, vỡ tiếng, v.v.")
        
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            error_type = st.selectbox(
                "Loại lỗi (Label)", 
                ["error_click (Tiếng Click/Pop)", "error_noise (Nhiễu nền)", "error_plosive (Bụp mic)", "error_clipping (Vỡ tiếng)", "Khác..."]
            )
            if error_type == "Khác...":
                error_type = st.text_input("Nhập tên lỗi mới (viết liền không dấu)", value="error_custom")
        
        with col_e2:
            files_error = st.file_uploader("Chọn file lỗi (.wav)", accept_multiple_files=True, key="u_error")
            
        if st.button("Lưu mẫu LỖI", type="primary"):
            if files_error:
                count = 0
                for f in files_error:
                    backend_core.save_training_data(f, error_type)
                    count += 1
                st.toast(f"Đã lưu {count} mẫu lỗi '{error_type}'!", icon="💾")
                st.success(f"Đã thêm {count} file vào kho dữ liệu LỖI.")
            else:
                st.warning("Chưa chọn file nào.")

 # --- SUB-TAB: THU THẬP SẠCH ---
    with tab_clean:
        st.markdown("### Dữ liệu đối chứng (Reference)")
        st.info("Upload các đoạn âm thanh ĐÃ QUA CHỈNH SỬA (Sạch). Hãy chỉ rõ đây là kết quả sau khi sửa lỗi gì.")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            # Nâng cấp: Cho phép chọn loại sạch cụ thể
            clean_option = st.selectbox(
                "Định loại mẫu Sạch (Clean Context)", 
                [
                    "clean_general (Sạch chung/Không rõ nguồn)", 
                    "clean_fixed_noise (Đã khử nhiễu nền)", 
                    "clean_fixed_click (Đã khử tiếng Click)", 
                    "clean_fixed_clipping (Đã sửa Vỡ tiếng)", 
                    "clean_fixed_plosive (Đã sửa Bụp mic)",
                    "Khác..."
                ]
            )
            
            # Xử lý logic lấy tên nhãn
            if clean_option == "Khác...":
                clean_label = st.text_input("Nhập tên nhãn sạch mới", value="clean_custom")
            else:
                # Lấy phần text trước dấu ngoặc đơn. VD: "clean_fixed_noise"
                clean_label = clean_option.split(" ")[0]
            
            st.caption(f"👉 Nhãn sẽ lưu vào hệ thống: **{clean_label}**")
        
        with col_c2:
            files_clean = st.file_uploader("Chọn file sạch (.wav)", accept_multiple_files=True, key="u_clean")

        if st.button("Lưu mẫu SẠCH", type="primary"):
            if files_clean:
                count = 0
                for f in files_clean:
                    backend_core.save_training_data(f, clean_label)
                    count += 1
                st.toast(f"Đã lưu {count} mẫu '{clean_label}'!", icon="💾")
                st.success(f"Đã thêm {count} file vào kho dữ liệu SẠCH (Loại: {clean_label}).")
            else:
                st.warning("Chưa chọn file nào.")

# --- TAB 2 & 3: CẬP NHẬT CALLBACK CHO TRAIN ---
# (Logic tương tự, tôi sẽ tóm tắt phần gọi hàm)
with tab3:
    st.header("Huấn luyện Mô hình")
    
    tab_train, tab_bench = st.tabs(["🚀 Huấn luyện (Train)", "📈 Đánh giá Hiệu suất (Benchmark)"])
    with tab_train:
        st.info("Huấn luyện model trên TOÀN BỘ dữ liệu để sử dụng thực tế.")
        if st.button("🧠 Retrain Model"):
            status_box = st.empty()
            p_bar = st.progress(0)
            log_box = st.empty()
            
            # Callback đơn giản hơn cho train (chỉ 2 tham số)
            def train_cb(p, msg):
                p_bar.progress(p)
                status_box.info(msg)
                log_box.code(f"{msg}")

            success, msg = backend_core.train_model_from_csv(status_callback=train_cb)
            if success: st.balloons()
    # --- SUB-TAB BENCHMARK (MỚI) ---
    with tab_bench:
        st.markdown("""
        **Chức năng:** Kiểm tra xem Model thông minh đến đâu bằng cách cho thi thử.
        *   Hệ thống sẽ dùng 80% dữ liệu để học và 20% để thi.
        *   **Precision (Độ chính xác):** Khi AI báo lỗi A, bao nhiêu % là đúng?
        *   **Recall (Độ nhạy):** AI tìm được bao nhiêu % lỗi A trong thực tế?
        """)
        
        if st.button("📊 Chạy Benchmark"):
            with st.spinner("Đang chạy kiểm thử trên M2 Ultra..."):
                success, msg, report_data, fig = backend_core.run_benchmark_test()
                
            if success:
                st.success(msg)
                
                # 1. Hiển thị Bảng điểm chi tiết
                # Chuyển đổi dict thành dataframe đẹp
                report_df = pd.DataFrame(report_data).transpose()
                # Format số %
                report_df['precision'] = report_df['precision'].apply(lambda x: f"{x:.1%}")
                report_df['recall'] = report_df['recall'].apply(lambda x: f"{x:.1%}")
                report_df['f1-score'] = report_df['f1-score'].apply(lambda x: f"{x:.1%}")
                
                # Tô màu các hàng quan trọng
                st.markdown("### 🎯 Bảng điểm chi tiết theo Nhãn")
                st.dataframe(
                    report_df.style.applymap(
                        lambda x: "background-color: #d4edda; color: green; font-weight: bold" if isinstance(x, str) and "%" in x and float(x.strip('%')) > 90 else "",
                        subset=['precision', 'recall', 'f1-score']
                    )
                )

                # 2. Hiển thị Confusion Matrix
                st.markdown("### 🧩 Ma trận nhầm lẫn")
                st.caption("Trục dọc là Nhãn Thực Tế. Trục ngang là AI Dự Đoán. Đường chéo đậm là tốt.")
                st.pyplot(fig)
                
                # 3. Phân tích nhanh
                acc = report_data['accuracy']
                st.metric("Độ chính xác tổng thể (Overall Accuracy)", f"{acc:.1%}")
                if acc < 0.8:
                    st.error("⚠️ Model chưa đủ tốt. Cần thu thập thêm dữ liệu cho các nhãn bị sai nhiều.")
                else:
                    st.success("✅ Model hoạt động ổn định!")

            else:
                st.error(f"Lỗi: {msg}")
# --- TAB 4: QUẢN LÝ & VISUALIZE ---
with tab4:
    st.header("🔬 Phòng Lab Phân tích (Visual & Stats)")
    
    # Load dữ liệu CSV
    if os.path.exists(backend_core.DATA_CSV):
        df = pd.read_csv(backend_core.DATA_CSV)
    else:
        df = pd.DataFrame(columns=["filepath", "label"])

    if df.empty:
        st.warning("Chưa có dữ liệu. Hãy thu thập thêm ở Tab 2.")
    else:
        # --- PHẦN 1: THỐNG KÊ (Giữ nguyên nhưng gọn hơn) ---
        with st.expander("📊 Xem Thống kê Tổng quan", expanded=False):
            stats = df['label'].value_counts().reset_index()
            stats.columns = ['Nhãn', 'Số lượng']
            col_s1, col_s2 = st.columns(2)
            with col_s1: st.bar_chart(stats.set_index('Nhãn'))
            with col_s2: st.dataframe(stats, width='stretch')

        st.markdown("---")
        
        # --- PHẦN 2: SO SÁNH WAVEFORM (TÍNH NĂNG MỚI) ---
        st.subheader("🔍 So sánh Sóng âm (FCP Style)")
        st.caption("Chọn một cặp file (Lỗi vs Sạch) để xem AI nhìn thấy sự khác biệt như thế nào.")

        col_viz1, col_viz2 = st.columns(2)
        
        # Cột trái: Chọn file Lỗi
        with col_viz1:
            st.markdown("**:red[1. Chọn Mẫu Lỗi (Raw)]**")
            # Lọc chỉ lấy các label bắt đầu bằng 'error'
            error_labels = [l for l in df['label'].unique() if 'error' in l.lower()]
            if not error_labels: error_labels = df['label'].unique()
            
            selected_err_label = st.selectbox("Loại lỗi:", error_labels)
            # Lọc file theo label
            err_files = df[df['label'] == selected_err_label]['filepath'].tolist()
            # Hiển thị tên file ngắn gọn hơn
            err_file_map = {os.path.basename(f): f for f in err_files}
            selected_err_file_name = st.selectbox("File mẫu:", list(err_file_map.keys()))
            real_err_path = err_file_map.get(selected_err_file_name)

        # Cột phải: Chọn file Sạch đối chứng
        with col_viz2:
            st.markdown("**:green[2. Chọn Mẫu Sạch (Clean/Reference)]**")
            # Lọc chỉ lấy label 'clean'
            clean_labels = [l for l in df['label'].unique() if 'clean' in l.lower()]
            if not clean_labels: clean_labels = df['label'].unique()

            selected_clean_label = st.selectbox("Loại sạch:", clean_labels)
            clean_files = df[df['label'] == selected_clean_label]['filepath'].tolist()
            
            clean_file_map = {os.path.basename(f): f for f in clean_files}
            
            # Gợi ý thông minh: Tự chọn file có tên gần giống nhất (nếu bạn đặt tên file giống nhau)
            suggested_index = 0
            if selected_err_file_name:
                # Logic đơn giản: tìm file sạch có tên trùng khớp phần đầu
                base_name = selected_err_file_name.split('.')[0]
                for idx, fname in enumerate(clean_file_map.keys()):
                    if base_name in fname:
                        suggested_index = idx
                        break
            
            selected_clean_file_name = st.selectbox("File đối chứng:", list(clean_file_map.keys()), index=suggested_index)
            real_clean_path = clean_file_map.get(selected_clean_file_name)

        # Nút vẽ
        if st.button("🎨 Vẽ Biểu đồ So sánh", type="primary"):
            if real_err_path and real_clean_path:
                with st.spinner("Đang đồng bộ hóa và vẽ sóng âm..."):
                    # Gọi hàm vẽ từ backend
                    fig, lag = backend_core.generate_comparison_plot(real_err_path, real_clean_path)
                    
                    if fig:
                        st.pyplot(fig)
                        st.success(f"Đã tự động đồng bộ. Độ lệch: {lag} samples.")
                        
                        # Cho nghe thử
                        c1, c2 = st.columns(2)
                        with c1: 
                            st.write("🔊 Nghe Lỗi:")
                            st.audio(real_err_path)
                        with c2: 
                            st.write("🔊 Nghe Sạch:")
                            st.audio(real_clean_path)
                    else:
                        st.error("Không thể vẽ biểu đồ. Kiểm tra lại file âm thanh.")
            else:
                st.warning("Vui lòng chọn đủ cả file lỗi và file sạch.")
# Footer
st.markdown("---")
st.caption("IA MEDIA Project - Developed for Zen Master Thich Nhat Hanh's Dharma Talks Restoration.")