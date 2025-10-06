from .db import SessionLocal
from sqlalchemy import text

def insert_item(name, description, image_path, text_emb, image_emb):
    with SessionLocal() as db:
        db.execute(
            text("""
                INSERT INTO items (name, description, image_path, text_embedding, image_embedding)
                VALUES (:n, :d, :ip, :te, :ie)
            """),
            {"n": name, "d": description, "ip": image_path,
             "te": list(text_emb), "ie": list(image_emb) if image_emb is not None else None}
        )
        db.commit()

def search_by_text_embedding(query_vec, limit=5):
    with SessionLocal() as db:
        res = db.execute(
            text("""
                SELECT id, name, description, image_path,
                       (text_embedding <-> :q) AS distance
                FROM items
                WHERE text_embedding IS NOT NULL
                ORDER BY text_embedding <-> :q
                LIMIT :lim
            """),
            {"q": list(query_vec), "lim": limit}
        ).fetchall()
        return res
