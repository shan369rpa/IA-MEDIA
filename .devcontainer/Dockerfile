# Sử dụng image Python & Docker chính thức từ Microsoft
FROM mcr.microsoft.com/devcontainers/python:1-3.10-bullseye

# Cài đặt FFmpeg và các công cụ hệ thống cần thiết
# '-y' tự động trả lời yes cho các câu hỏi cài đặt
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends ffmpeg

# Cài đặt các thư viện Python cho dự án
# --no-cache-dir để giữ cho image gọn nhẹ
COPY requirements.txt /tmp/pip-tmp/
RUN python3 -m pip install --no-cache-dir -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp