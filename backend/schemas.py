from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# -----------------------------
# User Schemas
# -----------------------------
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

# -----------------------------
# Image Schemas
# -----------------------------
class ImageOut(BaseModel):
    id: int
    filename: str
    labels: List[str] = []
    bbox_x: Optional[float] = None
    bbox_y: Optional[float] = None
    bbox_w: Optional[float] = None
    bbox_h: Optional[float] = None
    detections_hash: Optional[str] = None
    uploaded_at: datetime
    owner_id: int

    class Config:
        orm_mode = True
