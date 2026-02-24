from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Table, Text, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# Таблицы для избранного (многие ко многим)
favorite_tracks = Table(
    'favorite_tracks',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('track_id', Integer, ForeignKey('tracks.id'))
)

favorite_albums = Table(
    'favorite_albums',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('album_id', Integer, ForeignKey('albums.id'))
)

favorite_artists = Table(
    'favorite_artists',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('artist_id', Integer, ForeignKey('artists.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default='user')  # 'user', 'artist', 'admin'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи с избранным
    favorite_tracks = relationship('Track', secondary=favorite_tracks, backref='favorited_by')
    favorite_albums = relationship('Album', secondary=favorite_albums, backref='favorited_by')
    favorite_artists = relationship('Artist', secondary=favorite_artists, backref='favorited_by')

    # Связь с артистом (если пользователь - артист)
    artist = relationship('Artist', back_populates='user', uselist=False)

class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    bio = Column(Text)
    avatar = Column(String)  # url или путь к картинке
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)

    user = relationship('User', back_populates='artist')
    albums = relationship('Album', back_populates='artist')
    tracks = relationship('Track', back_populates='artist')
    submissions = relationship('Submission', back_populates='artist')

class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)
    release_date = Column(DateTime)
    cover_image = Column(String)
    type = Column(String)  # 'album' или 'single'
    is_published = Column(Boolean, default=False)

    artist = relationship('Artist', back_populates='albums')
    tracks = relationship('Track', back_populates='album')

class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    duration = Column(Integer)  # в секундах
    album_id = Column(Integer, ForeignKey('albums.id'), nullable=True)
    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)
    file_path = Column(String, nullable=False)  # путь к файлу на сервере
    play_count = Column(BigInteger, default=0)
    is_published = Column(Boolean, default=False)

    album = relationship('Album', back_populates='tracks')
    artist = relationship('Artist', back_populates='tracks')
    submissions = relationship('Submission', back_populates='track')

class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)
    track_id = Column(Integer, ForeignKey('tracks.id'), nullable=False)
    status = Column(String, default='pending')  # pending, approved, rejected
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    artist = relationship('Artist', back_populates='submissions')
    track = relationship('Track', back_populates='submissions')