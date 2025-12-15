# Hướng dẫn Sử dụng Báo cáo Lỗi Tự động từ AI (Phiên bản Demo)

Chào đội ngũ Media,

Chúng tôi đã hoàn thành phiên bản demo đầu tiên của công cụ AI có tên **IA MEDIA**, được thiết kế để hỗ trợ và tăng tốc quá trình chỉnh sửa âm thanh của mọi người.

Công cụ này sẽ tự động "nghe" trước các video thô và đánh dấu những vị trí có khả năng chứa lỗi âm thanh. Mục tiêu là giúp các bạn tiết kiệm thời gian dò tìm và có thể đi thẳng vào các điểm cần xử lý.

Dưới đây là hướng dẫn từng bước để sử dụng file báo cáo.

---

### **Yêu cầu:**
1.  File video `raw` (ví dụ: `2004.09.19..._raw.mp4`).
2.  File báo cáo lỗi `.fcpxml` tương ứng (ví dụ: `error_report.fcpxml`).

### **Bước 1: Mở Final Cut Pro và Tạo Library Mới**

Để tránh ảnh hưởng đến các dự án hiện tại, chúng ta sẽ làm việc trên một Library mới cho lần thử nghiệm này.
-   Mở Final Cut Pro.
-   Vào `File > New > Library...` và đặt tên, ví dụ `IA_MEDIA_Test`.

### **Bước 2: Import file Video `raw`**

-   Trong Library mới, vào `File > Import > Media...` (hoặc `Cmd + I`).
-   Tìm và chọn file video `raw` mà chúng tôi đã gửi.
-   Đảm bảo tùy chọn **"Leave files in place"** được chọn để tiết kiệm dung lượng.
-   Nhấn `Import`.

### **Bước 3: Import file Báo cáo Lỗi `.fcpxml` (Bước quan trọng nhất)**

-   Bây giờ, vào `File > Import > XML...`.
-   Tìm và chọn file `.fcpxml` mà chúng tôi đã gửi.
-   Một cửa sổ Import XML sẽ hiện ra. **Hãy giữ nguyên các tùy chọn mặc định** và nhấn `Import`.

### **Bước 4: Xem và Xử lý các "To-Do Marker"**

-   **Kết quả:** Sau khi import, một **Project mới** sẽ tự động xuất hiện trong Event của bạn. Hãy mở Project đó lên.
-   **Trên Timeline:** Bạn sẽ thấy clip video `raw` của mình. Đặc biệt, trên clip sẽ xuất hiện các **marker màu đỏ**. Đây chính là các "ghi chú công việc" (To-Do Markers) mà AI đã tạo ra.
-   **Mở Timeline Index:**
    -   Nhấn phím tắt `Cmd + Shift + 2` để mở bảng **Timeline Index**.
    -   Chuyển sang tab **"Tags"**.
    -   Bạn sẽ thấy một danh sách tất cả các marker To-Do. Đây là danh sách đầy đủ các lỗi tiềm năng mà AI đã tìm thấy.
-   **Cách làm việc:**
    1.  **Nhấp vào một marker** trong danh sách Tags, con trỏ timeline sẽ tự động **nhảy đến chính xác** vị trí lỗi đó.
    2.  **Đọc ghi chú của marker:** Di chuột qua marker trên timeline, bạn sẽ thấy ghi chú của AI, ví dụ: `[AI-SPIKE] Vấn đề tiềm ẩn tại từ: 'tư'`.
        -   `[AI-SPIKE]`: Gợi ý loại lỗi (Noise Spike - Nhiễu đột ngột).
        -   `[AI-VOLUME]`: Gợi ý lỗi Âm lượng.
        -   `[AI-AUDIO]`: Lỗi âm thanh chung (có thể là phát âm).
    3.  **Xác minh và Sửa lỗi:** Nghe đoạn âm thanh đó và quyết định xem có cần sửa không.
    4.  **Đánh dấu Hoàn thành:** Sau khi sửa xong, bạn có thể **nhấp vào vòng tròn màu đỏ** của marker trong bảng Timeline Index. Nó sẽ chuyển thành **dấu tick màu xanh**. Đây là cách để chúng ta biết bạn đã xử lý xong điểm đó.

---

Chúng tôi rất mong nhận được phản hồi của các bạn về tính hữu ích và độ chính xác của các gợi ý này. Cảm ơn sự hợp tác của mọi người!