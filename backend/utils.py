import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", use_fast=False)
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

def get_text_embedding(text):
    inputs = processor(text=[text], return_tensors="pt", padding=True)
    with torch.no_grad():
        embeddings = model.get_text_features(**inputs)
    return embeddings[0].numpy()

def get_image_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        embeddings = model.get_image_features(**inputs)
    return embeddings[0].numpy()

def cosine_similarity(vec1, vec2):
    import numpy as np
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
