import os
import ffmpeg
import numpy as np
import soundfile as sf
from pedalboard import load_plugin
from pedalboard.io import AudioFile

# --- CẤU HÌNH ĐƯỜNG DẪN ---
# Đường dẫn đến file VST3 của iZotope trên macOS
RX_DECLICK_PATH = "/Library/Audio/Plug-Ins/VST3/RX 11 De-click.vst3"

def process_video_audio(input_video, output_video, plugin_path):
    print(f"🔄 Đang xử lý: {input_video}")
    
    # BƯỚC 1: TÁCH AUDIO TỪ VIDEO (DEMUX)
    # Xuất ra file wav tạm thời để xử lý
    temp_audio_in = "temp_input.wav"
    temp_audio_out = "temp_processed.wav"
    
    try:
        (
            ffmpeg
            .input(input_video)
            .output(temp_audio_in, acodec='pcm_s24le', ar='48000', loglevel='error')
            .overwrite_output()
            .run()
        )
    except ffmpeg.Error as e:
        print("❌ Lỗi FFmpeg tách âm thanh")
        return

    # BƯỚC 2: APPLY PLUGIN RX (DÙNG PEDALBOARD)
    print("🎛 Đang chạy RX De-click...")
    
    try:
        # Load Plugin VST3
        plugin = load_plugin(plugin_path)
        
        # Cài đặt thông số cho Plugin (Đây là phần khó nhất - xem giải thích bên dưới)
        # Bạn phải biết tên tham số nội bộ của plugin. Ví dụ giả định:
        # plugin.sensitivity = 0.5 
        plugin.algorithm = 'Single-band'
        # plugin.algorithm = 'multi_band_random' 
        plugin.click_widening = '1,00'
        plugin.sensitivity = '4,00'
        # Đọc file audio
        with AudioFile(temp_audio_in) as f:
            audio = f.read(f.frames)
            samplerate = f.samplerate
            
        # Chạy hiệu ứng (Process)
        processed_audio = plugin(audio, samplerate)
        
        # Lưu file audio đã sửa
        with sf.SoundFile(temp_audio_out, 'w', samplerate, len(processed_audio.shape)) as f:
            f.write(processed_audio.T) # Pedalboard dùng (channels, samples), Soundfile cần transpose
            
    except Exception as e:
        print(f"❌ Lỗi xử lý VST: {e}")
        # Dọn dẹp file tạm trước khi thoát
        if os.path.exists(temp_audio_in): os.remove(temp_audio_in)
        return

    # BƯỚC 3: GHÉP AUDIO MỚI VÀO VIDEO GỐC (REMUX)
    # Quan trọng: Dùng vcodec='copy' để KHÔNG render lại hình ảnh (Giữ nguyên chất lượng 100%)
    print("🎬 Đang xuất video...")
    
    video_stream = ffmpeg.input(input_video).video # Lấy luồng hình gốc
    audio_stream = ffmpeg.input(temp_audio_out)    # Lấy luồng tiếng mới
    
    try:
        (
            ffmpeg
            .output(video_stream, audio_stream, output_video, vcodec='copy', acodec='aac', audio_bitrate='320k')
            .overwrite_output()
            .run()
        )
        print(f"✅ Hoàn tất! File lưu tại: {output_video}")
        
    except ffmpeg.Error as e:
        print("❌ Lỗi FFmpeg ghép file")
    
    # Dọn dẹp file tạm
    if os.path.exists(temp_audio_in): os.remove(temp_audio_in)
    if os.path.exists(temp_audio_out): os.remove(temp_audio_out)

# --- CHẠY THỬ ---
if __name__ == "__main__":
    # Thay đổi tên file của bạn ở đây
    # INPUT_FILE = "input_video.mp4" 
    # OUTPUT_FILE = "output_video_fixed.mp4"
    INPUT_FILE = "/Users/sonpc/Downloads/Mẫu/audio lỗi nặng/2007.12.11.PK.VN.HySinhChuyenRiengTuViDaiNghia.PAL.mp4"
    OUTPUT_FILE = "/Users/sonpc/Downloads/Mẫu/audio lỗi nặng/out_2007.12.11.PK.VN.HySinhChuyenRiengTuViDaiNghia.PAL.mp4"
    # Kiểm tra xem plugin có tồn tại không
    if os.path.exists(RX_DECLICK_PATH):
        process_video_audio(INPUT_FILE, OUTPUT_FILE, RX_DECLICK_PATH)
    else:
        print(f"❌ Không tìm thấy Plugin tại: {RX_DECLICK_PATH}")
    