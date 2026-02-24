from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Artist schemas
class ArtistBase(BaseModel):
    name: str
    bio: Optional[str] = None
    avatar: Optional[str] = None


class ArtistCreate(ArtistBase):
    pass


class ArtistOut(ArtistBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# Album schemas
class AlbumBase(BaseModel):
    title: str
    release_date: Optional[datetime] = None
    cover_image: Optional[str] = None
    type: str  # 'album' или 'single'


class AlbumCreate(AlbumBase):
    pass


class AlbumOut(AlbumBase):
    id: int
    artist_id: int
    is_published: bool

    model_config = ConfigDict(from_attributes=True)


# Track schemas
class TrackBase(BaseModel):
    title: str
    duration: Optional[int] = None


class TrackCreate(TrackBase):
    album_id: Optional[int] = None


class TrackOut(TrackBase):
    id: int
    artist_id: int
    album_id: Optional[int] = None
    play_count: int
    is_published: bool
    file_path: str

    model_config = ConfigDict(from_attributes=True)


# Submission schemas
class SubmissionBase(BaseModel):
    track_id: int


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionOut(SubmissionBase):
    id: int
    artist_id: int
    status: str
    submitted_at: datetime
    reviewed_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Favorites response schemas
class FavoriteArtists(BaseModel):
    artists: List[ArtistOut]


class FavoriteAlbums(BaseModel):
    albums: List[AlbumOut]


class FavoriteTracks(BaseModel):
    tracks: List[TrackOut]


# Search result schema
class SearchResult(BaseModel):
    artists: List[ArtistOut]
    albums: List[AlbumOut]
    tracks: List[TrackOut]