from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
import os

from database import get_db
import models, schemas, dependencies

router = APIRouter(prefix="/music", tags=["music"])

# Топ треков по прослушиваниям
@router.get("/top", response_model=list[schemas.TrackOut])
def get_top_tracks(limit: int = 20, db: Session = Depends(get_db)):
    tracks = db.query(models.Track).filter(models.Track.is_published == True).order_by(models.Track.play_count.desc()).limit(limit).all()
    return tracks

# Поиск
@router.get("/search", response_model=schemas.SearchResult)
def search(q: str, db: Session = Depends(get_db)):
    artists = db.query(models.Artist).filter(models.Artist.name.ilike(f"%{q}%")).all()
    albums = db.query(models.Album).filter(models.Album.title.ilike(f"%{q}%"), models.Album.is_published == True).all()
    tracks = db.query(models.Track).filter(models.Track.title.ilike(f"%{q}%"), models.Track.is_published == True).all()
    return {"artists": artists, "albums": albums, "tracks": tracks}

# Получение трека для прослушивания (увеличивает счетчик)
@router.get("/listen/{track_id}")
def listen_track(track_id: int, db: Session = Depends(get_db)):
    track = db.query(models.Track).filter(models.Track.id == track_id, models.Track.is_published == True).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    # Увеличиваем счетчик
    track.play_count += 1
    db.commit()
    # Возвращаем файл
    file_path = track.file_path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="audio/mpeg", filename=f"{track.title}.mp3")

# Скачивание трека (без увеличения счетчика? Можно тоже увеличивать)
@router.get("/download/{track_id}")
def download_track(track_id: int, db: Session = Depends(get_db)):
    track = db.query(models.Track).filter(models.Track.id == track_id, models.Track.is_published == True).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    file_path = track.file_path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="audio/mpeg", filename=f"{track.title}.mp3", headers={"Content-Disposition": f"attachment; filename={track.title}.mp3"})