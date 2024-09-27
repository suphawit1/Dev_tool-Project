# Dockerfile สำหรับ Django
FROM python:3.9-slim

# ตั้งค่า working directory
WORKDIR /Dev_tool-Project

# คัดลอกไฟล์ requirements.txt ไปยัง container และติดตั้ง dependencies
COPY requirements.txt /Dev_tool-Project/
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมดไปยัง container
COPY . /Dev_tool-Project/

# เปิดพอร์ต 8000 เพื่อให้สามารถเข้าถึง Django server ได้
EXPOSE 8000

# รันคำสั่งเพื่อเริ่ม Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]