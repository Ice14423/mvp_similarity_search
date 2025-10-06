from sentence_transformers import SentenceTransformer
import numpy as np
from PIL import Image

# โหลดโมเดล CLIP (Text + Image)
model = SentenceTransformer("sentence-transformers/clip-ViT-B-32", device="cpu")

def get_text_embedding(text: str):
    """รับข้อความและคืนค่า embedding (vector)"""
    embedding = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
    return embedding.tolist()

def get_image_embedding(image_path: str):
    """รับพาธรูปภาพและคืนค่า embedding (vector)"""
    image = Image.open(image_path)
    embedding = model.encode(image, convert_to_numpy=True, normalize_embeddings=True)
    return embedding.tolist()
