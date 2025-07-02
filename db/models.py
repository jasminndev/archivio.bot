from sqlalchemy import String, BIGINT, Text
from sqlalchemy.orm import Mapped, mapped_column

from db.utils import TimeBasedModel, Base


class User(TimeBasedModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.username})"


class InfoUser(TimeBasedModel):
    __tablename__ = "info_users"

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    tg_username: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)


class Photo(TimeBasedModel):
    __tablename__ = "photos"

    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    file_id: Mapped[str] = mapped_column(String(1000), nullable=False)


class Video(TimeBasedModel):
    __tablename__ = "videos"

    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    file_id: Mapped[str] = mapped_column(String(1000), nullable=False)


class Document(TimeBasedModel):
    __tablename__ = "documents"

    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    file_id: Mapped[str] = mapped_column(String(1000), nullable=False)


class Letter(TimeBasedModel):
    __tablename__ = "letters"

    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)


class Audio(TimeBasedModel):
    __tablename__ = "audios"

    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    file_id: Mapped[str] = mapped_column(String(1000), nullable=False)


class Voice(TimeBasedModel):
    __tablename__ = "voices"

    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    file_id: Mapped[str] = mapped_column(String(1000), nullable=False)


class Contact(TimeBasedModel):
    __tablename__ = "contacts"

    user_id: Mapped[int] = mapped_column(BIGINT, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=True)


metadata = Base.metadata
