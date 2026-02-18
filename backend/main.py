from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal
from models import ArtistDB, AlbumDB, TrackDB

app = FastAPI()

def get_db():
    db = SessionLocal()
    print(str(db.bind))
    try:
        yield db
    finally:
        db.close()

class Artist(BaseModel):
    name: str

class Album(BaseModel):
    name: str
    img: str
    countlisten: int
    likes: int
    artist_id: int

class Track(BaseModel):
    url: str
    name: str
    genre: str
    image: str
    likes: int

    album_id: int
    artist_id: int


@app.get("/artists")
def get_artists(db: Session = Depends(get_db)):
    artists = db.query(ArtistDB).all()
    return {"artists": [ {"id": a.id, "name": a.name} for a in artists ]}

@app.post("/artists")
def add_artist(artist: Artist, db: Session = Depends(get_db)):
    new_artist = ArtistDB(name=artist.name)
    db.add(new_artist)
    db.commit()
    db.refresh(new_artist)
    return {"id": new_artist.id, "name": new_artist.name}


@app.get("/albums")
def get_albums(db: Session = Depends(get_db)):
    albums = db.query(AlbumDB).all()
    return {"albums": [ {"id": a.id, "name": a.name, "img": a.img, "count": a.countlisten, "likes": a.likes, "artist_id": a.artist_id} for a in albums ] }

@app.post("/albums")
def add_album(album: Album, db: Session = Depends(get_db)):
    try:
        new_album = AlbumDB(name=album.name, img=album.img, countlisten=album.countlisten, likes=album.likes, artist_id=album.artist_id)
        db.add(new_album)
        db.commit()
        db.refresh(new_album)
        return {"id": new_album.id, "name": new_album.name, "img": new_album.img, "countlisten": new_album.countlisten, "likes": new_album.likes, "artist_id": new_album.artist_id}
    except Exception as e:
        return {"error": f"Something went wrong, {e.args}"}

@app.get("/tracks")
def get_tracks(db: Session = Depends(get_db)):
    tracks = db.query(TrackDB).all()
    return {"tracks": [ {"id": t.id, "url": t.url, "name": t.name, "genre": t.genre, "image": t.image, "likes": t.likes, "album_id": t.album_id, "artist_id": t.artist_id } for t in tracks ]}
@app.post("/tracks")
def add_track(track: Track, db: Session = Depends(get_db)):
    try:
        new_track = TrackDB(name=track.name, url=track.url, genre=track.genre, image=track.image, likes=track.likes, artist_id=track.artist_id, album_id=track.album_id)
        db.add(new_track)
        db.commit()
        db.refresh(new_track)
        return {"id": new_track.id, "name": new_track.name, "url": new_track.url, "genre": new_track.genre, "image": new_track.image, "likes": new_track.likes, "artist_id": new_track.artist_id, "album_id": new_track.album_id}
    except Exception as e:
        return {"error": f"Something went wrong, {e.args}"}