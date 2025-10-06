from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil, os, uuid, json
from db import cursor, conn
from utils import get_text_embedding, get_image_embedding, cosine_similarity
import numpy as np

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve static files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# ---------------- Upload Item ----------------
@app.post("/upload")
async def upload_item(
    name: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(None)
):
    file_path = None
    text_vec = get_text_embedding(description)
    image_vec = None

    # Handle file upload
    if file:
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        image_vec = get_image_embedding(file_path)
        image_url = f"/uploads/{filename}"
    else:
        image_url = None

    # Store embeddings as JSON strings
    cursor.execute(
        "INSERT INTO items (name, description, image_path, text_embedding, image_embedding) VALUES (%s, %s, %s, %s, %s)",
        (
            name,
            description,
            image_url,
            json.dumps(text_vec.tolist()),
            json.dumps(image_vec.tolist()) if image_vec is not None else None
        )
    )
    conn.commit()
    return {"status": "success", "image_url": image_url}

# ---------------- Search Items ----------------
@app.post("/search")
async def search_item(text: str = Form(None), file: UploadFile = File(None)):
    query_text_vec = np.array(get_text_embedding(text), dtype=float) if text else None
    query_image_vec = None
    tmp_path = None

    # Handle temporary file for image query
    if file:
        tmp_filename = f"{uuid.uuid4()}_{file.filename}"
        tmp_path = os.path.join(UPLOAD_DIR, tmp_filename)
        with open(tmp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        query_image_vec = np.array(get_image_embedding(tmp_path), dtype=float)

    cursor.execute("SELECT id, name, description, image_path, text_embedding, image_embedding FROM items")
    rows = cursor.fetchall()
    results = []

    for r in rows:
        id, name, description, image_url, text_vec_str, image_vec_str = r
        score = 0.0

        # Compare text embeddings
        if query_text_vec is not None and text_vec_str:
            text_vec = np.array(json.loads(text_vec_str), dtype=float)
            score += cosine_similarity(text_vec, query_text_vec)

        # Compare image embeddings
        if query_image_vec is not None and image_vec_str:
            image_vec = np.array(json.loads(image_vec_str), dtype=float)
            score += cosine_similarity(image_vec, query_image_vec)

        results.append({
            "id": id,
            "name": name,
            "description": description,
            "image_url": image_url,
            "score": float(score)  # ensure JSON serializable
        })

    # Clean up temporary file
    if tmp_path and os.path.exists(tmp_path):
        os.remove(tmp_path)

    results.sort(key=lambda x: x["score"], reverse=True)
    return {"results": results[:5]}
