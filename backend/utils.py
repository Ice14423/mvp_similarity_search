import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import io
import numpy as np

# โหลดโมเดล CLIP เพียงครั้งเดียว
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", use_fast=False)
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")


def get_text_embedding(text):
    """รับข้อความแล้วคืนค่า embedding เป็น numpy array"""
    inputs = processor(text=[text], return_tensors="pt", padding=True)
    with torch.no_grad():
        embeddings = model.get_text_features(**inputs)
    return embeddings[0].numpy()


def get_image_embedding(image_source):
    """
    รับภาพได้ทั้งแบบ path หรือ UploadFile แล้วคืนค่า embedding เป็น numpy array
    """
    # ถ้าเป็น UploadFile → อ่านจาก memory
    if hasattr(image_source, "file"):
        image_bytes = image_source.file.read()
        image_source.file.seek(0)  # รีเซ็ต pointer เพื่อไม่ให้ fastapi error ภายหลัง
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    else:
        # ถ้าเป็น path string → เปิดจากไฟล์
        image = Image.open(image_source).convert("RGB")

    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        embeddings = model.get_image_features(**inputs)
    return embeddings[0].numpy()


def cosine_similarity(vec1, vec2):
    """คำนวณความคล้ายคลึง (cosine similarity) ระหว่างเวกเตอร์"""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
