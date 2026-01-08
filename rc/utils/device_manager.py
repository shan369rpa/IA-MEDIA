import torch
import logging

def get_optimal_device():
    """
    Tự động phát hiện thiết bị mạnh nhất:
    - NVIDIA GPU -> 'cuda'
    - Apple Silicon GPU -> 'mps'
    - CPU -> 'cpu'
    """
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        # Kiểm tra xem MPS có khả dụng không (macOS 12.3+)
        logging.info("Phát hiện Apple Silicon (M-series). Sử dụng Metal (MPS) để tăng tốc.")
        return "mps"
    else:
        return "cpu"

def clear_memory():
    """Dọn dẹp bộ nhớ VRAM/RAM"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    elif torch.backends.mps.is_available():
        torch.mps.empty_cache()