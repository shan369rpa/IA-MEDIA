# scripts/visualize_spectrogram.py

import argparse
import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

def create_mel_spectrogram(audio_path, n_mels=128, fmax=8000):
    """
    Chuyển đổi Audio thành ma trận Mel-Spectrogram (dB).
    
    Args:
        audio_path: Đường dẫn file audio.
        n_mels: Số lượng dải tần số (chiều cao của ảnh). 128 là chuẩn cho các model AI.
        fmax: Tần số tối đa hiển thị (8000Hz là đủ cho giọng nói).
    
    Returns:
        S_dB: Ma trận năng lượng (dB).
        sr: Tần số mẫu.
    """
    # 1. Tải audio
    # sr=None để giữ nguyên tần số gốc (thường là 44.1k hoặc 48k), 
    # nhưng để phân tích giọng nói ta thường dùng 16k hoặc 22k.
    y, sr = librosa.load(audio_path, sr=None)

    # 2. Tính toán Mel Spectrogram
    # n_fft: Độ dài cửa sổ phân tích. hop_length: Bước nhảy.
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, fmax=fmax)

    # 3. Chuyển đổi sang thang đo Decibel (Log scale)
    # Vì tai người nghe theo log, và để làm nổi bật các tín hiệu nhỏ.
    S_dB = librosa.power_to_db(S, ref=np.max)
    
    return S_dB, sr

def plot_single(audio_path, output_path=None):
    """Vẽ 1 biểu đồ duy nhất."""
    S_dB, sr = create_mel_spectrogram(audio_path)

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', fmax=8000)
    plt.colorbar(format='%+2.0f dB')
    plt.title(f'Mel-Spectrogram: {os.path.basename(audio_path)}')
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
        print(f"✅ Đã lưu ảnh tại: {output_path}")
    else:
        plt.show()

def plot_comparison(clean_path, error_path, output_path=None):
    """
    Vẽ so sánh Clean vs Error và sự khác biệt.
    Đây là công cụ mạnh nhất để nhìn thấy lỗi.
    """
    # Tính toán
    S_clean, sr = create_mel_spectrogram(clean_path)
    S_error, _ = create_mel_spectrogram(error_path)

    # Đảm bảo 2 ma trận cùng kích thước (cắt bớt phần thừa nếu lệch vài ms)
    min_len = min(S_clean.shape[1], S_error.shape[1])
    S_clean = S_clean[:, :min_len]
    S_error = S_error[:, :min_len]

    # Tính ma trận khác biệt (Absolute Difference)
    # Chỗ nào màu càng sáng thì sự khác biệt càng lớn (chính là Lỗi)
    S_diff = np.abs(S_error - S_clean)

    # Vẽ biểu đồ (3 hàng)
    fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(10, 10))

    # 1. Clean
    img1 = librosa.display.specshow(S_clean, sr=sr, x_axis='time', y_axis='mel', fmax=8000, ax=ax[0])
    ax[0].set_title(f'Clean (Edited): {os.path.basename(clean_path)}')
    fig.colorbar(img1, ax=ax[0], format='%+2.0f dB')

    # 2. Error (Raw)
    img2 = librosa.display.specshow(S_error, sr=sr, x_axis='time', y_axis='mel', fmax=8000, ax=ax[1])
    ax[1].set_title(f'Raw (Error): {os.path.basename(error_path)}')
    fig.colorbar(img2, ax=ax[1], format='%+2.0f dB')

    # 3. Difference (Lỗi nằm ở đâu?)
    img3 = librosa.display.specshow(S_diff, sr=sr, x_axis='time', y_axis='mel', fmax=8000, ax=ax[2], cmap='magma')
    ax[2].set_title('Difference (Sự khác biệt = Lỗi)')
    fig.colorbar(img3, ax=ax[2], format='%+2.0f dB')

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path)
        print(f"✅ Đã lưu ảnh so sánh tại: {output_path}")
    else:
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tạo ảnh Mel-Spectrogram từ audio.")
    parser.add_argument("input_path", type=str, help="Đường dẫn file audio (hoặc file Raw trong chế độ so sánh).")
    parser.add_argument("--compare", type=str, help="Đường dẫn file Clean để so sánh.", default=None)
    parser.add_argument("-o", "--output", type=str, help="Đường dẫn lưu file ảnh (nếu không có sẽ hiển thị cửa sổ).", default=None)

    args = parser.parse_args()

    if args.compare:
        print(f"Đang so sánh:\n 1. {args.compare}\n 2. {args.input_path}")
        plot_comparison(args.compare, args.input_path, args.output)
    else:
        print(f"Đang vẽ: {args.input_path}")
        plot_single(args.input_path, args.output)