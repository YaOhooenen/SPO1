from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models, schemas, dependencies

router = APIRouter(prefix="/artists", tags=["artists"])


@router.post("/", response_model=schemas.ArtistOut)
def create_artist(
        artist: schemas.ArtistCreate,
        current_user: models.User = Depends(dependencies.get_current_active_user),
        db: Session = Depends(get_db)
):
    # Проверяем, не создан ли уже профиль артиста для этого пользователя
    existing = db.query(models.Artist).filter(models.Artist.user_id == current_user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Artist profile already exists")

    # Создаём профиль артиста
    new_artist = models.Artist(
        name=artist.name,
        bio=artist.bio,
        avatar=artist.avatar,
        user_id=current_user.id
    )
    db.add(new_artist)

    # Меняем роль пользователя на artist
    current_user.role = "artist"

    db.commit()
    db.refresh(new_artist)
    return new_artist


# Получение карточки артиста с его альбомами и треками (этот эндпоинт не требует специальной роли)
@router.get("/{artist_id}")
def get_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = db.query(models.Artist).filter(models.Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    albums = db.query(models.Album).filter(models.Album.artist_id == artist_id, models.Album.is_published == True).all()
    tracks = db.query(models.Track).filter(models.Track.artist_id == artist_id, models.Track.is_published == True).all()
    return {
        "artist": artist,
        "albums": albums,
        "tracks": tracks
    }