# IA MEDIA: Khung Lý thuyết & Hướng dẫn Vận hành
**(Theoretical Framework & Operational Guide)**

---

## **PHẦN 1: CƠ SỞ LÝ THUYẾT (THEORETICAL BASIS)**

### **1. Bài toán Tổng quát**
Chúng ta sở hữu một "Kho báu Dữ liệu" (Golden Dataset) gồm **700 bài pháp thoại** đã được chỉnh sửa hoàn thiện bởi con người. Mục tiêu là tận dụng tri thức ẩn chứa trong 700 bài này để tự động hóa quy trình xử lý cho **300 bài còn lại**.

### **2. Nguyên lý: Phân tích Chênh lệch (Differential Analysis)**

Hầu hết các hệ thống AI học từ dữ liệu tĩnh. Hệ thống của chúng ta khác biệt ở chỗ nó học từ **sự thay đổi**.

Ta định nghĩa:
*   **Video Raw ($V_{raw}$):** Chứa "Tín hiệu Sạch" ($S$) + "Nhiễu/Lỗi" ($N$).
*   **Video Edited ($V_{edited}$):** Chỉ chứa "Tín hiệu Sạch" ($S$).
*   **FCPXML ($Map$):** Bản đồ ánh xạ thời gian giữa $V_{raw}$ và $V_{edited}$.

Thông qua FCPXML, ta có thể đồng bộ hóa và thực hiện phép trừ logic:
$$N (Lỗi) \approx V_{raw} - V_{edited}$$

Hệ thống không học "thế nào là hay", mà nó học **"Editor đã vứt bỏ cái gì và giữ lại cái gì"**.

### **3. Các Kỹ thuật Chunking Đa tầng (Multi-layered Chunking)**

Để AI hiểu được, chúng ta không thể đưa cả video 1 tiếng vào. Chúng ta phải chia nhỏ (chunk) nó ra theo các tầng ý nghĩa khác nhau. Chúng ta áp dụng 3 tầng chunking:

#### **Tầng 0: Kỹ thuật Cửa sổ Trượt (Sliding Window / Slice-Level)**
*   **Đơn vị:** Các lát cắt siêu nhỏ (Slices) chồng lên nhau bên trong một từ.
*   **Mục đích:** "Soi" kỹ vào cấu trúc bên trong của một âm thanh để tìm các lỗi kỹ thuật cực nhanh (tiếng click, tiếng bật hơi mic - pop).
*   **Minh họa:**
    Giả sử từ "Pháp" dài 500ms.
    *   *Cửa sổ 1:* 0ms - 100ms (Âm "Ph")
    *   *Cửa sổ 2:* 20ms - 120ms (Phần tiếp theo...)
    *   ... Trượt liên tục cho đến hết từ.
*   **Ứng dụng:**
    *   Phát hiện lỗi ở mức mili-giây mà tai thường khó nghe thấy.
    *   Phát hiện sự biến đổi bất thường của âm đuôi (ví dụ: âm /t/ bị bật quá mạnh).

#### **Tầng 1: Micro-Chunking (Cấp độ Từ - Word Level)**
*   **Mục tiêu:** Phát hiện lỗi phát âm (âm đuôi, âm gió, giọng địa phương), nói lắp.
*   **Kỹ thuật:** Sử dụng ASR (Whisper) để lấy timestamp từng từ.
*   **Cơ chế:** Với mỗi từ (ví dụ: "bát"), ta cắt ra 2 phiên bản:
    *   `Sample_Clean`: Từ "bát" trong video đã sửa.
    *   `Sample_Error`: Từ "bát" trong video gốc (có thể bị dính tiếng tặc lưỡi hoặc âm đuôi bị bật mạnh).
*   **Ứng dụng Vector:** Ta biến cả 2 mẫu này thành vector. Khoảng cách giữa vector `Clean` và `Error` chính là "độ lỗi".

