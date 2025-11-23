# Sử dụng image Python & Docker chính thức từ Microsoft làm nền tảng.
# Phiên bản: Python 3.10 trên Debian 11 (Bullseye).
FROM mcr.microsoft.com/devcontainers/python:1-3.10-bullseye

# Cài đặt các công cụ hệ thống cần thiết từ APT (Advanced Package Tool).
# - ffmpeg: Công cụ mạnh mẽ để xử lý audio và video.
# - git-lfs: Mở rộng của Git để quản lý các file lớn.
# Ghi chú:
#   - apt-get update: Cập nhật danh sách các gói phần mềm.
#   - export DEBIAN_FRONTEND=noninteractive: Tránh các câu hỏi tương tác trong quá trình cài đặt.
#   - -y: Tự động trả lời "yes" cho các câu hỏi cài đặt.
#   - --no-install-recommends: Chỉ cài đặt các gói cần thiết, giữ cho image gọn nhẹ.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends ffmpeg git-lfs postgresql-client libsndfile1 sox

# Sao chép file requirements.txt từ máy host vào một thư mục tạm bên trong container.
# Điều này tối ưu hóa cơ chế cache của Docker. Nếu file requirements.txt không thay đổi,
# bước cài đặt thư viện sẽ không cần chạy lại khi rebuild.
COPY requirements.txt /tmp/pip-tmp/

# Cài đặt tất cả các thư viện Python được định nghĩa trong requirements.txt.
# Ghi chú:
#   - python3 -m pip: Cách gọi pip được khuyến nghị để đảm bảo dùng đúng phiên bản.
#   - --no-cache-dir: Không lưu cache của pip, giúp giảm kích thước cuối cùng của image.
#   - rm -rf /tmp/pip-tmp: Xóa thư mục tạm sau khi cài đặt xong để giữ sạch sẽ.
RUN python3 -m pip install --no-cache-dir -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp
# Cài đặt dự án ở chế độ editable
COPY . /workspaces/IA-MEDIA
WORKDIR /workspaces/IA-MEDIA
RUN pip install -e .