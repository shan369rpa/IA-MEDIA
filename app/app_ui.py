# app_ui.py
import streamlit as st
import pandas as pd
import os
import time
import backend_core
# import fcpxml_utils
import data_factory # Module vừa tạo
import random
st.set_page_config(page_title="IA MEDIA Pro", page_icon="🎛️", layout="wide")

st.title("🎛️ IA MEDIA - Professional Audio Analysis")
st.markdown("---")

tab1, tab2, tab3, tab4,tab5 = st.tabs([
    "🔍 1. Phân tích & Log Chi tiết", 
    "📥 2. Thu thập Dữ liệu", 
    "🧠 3. Huấn luyện AI", 
    "📊 4. Phòng Lab",
    "🏭 5. Data Factory"
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
# --- TAB 1: DEEP SCAN VIDEO (INTERACTIVE) ---
with tab1:
    st.subheader("Deep Scan Video (Interactive Mode)")
    
    # 1. Input
    col_input, col_status = st.columns([2, 1])
    with col_input:
        video_path_input = st.text_input("Đường dẫn Video (Local Path)", placeholder="/Users/name/video.mp4")
        
        # Xử lý path
        video_path = None
        if video_path_input:
            clean_path = video_path_input.strip().strip('"').strip("'")
            if os.path.exists(clean_path) and os.path.isfile(clean_path):
                video_path = clean_path
                st.success(f"File OK: {os.path.basename(video_path)}")
            else:
                st.error("File không tồn tại.")

    # 2. State Management (Quản lý con trỏ thời gian)
    if 'scan_cursor' not in st.session_state:
        st.session_state.scan_cursor = 0.0
    if 'current_video' not in st.session_state:
        st.session_state.current_video = ""

    # Reset cursor nếu đổi video
    if video_path and video_path != st.session_state.current_video:
        st.session_state.scan_cursor = 0.0
        st.session_state.current_video = video_path

    # 3. Action Buttons
    col_btn1, col_btn2 = st.columns(2)

    
    # --- SỬA LẠI HÀM SĂN LỖI ĐỂ CẬP NHẬT UI ---
    def hunt_next_error(start_time, status_placeholder):
        """
        Hàm săn lỗi có khả năng cập nhật giao diện realtime.
        """
        current_t = start_time
        max_duration = 3600 * 5 
        
        # Thanh tiến trình giả lập (để người dùng thấy nó đang chạy)
        p_bar = st.progress(0)
        
        while current_t < max_duration:
            # CẬP NHẬT UI: Báo cáo đang quét đoạn nào
            mins = int(current_t // 60)
            secs = int(current_t % 60)
            status_placeholder.info(f"🤖 Đang quét đoạn: **{mins}p {secs}s** ... (Chưa thấy lỗi)")
            
            # Chạy Backend (Chỉ 60s)
            errors, y, sr, msg = backend_core.detect_segment(video_path, start_time=current_t, duration=60.0)
            
            if msg == "Hết video (End of file).":
                p_bar.empty()
                return None, None, None, current_t, "Đã quét hết video."
            
            if errors: # BINGO!
                p_bar.empty()
                return errors, y, sr, current_t, "Found"
            
            # Nếu sạch, nhảy cóc
            current_t += 60.0
            
            # Update thanh progress cho vui mắt (reset mỗi 10 phút)
            p_bar.progress((current_t % 600) / 600)
            
        return None, None, None, current_t, "Timeout."

    with col_btn1:
        if st.button("🔍 Săn lỗi đầu tiên (Skip clean)", type="primary", disabled=not video_path):
            st.session_state.scan_cursor = 0.0
            st.session_state.is_hunting = True
            
    with col_btn2:
        if st.button("⏭️ Nhảy đến lỗi tiếp theo", disabled=not video_path):
            st.session_state.scan_cursor += 60.0 # Bắt đầu từ đoạn sau
            st.session_state.is_hunting = True

    # 4. Thực thi Săn lỗi
    if st.session_state.get('is_hunting') and video_path:
        status_text = st.empty()
        status_text.info(f"🤖 AI đang săn lỗi bắt đầu từ {int(st.session_state.scan_cursor)}s... (Đang bỏ qua đoạn sạch)")
        
        # Chạy hàm săn lỗi
        errors, y, sr, found_time, msg = hunt_next_error(st.session_state.scan_cursor, status_text)

        if msg == "Found":
            st.session_state.scan_cursor = found_time # Cập nhật con trỏ đến chỗ có lỗi
            mins = int(found_time // 60)
            secs = int(found_time % 60)
            status_text.success(f"🚨 **DỪNG LẠI!** Phát hiện lỗi tại **{mins}p {secs}s**")
            # status_text.success(f"🚨 Đã bắt được lỗi tại {int(found_time)}s!")
            
            # --- Hiển thị Kết quả (Giống cũ) ---
            st.markdown("##### Waveform Visualizer")
            fig = backend_core.plot_interactive_waveform(y, sr, errors, found_time)
            st.pyplot(fig)
            
            # Audio
            import soundfile as sf
            temp_segment = "temp_segment_preview.wav"
            sf.write(temp_segment, y, sr)
            st.audio(temp_segment)
            
            # Bảng lỗi
            df_err = pd.DataFrame(errors)
            df_err['Time'] = df_err['start_abs'].apply(lambda x: f"{int(x//60):02}:{int(x%60):02}")
            st.dataframe(df_err[['Time', 'label']], use_container_width=True)
            
        elif "Hết video" in msg:
            status_text.warning("🏁 Đã quét hết video. Không còn lỗi nào nữa.")
        else:
            status_text.error(msg)
            
        st.session_state.is_hunting = False # Tắt cờ chạy

    # Hiển thị vị trí hiện tại
    st.caption(f"📍 Vị trí quét hiện tại: {st.session_state.scan_cursor}s")
    
# --- TAB 2: THU THẬP DỮ LIỆU (ADVANCED) ---
with tab2:
    st.header("📥 Thu thập Dữ liệu (Batch Collection)")
    st.info("Hỗ trợ upload hàng loạt. Hệ thống sẽ tự động ghép cặp dựa trên tên file.")
    with st.expander("📖 HƯỚNG DẪN SỬ DỤNG", expanded=False):
        st.markdown(
        """
        1. Chuẩn bị file:
        - File LỖI (Raw): Đặt tên file theo định dạng `tênfile_raw.ext` (ví dụ: `clip1_raw.wav`).
        - File SẠCH (Clean): Đặt tên file theo định dạng `tênfile_clean.ext` (ví dụ: `clip1_clean.wav`).
        2. Upload:
        - Sử dụng hai khung upload để tải lên danh sách file LỖI và SẠCH tương ứng.
        3. Ghép cặp & Xem trước:
        - Hệ thống sẽ tự động ghép cặp file dựa trên tên.
        - Bạn có thể nghe thử từng cặp và vẽ biểu đồ sóng âm để so sánh.
        4. Lưu trữ:
        - Nhập Tên lỗi (Label) chung cho tất cả cặp.
        - Nhấn nút "Lưu tất cả" để lưu vào kho dữ liệu.
        Lưu ý:
        - Đảm bảo tên file LỖI và SẠCH khớp nhau (ngoại trừ phần `_raw` và `_clean`).
        - Hệ thống hỗ trợ nhiều định dạng: wav, mp3, mp4, mov, m4a.
        """
        )
        
    # --- [MỚI] TOOL TỰ ĐỘNG CHUẨN HÓA TÊN FILE TỪ LOCAL ---
    with st.expander("🛠️ Công cụ: Chuẩn hóa & Sắp xếp File Local (Dành cho máy chủ/Local)", expanded=False):
        st.info("Công cụ này giúp đổi tên các file 'lỗi-ABC.wav' -> 'ABC_raw.wav' và gom vào thư mục chuẩn để dễ upload.")
        
        local_scan_path = st.text_input("Nhập đường dẫn thư mục chứa file lộn xộn:", placeholder="/Users/name/Downloads/Mau_Thu")
        
        if st.button("Sắp xếp & Đổi tên Tự động"):
            if local_scan_path:
                with st.spinner("Đang quét và xử lý..."):
                    ok, log_msg = backend_core.auto_organize_local_folder(local_scan_path)
                    if ok:
                        st.success("Xử lý xong!")
                        st.text_area("Chi tiết log:", value=log_msg, height=200)
                    else:
                        st.error(log_msg)
            else:
                st.warning("Vui lòng nhập đường dẫn.")
    
    st.markdown("---")
    col_meta, col_upload = st.columns([1, 2])
    
    with col_meta:
        label_input = st.text_input("Tên lỗi (Label)", placeholder="VD: error_click")
        is_fake = st.checkbox("Mẫu Fake (Giả lập)?", value=False)
        note = st.text_area("Ghi chú")
    
    with col_upload:
        # Hỗ trợ nhiều định dạng
        accepted_types = ["wav", "mp3", "mp4", "mov", "m4a"]
        files_raw = st.file_uploader("1. Danh sách file LỖI (Raw)", type=accepted_types, accept_multiple_files=True, key="u_raw_multi")
        files_clean = st.file_uploader("2. Danh sách file SẠCH (Clean)", type=accepted_types, accept_multiple_files=True, key="u_clean_multi")

    st.markdown("---")

    # --- LOGIC GHÉP CẶP & REVIEW ---
    if files_raw and files_clean:
        # Gọi hàm ghép cặp
        pairs, unmatched_raw, unmatched_clean = backend_core.match_files_by_name(files_raw, files_clean)
                # 2. Hiển thị File Cô đơn (Unmatched) - PHẦN MỚI
        if unmatched_raw or unmatched_clean:
            st.markdown("---")
            st.subheader("⚠️ Các file chưa ghép được cặp (Unmatched)")
            st.caption("Nguyên nhân: Tên file không khớp hoặc thiếu file đối ứng.")
            
            c_err, c_clean = st.columns(2)
            
            with c_err:
                if unmatched_raw:
                    st.error(f"**{len(unmatched_raw)} File Lỗi (Raw) chưa có cặp:**")
                    for f in unmatched_raw:
                        st.write(f"- 📄 `{f.name}`")
                else:
                    st.success("Tất cả file Raw đã được ghép.")
                    
            with c_clean:
                if unmatched_clean:
                    st.warning(f"**{len(unmatched_clean)} File Sạch (Clean) chưa có cặp:**")
                    for f in unmatched_clean:
                        st.write(f"- 📄 `{f.name}`")
                else:
                    st.success("Tất cả file Clean đã được ghép.")  
        if not pairs:
            st.warning("⚠️ Không tìm thấy cặp file nào khớp tên. Vui lòng kiểm tra lại tên file (ví dụ: `clip1_raw.wav` và `clip1_clean.wav`).")
        else:
            st.success(f"✅ Đã ghép thành công {len(pairs)} cặp file.")
            
            # Hiển thị danh sách để review
            for i, (raw, clean) in enumerate(pairs):
                with st.expander(f"Cặp #{i+1}: {raw.name}  <-->  {clean.name}", expanded=(i==0)):
                    c1, c2, c3 = st.columns([1, 1, 2])
                    
                    with c1: st.audio(raw, format="audio/wav", start_time=0)
                    with c2: st.audio(clean, format="audio/wav", start_time=0)
                    
                    with c3:
                        # Nút vẽ biểu đồ cho từng cặp
                        if st.button(f"🎨 Vẽ Sóng âm (Cặp {i+1})", key=f"plot_{i}"):
                            with st.spinner("Đang phân tích..."):
                                fig, lag = backend_core.generate_comparison_plot_from_obj(raw, clean)
                                if fig:
                                    st.pyplot(fig)
                                    st.caption(f"Độ lệch đồng bộ: {lag} mẫu")
             
            # --- NÚT LƯU TOÀN BỘ ---
            st.markdown("---")
            if st.button(f"💾 LƯU TẤT CẢ {len(pairs)} CẶP VÀO NAS", type="primary"):
                if not label_input:
                    st.error("Vui lòng nhập Tên lỗi (Label) trước khi lưu.")
                else:
                    progress_text = "Đang xử lý và lưu trữ..."
                    my_bar = st.progress(0, text=progress_text)
                    
                    success_count = 0
                    for idx, (raw, clean) in enumerate(pairs):
                        # Reset con trỏ file trước khi lưu
                        raw.seek(0)
                        clean.seek(0)
                        
                        ok, msg = backend_core.save_paired_data(
                            raw, clean, label_input, is_fake, note
                        )
                        if ok: success_count += 1
                        
                        # Update progress
                        percent = int((idx + 1) / len(pairs) * 100)
                        my_bar.progress(percent, text=f"Đang lưu cặp {idx+1}/{len(pairs)}...")
                    
                    my_bar.empty()
                    if success_count == len(pairs):
                        st.balloons()
                        st.success(f"🎉 Đã lưu thành công toàn bộ {success_count} cặp dữ liệu vào kho!")
                    else:
                        st.warning(f"Lưu xong. Thành công: {success_count}, Thất bại: {len(pairs) - success_count}")
# (Logic tương tự, tôi sẽ tóm tắt phần gọi hàm)
# --- TAB 3: HUẤN LUYỆN & KIỂM THỬ (TRAIN & BENCHMARK) ---
with tab3:
    st.header("🧠 Huấn luyện & Đánh giá Mô hình AI")
    st.caption("Quy trình khép kín: Train Model để học dữ liệu mới -> Benchmark để kiểm tra độ thông minh -> Sẵn sàng sử dụng.")

    # Chia thành 3 Sub-tabs theo thiết kế V2
    sub_tab_train, sub_tab_bench, sub_tab_auto = st.tabs([
        "🚀 1. Train Error Detection", 
        "📈 2. Benchmark Model", 
        "✨ 3. Train Auto-Correction"
    ])

    # --- SUB-TAB 1: TRAIN ERROR DETECTION ---
    with sub_tab_train:
        st.subheader("Huấn luyện Nhận diện Lỗi")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.info("""
            **Chiến lược Huấn luyện:**
            *   **Dữ liệu:** Hệ thống sẽ tự động lọc lấy các mẫu `error_*` (Lỗi) và `clean` (Đối chứng).
            *   **Mô hình:** Sử dụng Wav2Vec2 Embedding (1024-dim) + SVM Classifier.
            *   **Mục tiêu:** Phân loại chính xác các loại lỗi âm thanh.
            """)
        with c2:
            st.write("Current Model Status:")
            if os.path.exists(backend_core.MODEL_FILE):
                st.success(f"✅ Model đã sẵn sàng\n\n(`{backend_core.MODEL_FILE}`)")
                # Có thể thêm ngày tạo file nếu muốn
            else:
                st.error("❌ Chưa có Model")

        if st.button("🧠 Bắt đầu Train Model", type="primary", use_container_width=True):
            # Placeholder cho UI logging
            status_box = st.empty()
            p_bar = st.progress(0)
            log_box = st.empty()
            
            # Callback cập nhật giao diện
            def train_callback(p, msg):
                p_bar.progress(p)
                status_box.info(f"**{msg}**")
                log_box.code(msg)

            with st.spinner("Đang khởi động M2 Ultra Neural Engine..."):
                # Gọi Backend
                success, msg = backend_core.train_model_from_csv(status_callback=train_callback)
            
            if success:
                st.balloons()
                st.success(f"✅ {msg}")
                # Clear UI components
                time.sleep(2)
                status_box.empty()
                p_bar.empty()
            else:
                st.error(f"❌ Thất bại: {msg}")

    # --- SUB-TAB 2: BENCHMARK MODEL (HIỆU SUẤT) ---
    with sub_tab_bench:
        st.subheader("Đánh giá Hiệu suất (Train/Test Split 80/20)")
        
        col_b1, col_b2 = st.columns([1, 3])
        
        with col_b1:
            st.markdown("Kiểm tra xem model có thực sự 'hiểu' lỗi hay chỉ học vẹt.")
            if st.button("📊 Chạy Benchmark Ngay"):
                if not os.path.exists(backend_core.DATA_CSV):
                    st.error("Chưa có dữ liệu để test!")
                else:
                    with st.spinner("Đang chia tập dữ liệu và thi thử..."):
                        success, msg, report_data, fig = backend_core.run_benchmark_test()
                    
                    if success:
                        st.session_state['bench_success'] = True
                        st.session_state['bench_report'] = report_data
                        st.session_state['bench_fig'] = fig
                        st.success(msg)
                    else:
                        st.error(msg)
        
        # Hiển thị kết quả (Dùng session_state để không bị mất khi reload)
        if st.session_state.get('bench_success'):
            report_data = st.session_state['bench_report']
            fig = st.session_state['bench_fig']

            # 1. Metric Tổng thể
            accuracy = report_data.get('accuracy', 0)
            st.divider()
            c_metric1, c_metric2 = st.columns(2)
            with c_metric1:
                st.metric("Độ chính xác Tổng thể (Accuracy)", f"{accuracy:.1%}")
            with c_metric2:
                if accuracy >= 0.9:
                    st.success("🌟 Xuất sắc! Model rất đáng tin cậy.")
                elif accuracy >= 0.8:
                    st.info("✅ Tốt. Model hoạt động ổn định.")
                else:
                    st.warning("⚠️ Cảnh báo: Độ chính xác dưới 80%. Cần bổ sung thêm dữ liệu mẫu.")

            # 2. Bảng điểm chi tiết
            st.markdown("#### 🎯 Chi tiết từng loại lỗi")
            
            # Chuyển đổi report dict thành DataFrame để hiển thị đẹp
            # Loại bỏ các dòng tổng hợp (accuracy, macro avg, weighted avg) để bảng gọn hơn
            df_report = pd.DataFrame(report_data).transpose()
            df_display = df_report.drop(['accuracy', 'macro avg', 'weighted avg'], errors='ignore')
            
            # Format số liệu
            df_display = df_display.style.format("{:.1%}")\
                .background_gradient(cmap="Greens", subset=['precision', 'recall', 'f1-score'], vmin=0, vmax=1)
            
            st.dataframe(df_display, use_container_width=True)
            
            # 3. Confusion Matrix
            st.markdown("#### 🧩 Ma trận Nhầm lẫn (Confusion Matrix)")
            st.caption("Giúp phát hiện xem AI hay nhầm lỗi A sang lỗi B nào.")
            st.pyplot(fig)

    # --- SUB-TAB 3: TRAIN AUTO-CORRECTION (PREVIEW) ---
    with sub_tab_auto:
        st.subheader("✨ Tự động Sửa lỗi (Generative AI)")
        st.info("""
        **Tính năng Phase 2:** Huấn luyện mô hình để biến đổi âm thanh Lỗi -> Âm thanh Sạch.
        Dữ liệu đầu vào: Các cặp file Raw và Clean đã được đồng bộ.
        """)
        
        # Kiểm tra dữ liệu cặp
        if os.path.exists(backend_core.DATA_CSV):
            df = pd.read_csv(backend_core.DATA_CSV)
            # Đếm số cặp có đủ cả raw và clean
            if 'path_clean' in df.columns:
                valid_pairs = df[df['path_clean'].notna() & (df['path_clean'] != "")].shape[0]
            else:
                valid_pairs = 0
        else:
            valid_pairs = 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Tổng số cặp dữ liệu", valid_pairs)
        c2.metric("Model Gợi ý", "Pix2Pix Audio")
        c3.metric("Trạng thái", "Chưa kích hoạt", delta_color="off")

        st.markdown("#### Cấu hình Huấn luyện (Dự kiến)")
        
        col_conf1, col_conf2 = st.columns(2)
        with col_conf1:
            st.selectbox("Kiến trúc Mạng", ["U-Net (Spectrogram)", "Demucs (Waveform)", "DiffWave"])
            st.slider("Epochs", 10, 1000, 100)
        with col_conf2:
            st.number_input("Batch Size", value=4)
            st.number_input("Learning Rate", value=0.0002, format="%.5f")

        if st.button("Start Generative Training", disabled=True):
            st.write("Tính năng này sẽ được cập nhật trong phiên bản sau.")
            
        # Hiển thị một cặp mẫu để minh họa
        st.markdown("---")
        st.markdown("##### Preview Dữ liệu Cặp (Mẫu)")
        if valid_pairs > 0:
            sample_pair = df[df['path_clean'].notna()].iloc[0]
            c_a, c_b = st.columns(2)
            with c_a:
                st.write("Input (Lỗi):")
                if os.path.exists(sample_pair['path_raw']):
                    st.audio(sample_pair['path_raw'])
            with c_b:
                st.write("Target (Sạch):")
                if os.path.exists(sample_pair['path_clean']):
                    st.audio(sample_pair['path_clean'])

# --- TAB 4: QUẢN LÝ & THỐNG KÊ ---
with tab4:
    c_header, c_btn = st.columns([6, 1])
    with c_btn:
        # Nút Refresh
        if st.button("🔄 Refresh"):
            st.rerun()
    st.header("📊 Dashboard Quản lý Dữ liệu")

    # 1. Load Data
    if os.path.exists(backend_core.DATA_CSV):
        df = pd.read_csv(backend_core.DATA_CSV)
    else:
        df = pd.DataFrame(columns=["label", "is_fake", "timestamp"])

    if df.empty:
        st.warning("Kho dữ liệu trống.")
    else:
        # --- KHU VỰC THỐNG KÊ (CHARTS) ---
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        
        with col_stats1:
            total_samples = len(df)
            st.metric("Tổng số Mẫu", total_samples)
            
        with col_stats2:
            real_count = len(df[df['is_fake'] == False])
            st.metric("Mẫu Thật (Real)", real_count, delta=f"{real_count/total_samples:.1%}" if total_samples else 0)
            
        with col_stats3:
            fake_count = len(df[df['is_fake'] == True])
            st.metric("Mẫu Giả (Fake)", fake_count, delta=f"{fake_count/total_samples:.1%}" if total_samples else 0, delta_color="inverse")

        st.markdown("#### Phân bố Dữ liệu (Real vs Fake)")
        
        # Chuẩn bị dữ liệu cho biểu đồ Stacked Bar
        chart_data = df.groupby(['label', 'is_fake']).size().unstack(fill_value=0)
        chart_data.columns = ['Real', 'Fake'] if len(chart_data.columns) == 2 else chart_data.columns
        st.bar_chart(chart_data, stack=True)

        st.markdown("---")

        # --- KHU VỰC QUẢN LÝ (DATA TABLE & DELETE) ---
        st.subheader("🗂️ Quản lý File")
        
        # Bộ lọc
        c_filter1, c_filter2 = st.columns(2)
        with c_filter1:
            filter_label = st.multiselect("Lọc theo Nhãn", df['label'].unique())
        with c_filter2:
            filter_type = st.radio("Lọc theo Loại", ["Tất cả", "Real Only", "Fake Only"], horizontal=True)

        # Apply filter
        df_show = df.copy()
        if filter_label:
            df_show = df_show[df_show['label'].isin(filter_label)]
        if filter_type == "Real Only":
            df_show = df_show[df_show['is_fake'] == False]
        elif filter_type == "Fake Only":
            df_show = df_show[df_show['is_fake'] == True]

        st.dataframe(df_show, use_container_width=True)

        # --- CHỨC NĂNG XÓA (DANGEROUS ZONE) ---
        with st.expander("🗑️ Khu vực Nguy hiểm (Xóa Dữ liệu)", expanded=False):
            st.warning("Hành động này không thể hoàn tác! Nó sẽ xóa file vật lý và dòng trong CSV.")
            
            c_del1, c_del2 = st.columns(2)
            
            # Xóa theo bộ lọc hiện tại
            with c_del1:
                st.markdown(f"Xóa **{len(df_show)}** mẫu đang hiển thị ở trên?")
                if st.button("Xóa theo Bộ lọc", type="primary"):
                    if len(df_show) == len(df):
                        st.error("Không cho phép xóa toàn bộ DB bằng nút này. Hãy dùng nút Reset bên cạnh.")
                    else:
                        # Gọi hàm xóa backend (Cần viết thêm)
                        deleted_count = backend_core.delete_data(df_show)
                        st.success(f"Đã xóa {deleted_count} mẫu.")
                        time.sleep(1)
                        st.rerun()

            # Xóa toàn bộ Fake
            with c_del2:
                st.markdown("Xóa toàn bộ **Dữ liệu Giả (Fake)** để sinh lại?")
                if st.button("Xóa TẤT CẢ Fake Data"):
                    fake_df = df[df['is_fake'] == True]
                    deleted_count = backend_core.delete_data(fake_df)
                    st.success(f"Đã dọn sạch {deleted_count} mẫu Fake.")
                    time.sleep(1)
                    st.rerun()

# --- TAB 5: DATA FACTORY (NHÀ MÁY DỮ LIỆU) ---
with tab5:
    st.header("🏭 Data Factory - Sản xuất Dữ liệu Giả lập")
    
    # Chia thành 3 quy trình rõ ràng
    t5_mining, t5_lab, t5_mass = st.tabs([
        "⛏️ 1. Khai thác Nền (Mining)", 
        "🧪 2. Thí nghiệm (Preview)", 
        "🏭 3. Sản xuất Hàng loạt (Mass Production)"
    ])

    # ==========================================================================
    # SUB-TAB 5.1: BACKGROUND MINING (Giữ nguyên logic cũ)
    # ==========================================================================
    with t5_mining:
        st.subheader("Khai thác Nền từ Video dài")
        bg_video_path = st.text_input("Đường dẫn Video Nền", placeholder="/path/to/video.mp4")
        
        c1, c2 = st.columns(2)
        with c1:
            bg_clip_len = st.slider("Độ dài mẫu (s)", 0.5, 5.0, 1.0)
            bg_quality_mode = st.selectbox("Chế độ lọc", ["quiet", "speech"])
        with c2:
            bg_max_samples = st.number_input("Số lượng mẫu tối đa", value=50)
            
        if st.button("⛏️ Bắt đầu Khai thác"):
            if bg_video_path:
                with st.status("Đang khai thác...", expanded=True) as status:
                    saved, msg = data_factory.extract_background_samples(
                        bg_video_path, bg_clip_len, bg_max_samples, bg_quality_mode
                    )
                    if saved:
                        status.update(label="Thành công!", state="complete")
                        st.success(f"{msg} ({len(saved)} files)")
                    else:
                        st.error(msg)
            else:
                st.error("Chưa nhập đường dẫn.")
    # Hiển thị số lượng hiện có
    num_bg = len([f for f in os.listdir(data_factory.BG_BANK_FOLDER) if f.endswith('.wav')]) if os.path.exists(data_factory.BG_BANK_FOLDER) else 0
    st.metric("Tổng mẫu nền trong kho", num_bg)
    # ==========================================================================
    # SUB-TAB 5.2: LAB PREVIEW (Code cũ chuyển vào đây)
    # ==========================================================================
    with t5_lab:
        st.subheader("Phòng Thí nghiệm (Sinh thử 1 mẫu)")
        
    # ==========================================================================
    # KHU VỰC 2: SYNTHESIS ENGINE (CẤY LỖI)
    # ==========================================================================
        st.subheader("2. Cấy Lỗi (Synthesis Engine)")
        st.info("Trộn mẫu Lỗi (Diff) vào mẫu Nền (Background) bằng thuật toán.")
        
        # --- BƯỚC A: CHỌN NGUYÊN LIỆU ---
        st.markdown("#### A. Chọn Mẫu Lỗi (Diff Source)")
        
        # Load danh sách label từ CSV (Chỉ lấy label có file Diff)
        available_labels = []
        if os.path.exists(backend_core.DATA_CSV):
            df = pd.read_csv(backend_core.DATA_CSV)
            # Giả định có cột 'path_diff' và file đó tồn tại
            if 'path_diff' in df.columns:
                valid_df = df[df['path_diff'].notna() & df['label'].str.contains('error')]
                available_labels = valid_df['label'].unique()
        
        if len(available_labels) == 0:
            st.warning("⚠️ Chưa có mẫu lỗi nào có file Diff. Hãy sang Tab 2 để thu thập dữ liệu cặp (Raw/Clean) trước.")
            selected_label = None
        else:
            c_label, c_file = st.columns([1, 1.5])
            with c_label:
                selected_label = st.selectbox("Chọn Loại Lỗi:", available_labels)
            
            # Lấy danh sách file diff của label này
            diff_files = []
            if selected_label:
                diff_files = [f for f in os.listdir(data_factory.DIFF_BANK_FOLDER) if selected_label in f]
            
            with c_file:
                selected_diff_name = st.selectbox("Chọn Mẫu Diff:", diff_files if diff_files else ["Không có file"])
        
        diff_file_path = None
        if selected_diff_name and selected_diff_name != "Không có file":
            diff_file_path = os.path.join(data_factory.DIFF_BANK_FOLDER, selected_diff_name)
            st.audio(diff_file_path) # Nghe thử Diff

        # --- BƯỚC B: CẤU HÌNH THUẬT TOÁN ---
        st.markdown("#### B. Cấu hình Cấy ghép")
        
        c_algo, c_snr = st.columns(2)
        with c_algo:
            algo_type = st.selectbox(
                "Thuật toán", 
                ["Mix", "Time Stretch", "Frequency Shift", "Feature Grafting", "Shuffle"],
                help="Mix: Cộng thường. Grafting: Trộn quang phổ (tự nhiên hơn). Shuffle: Ngẫu nhiên."
            )
        with c_snr:
            snr_val = st.slider("Độ to của Lỗi (SNR dB)", -30.65, 10.0, 0.0, help=">0: Lỗi to hơn nền. <0: Lỗi nhỏ hơn nền.")

        # --- BƯỚC C: SINH & LƯU ---
        st.markdown("#### C. Thực thi")
        
        if st.button("🧪 Sinh thử 1 Mẫu (Preview)", type="primary", use_container_width=True):
            if not diff_file_path:
                st.error("Chưa chọn mẫu Diff.")
            elif num_bg == 0:
                st.error("Kho Background trống! Hãy khai thác nền trước.")
            else:
                # Lấy ngẫu nhiên 1 background
                bg_files = [os.path.join(data_factory.BG_BANK_FOLDER, f) for f in os.listdir(data_factory.BG_BANK_FOLDER) if f.endswith('.wav')]
                random_bg = random.choice(bg_files)
                
                with st.spinner("Đang tổng hợp..."):
                    # Gọi hàm sinh từ Backend
                    mixed_audio, bg_audio, sr = data_factory.synthesize_sample(random_bg, diff_file_path, algo_type, snr_val)
                
                if mixed_audio is not None:
                    # Lưu tạm để nghe
                    temp_synth = "temp_synth_preview.wav"
                    temp_clean_ref = "temp_synth_clean.wav"

                    import soundfile as sf
                    sf.write(temp_synth, mixed_audio, sr)
                    sf.write(temp_clean_ref, bg_audio, sr)
                    
                    st.success("✅ Sinh thành công!")
                    
                    # Hiển thị kết quả so sánh
                    c_preview1, c_preview2 = st.columns(2)
                    with c_preview1:
                        st.write("**Gốc (Nền):**")
                        st.audio(random_bg)
                    with c_preview2:
                        st.write("**Kết quả (Fake):**")
                        st.audio(temp_synth)
                    
                    # Nút Lưu (Nested Button - Streamlit trick: dùng session state để nhớ trạng thái sinh)
                    st.session_state['last_synth_fake'] = temp_synth
                    st.session_state['last_synth_clean'] = temp_clean_ref
                    st.session_state['last_synth_label'] = selected_label
                else:
                    st.error("Lỗi thuật toán sinh mẫu.")

        # Nút Lưu riêng biệt (để tránh reload mất file)
        if 'last_synth_fake' in st.session_state and os.path.exists(st.session_state['last_synth_fake']):
            if st.button("💾 Lưu cặp mẫu này vào Kho (Training Data)"):
                with open(st.session_state['last_synth_fake'], "rb") as f_fake, \
                     open(st.session_state['last_synth_clean'], "rb") as f_clean:
                # with open(st.session_state['last_synth_fake'], "rb") as f:
                    # Lưu với cờ is_fake=True
                    f_fake.name = f"fake_{algo_type}.wav"
                    f_clean.name = f"clean_bg_ref.wav"
                    success, msg = backend_core.save_paired_data(
                        raw_file=f_fake,    # Fake đóng vai trò là Raw (Lỗi)
                        clean_file=f_clean, # Background đóng vai trò là Clean
                        label=st.session_state['last_synth_label'],
                        is_fake=True,       # Đánh dấu là Fake
                        note=f"Generated by Data Factory (Algo: {algo_type}, SNR: {snr_val})"
                    )
                st.toast("Đã lưu vào CSV!", icon="✅")
                # Xóa state
                del st.session_state['last_synth_fake']
                del st.session_state['last_synth_clean']
                st.rerun() # Refresh lại trang

    # ==========================================================================
    # SUB-TAB 5.3: MASS PRODUCTION (CHỨC NĂNG MỚI)
    # ==========================================================================
    with t5_mass:
        st.subheader("Dây chuyền Sản xuất (Batch Synthesis)")
        st.info("Tự động lấy TẤT CẢ mẫu Real Diff của một nhãn và trộn với kho Background để tạo ra hàng nghìn mẫu Fake.")
        
        # 1. Cấu hình Đầu vào
        col_mass1, col_mass2 = st.columns(2)
        with col_mass1:
            # Load labels
            if os.path.exists(backend_core.DATA_CSV):
                df = pd.read_csv(backend_core.DATA_CSV)
                # Chỉ lấy label có dữ liệu Real (is_fake = False)
                real_df = df[df['is_fake'] == False]
                labels = real_df['label'].unique()
            else:
                labels = []
            
            target_label = st.selectbox("Chọn Loại Lỗi cần nhân bản:", labels if len(labels)>0 else ["Chưa có dữ liệu Real"])
            
            # Đếm số lượng mẫu Diff gốc
            if len(labels) > 0:
                num_diff_source = len(real_df[real_df['label'] == target_label])
                st.caption(f"Tìm thấy **{num_diff_source}** mẫu Diff gốc (Real) cho nhãn này.")

        with col_mass2:
            # Cấu hình số lượng
            num_bg_mix = st.number_input("Số lượng Background ghép với mỗi Diff", min_value=1, value=10, help="1 Diff sẽ được trộn với bao nhiêu nền khác nhau?")
            total_estimate = num_diff_source * num_bg_mix if len(labels) > 0 else 0
            st.metric("Tổng số mẫu Fake sẽ tạo ra", total_estimate)

        # 2. Cấu hình Thuật toán (Áp dụng chung)
        with st.expander("⚙️ Cấu hình Thuật toán & Biến đổi", expanded=False):
            c1, c2 = st.columns(2)

            with c1:
                mass_algo = st.multiselect("Các thuật toán được phép dùng (Random)", 
                                        ["Mix", "Time Stretch", "Frequency Shift", "Feature Grafting"],
                                        default=["Mix", "Time Stretch"])
                mass_snr_range = st.slider("Khoảng biến thiên SNR (dB)", -10.0, 10.0, (-5.0, 5.0))
            with c2:
                # --- THÊM PHẦN NÀY ---
                mass_snr_range = st.slider(
                    "Độ to của Lỗi (SNR Range dB)", 
                    min_value=-50, max_value=10, 
                    value=(-30, -25), # Mặc định random từ -5 đến 5dB
                    help="Chọn khoảng biến thiên độ to của lỗi so với nền. \n-10dB: Lỗi nhỏ hơn nền. 10dB: Lỗi to hơn nền."
                )
        
        # 3. Thực thi
        if st.button("🏭 BẮT ĐẦU SẢN XUẤT HÀNG LOẠT", type="primary", disabled=(total_estimate==0)):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Gọi hàm backend mới (cần viết thêm)
            success_count = 0
            
            # Lấy danh sách file diff
            diff_sources = real_df[real_df['label'] == target_label]['path_diff'].tolist()
            # Lấy danh sách file background
            bg_files = [os.path.join(data_factory.BG_BANK_FOLDER, f) for f in os.listdir(data_factory.BG_BANK_FOLDER) if f.endswith('.wav')]
            
            if not bg_files:
                st.error("Kho Background trống!")
            else:
                for i, diff_path in enumerate(diff_sources):
                    # Với mỗi mẫu Diff
                    for j in range(num_bg_mix):
                        # Random Background & Algo
                        bg_path = random.choice(bg_files)
                        algo = random.choice(mass_algo)
                        snr = random.uniform(mass_snr_range[0], mass_snr_range[1])
                        
                        # Sinh mẫu
                        mixed_audio, bg_audio, sr = data_factory.synthesize_sample(bg_path, diff_path, algo, snr)
                        
                        if mixed_audio is not None:
                            # Lưu file Fake & Clean (BG)
                            # Logic lưu file nhanh
                            # ... (Gọi hàm save_batch_sample bên dưới) ...
                            backend_core.save_batch_generated_sample(
                                mixed_audio, bg_audio, sr, 
                                target_label, diff_path, # Truyền diff path gốc
                                f"Mass Gen: {algo}, SNR {snr:.1f}"
                            )
                            success_count += 1
                    
                    # Update progress
                    progress_bar.progress((i + 1) / len(diff_sources))
                    status_text.text(f"Đang xử lý mẫu gốc {i+1}/{len(diff_sources)}...")
                
                st.success(f"🎉 Hoàn tất! Đã sinh và lưu {success_count} mẫu mới vào kho.")
# Footer
st.markdown("---")
st.caption("IA MEDIA Project - Developed for Zen Master Thich Nhat Hanh's Dharma Talks Restoration.")

