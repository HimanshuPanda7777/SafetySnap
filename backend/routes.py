from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from backend import crud, schemas, database
import shutil
import os

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(db, user)

@router.post("/api/images", response_model=schemas.ImageOut)
def upload_image(owner_id: int, file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    # check owner exists
    owner = crud.get_user(db, owner_id)
    if not owner:
        raise HTTPException(status_code=400, detail=f"Owner with id {owner_id} does not exist")

    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_data = schemas.ImageCreate(
        owner_id=owner_id,
        filename=file.filename,
        labels=[],
        bbox_x=None,
        bbox_y=None,
        bbox_w=None,
        bbox_h=None
    )
    return crud.create_image(db, image_data)

@router.get("/api/images")
def list_images(limit: int = 10, offset: int = 0, db: Session = Depends(database.get_db)):
    return crud.get_images(db, limit=limit, offset=offset)

@router.get("/api/labels")
def labels_count(db: Session = Depends(database.get_db)):
    return crud.get_labels_count(db)
