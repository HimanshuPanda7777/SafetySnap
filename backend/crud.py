from sqlalchemy.orm import Session
from backend import models
import hashlib
import json

# -----------------------------
# User CRUD
# -----------------------------
def create_user(db: Session, username: str, email: str, password: str):
    user = models.User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# -----------------------------
# Image CRUD
# -----------------------------
def create_image(db: Session, filename: str, owner_id: int, labels: list = None, bbox: dict = None):
    if labels is None:
        labels = []
    if bbox is None:
        bbox = {}

    # Convert list to JSON string
    labels_json = json.dumps(labels)

    # Generate a simple hash of filename + owner_id
    detections_hash = hashlib.sha256(f"{filename}{owner_id}".encode()).hexdigest()

    image = models.Image(
        filename=filename,
        owner_id=owner_id,
        labels=labels_json,  # store JSON string
        detections_hash=detections_hash,
        bbox_x=bbox.get("x"),
        bbox_y=bbox.get("y"),
        bbox_w=bbox.get("w"),
        bbox_h=bbox.get("h")
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return image
