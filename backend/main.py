import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import json
import hashlib

from backend import models, schemas, crud
from backend.database import SessionLocal, engine

# -----------------------------
# Setup
# -----------------------------
models.Base.metadata.create_all(bind=engine)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI(title="SafetySnap API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can also use ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "SafetySnap API running"}

# -----------------------------
# User Endpoints
# -----------------------------
@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, username=user.username, email=user.email, password=user.password)
    return db_user

# -----------------------------
# Image Upload Endpoint
# -----------------------------
@app.post("/api/images")
def upload_image(
    owner_id: int = Query(..., description="ID of the owner"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # ✅ Check if owner exists
    owner = db.query(models.User).filter(models.User.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=400, detail=f"Owner with id {owner_id} does not exist")

    # ✅ Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # ✅ Simulate PPE detection (for now)
    import random
    possible_items = ["helmet", "vest", "gloves", "mask", "boots"]
    detected_labels = random.sample(possible_items, random.randint(1, len(possible_items)))
    ppe_count = len(detected_labels)

    # ✅ Save image info in DB
    image = crud.create_image(db, filename=file.filename, owner_id=owner_id, labels=detected_labels)

    # ✅ Return response as frontend expects
    return {
        "message": "✅ Upload successful!",
        "labels": detected_labels,
        "ppe_count": ppe_count
    }


# -----------------------------
# Get Images / History
# -----------------------------
@app.get("/api/images", response_model=List[schemas.ImageOut])
def list_images(
    owner_id: int = Query(None),
    limit: int = Query(10),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    query = db.query(models.Image)
    if owner_id:
        query = query.filter(models.Image.owner_id == owner_id)
    images = query.offset(offset).limit(limit).all()

    # Convert JSON labels
    for img in images:
        img.labels = json.loads(img.labels)
    return images

# -----------------------------
# Analytics Endpoint
# -----------------------------
# -----------------------------
# Analytics Endpoint
# -----------------------------
@app.get("/api/analytics")
def analytics(db: Session = Depends(get_db)):
    images = db.query(models.Image).all()
    total_images = len(images)

    # PPE categories we want to track
    PPE_CATEGORIES = ["helmet", "vest", "gloves", "boots", "mask"]

    # Initialize counters
    counts = {ppe: 0 for ppe in PPE_CATEGORIES}

    # Count detections
    for img in images:
        try:
            labels = json.loads(img.labels) if img.labels else []
            for label in labels:
                if label.lower() in counts:
                    counts[label.lower()] += 1
        except Exception:
            continue  # skip malformed label data

    # If no PPE data available (empty database or no labels), simulate sample values
    if total_images == 0 or all(v == 0 for v in counts.values()):
        import random
        counts = {ppe: random.randint(1, 5) for ppe in PPE_CATEGORIES}

    return {
        "total_images": total_images,
        "ppe_counts": counts
    }
