import base64
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import json
import psycopg2
from db import cursor, conn
from utils import get_text_embedding, get_image_embedding, cosine_similarity
import numpy as np
import io
from PIL import Image

app = FastAPI()

# ------------------- CORS -------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ------------------- Upload Item -------------------
@app.post("/upload")
async def upload_item(
    name: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(None)
):
    text_vec = get_text_embedding(description)
    image_vec = None
    image_blob = None

    if file:
        # อ่านไฟล์ภาพจาก memory
        image_bytes = await file.read()
        image_blob = image_bytes  # เก็บ blob ไว้ในฐานข้อมูล
        file.file.seek(0)  # รีเซ็ต pointer ให้ใช้ซ้ำได้

        # ใช้ฟังก์ชัน utils ที่แก้ไว้ใหม่
        image_vec = get_image_embedding(file)

    cursor.execute(
        """
        INSERT INTO items (name, description, image_blob, text_embedding, image_embedding)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            name,
            description,
            psycopg2.Binary(image_blob) if image_blob else None,
            json.dumps(text_vec.tolist()),
            json.dumps(image_vec.tolist()) if image_vec is not None else None
        )
    )
    conn.commit()

    return {"status": "success"}


# ------------------- Search Items -------------------
@app.post("/search")
async def search_item(text: str = Form(None), file: UploadFile = File(None)):
    query_text_vec = np.array(get_text_embedding(text), dtype=float) if text else None
    query_image_vec = None

    # อ่านไฟล์ภาพที่อัปโหลดเพื่อค้นหา
    if file:
        await file.read()
        file.file.seek(0)  # reset pointer
        query_image_vec = np.array(get_image_embedding(file), dtype=float)

    # ดึงข้อมูลทั้งหมดจาก DB
    cursor.execute("SELECT id, name, description, image_blob, text_embedding, image_embedding FROM items")
    rows = cursor.fetchall()

    results = []

    for r in rows:
        id, name, description, image_blob, text_vec_str, image_vec_str = r
        score = 0.0

        # Text embedding
        text_vec = None
        if text_vec_str:
            text_vec = np.array(json.loads(text_vec_str), dtype=float)
            if query_text_vec is not None:
                score += cosine_similarity(text_vec, query_text_vec)

        # Image embedding
        image_vec = None
        if image_vec_str:
            image_vec = np.array(json.loads(image_vec_str), dtype=float)
            if query_image_vec is not None:
                score += cosine_similarity(image_vec, query_image_vec)

        # แปลง image_blob → base64
        image_base64 = base64.b64encode(image_blob).decode('utf-8') if image_blob else None

        results.append({
            "id": id,
            "name": name,
            "description": description,
            "image_base64": image_base64,
            "score": float(score),
            "text_vector": text_vec.tolist() if text_vec is not None else None,
            "image_vector": image_vec.tolist() if image_vec is not None else None   # <-- เพิ่มตรงนี้
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return {"results": results[:5]}
