from sqlalchemy import Column, Integer, String, ForeignKey, Sequence
from sqlalchemy.orm import relationship

from database import Base

class TrackDB(Base):
    __tablename__ = "tracks"
    id = Column(Integer, Sequence('tracks_id_seq'), primary_key=True)
    url = Column(String, unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    genre = Column(String(50), nullable=False)
    image = Column(String, nullable=False)
    likes = Column(Integer, nullable=False)

    album_id = Column(Integer, ForeignKey("albums.id", ondelete="CASCADE"))
    artist_id = Column(Integer, ForeignKey("artists.id", ondelete="CASCADE"))

    album = relationship("AlbumDB", back_populates="tracks")
    artist = relationship("ArtistDB", back_populates="tracks")
class AlbumDB(Base):
    __tablename__ = "albums"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    img = Column(String, nullable=False)
    countlisten = Column(Integer, nullable=False)
    likes = Column(Integer, nullable=False)

    artist_id = Column(Integer, ForeignKey("artists.id", ondelete="CASCADE"))

    artist = relationship("ArtistDB", back_populates="albums")
    tracks = relationship("TrackDB", back_populates="album")

class ArtistDB(Base):
    __tablename__ = "artists"
    id = Column(Integer, Sequence('songers_id_seq'), primary_key=True)
    name = Column(String(50))

    albums = relationship("AlbumDB", back_populates="artist")
    tracks = relationship("TrackDB", back_populates="artist")

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    nickname = Column(String(50), nullable=False)
    image = Column(String, nullable=False)
    savedAlbums = relationship("AlbumDB", back_populates="user")
    savedTracks = relationship("TrackDB", back_populates="user")
