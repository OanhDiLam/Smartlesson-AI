# 1. Dùng hình ảnh Python chính thức
FROM python:3.10-slim

# 2. Thiết lập thư mục làm việc trong container
WORKDIR /app

# 3. Copy file requirements và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy toàn bộ code vào container
COPY . .

# 5. Mở cổng 8501 (cổng mặc định của Streamlit)
EXPOSE 8501

# 6. Lệnh để chạy ứng dụng
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]


RUN pip install --upgrade google-generativeai