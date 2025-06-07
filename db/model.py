from contextlib import asynccontextmanager
from datetime import datetime
from os import getenv

from dotenv import load_dotenv
from sqlalchemy import String, create_engine, BIGINT, TIMESTAMP, text, Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

load_dotenv()

ENGINE = getenv('ENGINE')
engine = create_engine(ENGINE, echo=True)
tz = "TIMEZONE('Asia/Tashkent', NOW())"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.username})"


class InfoUser(Base):
    __tablename__ = "info_users"

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    tg_username: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    started_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text(tz))


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    file_id: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text(tz))


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    file_id: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text(tz))


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    file_id: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text(tz))


class Letter(Base):
    __tablename__ = "letters"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text(tz))


async def save_photo(db: AsyncSession, user_id: int, file_id: str):
    photo = Photo(user_id=user_id, file_id=file_id)
    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    return photo


async def save_video(db: AsyncSession, user_id: int, file_id: str):
    video = Video(user_id=user_id, file_id=file_id)
    db.add(video)
    await db.commit()
    await db.refresh(video)
    return video


async def save_document(db: AsyncSession, user_id: int, file_id: str):
    document = Document(user_id=user_id, file_id=file_id)
    db.add(document)
    await db.commit()
    await db.refresh(document)
    return document


async def save_letter(db: AsyncSession, user_id: int, content: str):
    letter = Letter(user_id=user_id, content=content)
    db.add(letter)
    await db.commit()
    await db.refresh(letter)
    return letter


async def get_user_photos(db: AsyncSession, user_id: int):
    from sqlalchemy import select

    stmt = select(Photo).where(Photo.user_id == user_id).order_by(Photo.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@asynccontextmanager
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
