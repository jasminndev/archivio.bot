from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Photo, Video, Document, Letter, Audio, Voice, Contact


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


async def save_audio(db: AsyncSession, user_id: int, file_id: str):
    audio = Audio(user_id=user_id, file_id=file_id)
    db.add(audio)
    await db.commit()
    await db.refresh(audio)
    return audio


async def save_voice(db: AsyncSession, user_id: int, file_id: str):
    voice = Voice(user_id=user_id, file_id=file_id)
    db.add(voice)
    await db.commit()
    await db.refresh(voice)
    return voice


async def save_contact(
        db: AsyncSession,
        user_id: int,
        phone_number: str,
        first_name: str,
        last_name: str | None = None
):
    contact = Contact(
        user_id=user_id,
        phone_number=phone_number,
        first_name=first_name,
        last_name=last_name
    )
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def get_user_photos(db: AsyncSession, user_id: int):
    stmt = select(Photo).where(Photo.user_id == user_id).order_by(Photo.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user_videos(db: AsyncSession, user_id: int):
    stmt = select(Video).where(Video.user_id == user_id).order_by(Video.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user_documents(db: AsyncSession, user_id: int):
    stmt = select(Document).where(Document.user_id == user_id).order_by(Document.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user_letters(db: AsyncSession, user_id: int):
    stmt = select(Letter).where(Letter.user_id == user_id).order_by(Letter.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user_audios(db: AsyncSession, user_id: int):
    stmt = select(Audio).where(Audio.user_id == user_id).order_by(Audio.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user_voices(db: AsyncSession, user_id: int):
    stmt = select(Voice).where(Voice.user_id == user_id).order_by(Voice.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user_contacts(db: AsyncSession, user_id: int):
    stmt = select(Contact).where(Contact.user_id == user_id).order_by(Contact.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()