#### **Tầng 2: Semantic Chunking (Cấp độ Câu - Sentence Level)**
*   **Mục tiêu:** Phát hiện lỗi về nhịp điệu (pacing), ngắt nghỉ sai, ngữ điệu bất thường, hoặc khoảng lặng quá dài (Long Silence).
*   **Kỹ thuật:** Dựa trên dấu câu hoặc khoảng lặng > 500ms.
*   **Cơ chế:** Phân tích ngữ cảnh rộng hơn. Một từ có thể phát âm đúng, nhưng nếu nó nằm trong một câu bị ngắt quãng vô lý, thì cả câu đó là lỗi.

#### **Tầng 3: Event Chunking (Cấp độ Sự kiện - Event Level)**
*   **Mục tiêu:** Phát hiện các tạp âm môi trường không phải tiếng người.
*   **Kỹ thuật:** Sử dụng mô hình phân loại âm thanh (Audio Event Detection) để quét toàn bộ file raw.
*   **Cơ chế:** Tự động khoanh vùng các đoạn có tiếng: *Ho, Cười, Viết bảng, Tiếng chuông, Va chạm Micro*.

---

### **4. Chiến lược Áp dụng (Strategy: From 700 to 300)**

Quá trình được chia làm 2 giai đoạn rõ ràng:

#### **Giai đoạn A: Học hỏi (Training / Database Building) - Áp dụng cho 700 bài**
Chúng ta "khai thác" 700 bài đã sửa để xây dựng một **Cơ sở dữ liệu Vector (Knowledge Base)**.
*   CSDL này chứa hàng triệu cặp mẫu: "Đây là cách Thầy phát âm từ 'Chánh niệm' chuẩn" vs "Đây là cách phát âm bị lỗi (do mic/môi trường)".
*   Kết quả: Một "bản đồ" khổng lồ về các lỗi thường gặp.

#### **Giai đoạn B: Suy luận (Inference / Fixing) - Áp dụng cho 300 bài**
Khi có một video mới trong nhóm 300 bài chưa sửa:
1.  Hệ thống cắt video đó ra thành các chunk (Từ/Câu/Sự kiện).
2.  Nó biến các chunk đó thành vector.
3.  Nó mang vector đó đi hỏi CSDL (Giai đoạn A): *"Đoạn âm thanh này giống với nhóm 'Sạch' hay nhóm 'Lỗi' mà mày đã biết?"*
4.  Nếu giống nhóm 'Lỗi', hệ thống đánh dấu: **"Khả năng cao đoạn này cần sửa"**.

---

## **PHẦN 2: HƯỚNG DẪN CUNG CẤP DỮ LIỆU (DATA PROVISIONING)**

Để hệ thống hoạt động, dữ liệu đầu vào phải tuân thủ nghiêm ngặt các quy tắc sau.

### **1. Cấu trúc Thư mục (Trên Google Drive)**
Media Team cần upload dữ liệu vào thư mục được chia sẻ theo cấu trúc:

```text
IA_MEDIA_PROJECT/
└── source_data/
    ├── Batch_01/  <-- Tên Lô (Ví dụ: 10 video đầu tiên)
    │   ├── 2010-06-15-blue-cliff-raw.mp4
    │   ├── 2010-06-15-blue-cliff-edited.mp4
    │   └── 2010-06-15-blue-cliff.fcpxml
    ├── Batch_02/
    └── ...
```

### **2. Quy tắc Đặt tên (Naming Convention)**
BẮT BUỘC phải có 3 file cho mỗi bài pháp thoại (Session). Tên file phải khớp nhau phần đầu (Session ID).

*   **File Gốc (Raw):** `{tên-bài}_raw.mp4`
*   **File Đã Sửa (Edited):** `{tên-bài}_edited.mp4`
*   **File Project (XML):** `{tên-bài}.fcpxml`

*Ví dụ đúng:* `phap-thoai-01_raw.mp4`, `phap-thoai-01_edited.mp4`, `phap-thoai-01.fcpxml`.

### **3. Yêu cầu về File FCPXML**
*   File XML phải được xuất từ chính Project đã dùng để edit video đó.
*   Trong timeline của FCP, clip gốc (raw) không được bị đổi tên (rename) khác với tên file vật lý trên đĩa, để hệ thống có thể nhận diện.