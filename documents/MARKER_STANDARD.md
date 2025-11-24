# QUY CHUẨN MARKER LỖI (IA MEDIA MARKER STANDARD)

Tài liệu này quy định cách hiển thị các lỗi phát hiện bởi AI trong phần mềm Final Cut Pro.

## 1. Định dạng Marker
Chúng ta sử dụng loại **To-Do Marker** (Marker việc cần làm).
*   **Trạng thái mặc định:** `Incomplete` (Màu Đỏ trong FCP).
*   **Khi editor sửa xong:** Click vào marker để chuyển sang `Completed` (Màu Xanh lá).

## 2. Cấu trúc Tên (Marker Name)
Tên marker hiển thị trên timeline phải tuân thủ format:
`[LOẠI_LỖI] Tên_Chi_Tiết`

| Mã Loại | Ý nghĩa | Màu sắc gợi ý (Nếu dùng Chapter Marker) | Ví dụ |
| :--- | :--- | :--- | :--- |
| **[PRON]** | Lỗi Phát âm (Pronunciation) - Sai âm đuôi, nuốt âm | Tím (Purple) | `[PRON] Lỗi đuôi /t/` |
| **[VOL]** | Lỗi Âm lượng (Volume) - Quá nhỏ, vỡ tiếng | Vàng (Yellow) | `[VOL] Nhỏ (< -20dB)` |
| **[NOISE]** | Tiếng ồn (Noise) - Ho, gõ bàn, tiếng bút | Đỏ (Red) | `[NOISE] Tiếng Ho/Rè` |
| **[PACE]** | Nhịp điệu (Pacing) - Khoảng lặng, từ đệm | Xanh (Cyan) | `[PACE] Lặp từ "và và"` |

## 3. Nội dung Ghi chú (Notes)
Trong phần Note của marker phải chứa thông tin giải thích:
*   **Độ tin cậy (Confidence):** AI chắc chắn bao nhiêu %.
*   **Gợi ý (Suggestion):** (Phase 2 sẽ điền cái này).
*   **Dữ liệu kỹ thuật:** Ví dụ RMS level, khoảng cách vector.

**Ví dụ hiển thị trong FCP:**
> **Name:** `[PRON] Lỗi đuôi /t/ - 'bát'`
> **Note:** Phát âm giống 'bash'. Độ tin cậy: 89%. Gợi ý: Kiểm tra file gốc hoặc dùng bản vá từ 00:12:00.