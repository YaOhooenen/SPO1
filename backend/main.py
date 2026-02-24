from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import users, artists, music, favorites, submissions, admin

app = FastAPI(title="Music App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(artists.router)
app.include_router(music.router)
app.include_router(favorites.router)
app.include_router(submissions.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Music App API"}