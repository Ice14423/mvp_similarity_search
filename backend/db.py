import psycopg2
import os
from dotenv import load_dotenv  # ต้องติดตั้ง: pip install python-dotenv

# โหลดตัวแปรจากไฟล์ .env
load_dotenv()

# ดึงค่าจาก environment variables
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# เชื่อมต่อ PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = conn.cursor()
print("Connected to PostgreSQL successfully!")
