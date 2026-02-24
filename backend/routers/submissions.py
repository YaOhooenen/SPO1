from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import shutil
from datetime import datetime

from database import get_db
import models, schemas, dependencies

UPLOAD_DIR = "uploads/"

router = APIRouter(prefix="/submissions", tags=["submissions"])

@router.post("/", response_model=schemas.SubmissionOut)
async def create_submission(
    track_data: schemas.TrackCreate,
    file: UploadFile = File(...),
    current_user: models.User = Depends(dependencies.require_role("artist")),
    db: Session = Depends(get_db)
):
    # Проверяем, что у пользователя есть профиль артиста
    artist = db.query(models.Artist).filter(models.Artist.user_id == current_user.id).first()
    if not artist:
        raise HTTPException(status_code=400, detail="You need to create an artist profile first")

    # Сохраняем файл
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{datetime.utcnow().timestamp()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Создаём трек (неопубликованный)
    new_track = models.Track(
        title=track_data.title,
        duration=track_data.duration,
        album_id=track_data.album_id,
        artist_id=artist.id,
        file_path=file_path,
        is_published=False
    )
    db.add(new_track)
    db.commit()
    db.refresh(new_track)

    # Создаём заявку
    submission = models.Submission(
        artist_id=artist.id,
        track_id=new_track.id,
        status="pending"
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission