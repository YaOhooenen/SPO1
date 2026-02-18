from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://egorkazancev:1234@localhost:5432/eemusic"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True показывает SQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
