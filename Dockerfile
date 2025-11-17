FROM python:3.11-slim

# Cài đặt FFmpeg và các dependencies hệ thống
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Tạo thư mục làm việc
WORKDIR /app

# Copy requirements và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code ứng dụng
COPY app.py .
COPY downloads/ downloads/

# Tạo thư mục downloads nếu chưa có
RUN mkdir -p downloads

# Expose port (Render sẽ tự động map PORT)
EXPOSE 5000

# Chạy ứng dụng với gunicorn (sử dụng PORT từ biến môi trường Render)
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers 2 --timeout 300

