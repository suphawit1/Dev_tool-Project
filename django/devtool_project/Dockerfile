# Dockerfile สำหรับ Django
FROM python:3.9-slim

# ติดตั้ง dependencies ที่จำเป็นสำหรับ mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    libmariadb-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# คัดลอกไฟล์ requirements.txt ไปยัง container และติดตั้ง dependencies
COPY requirements.txt /Dev_tool-Project/
RUN pip install --no-cache-dir -r /Dev_tool-Project/requirements.txt

# คัดลอกโค้ดทั้งหมดไปยัง container
COPY . /Dev_tool-Project/

# เปิดพอร์ต 8000
EXPOSE 8000

# รันคำสั่งเพื่อเริ่ม Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]