from aiogram.types import InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio

from bot.states import SectorStates
from db.crud import save_photo, get_user_photos, save_video, get_user_videos, save_document, get_user_documents, \
    save_audio, get_user_audios, save_voice, get_user_voices, save_letter, get_user_letters

MEDIA_TYPES = {
    "photo": {
        "add_state": SectorStates.add_photo,
        "main_state": SectorStates.photo,
        "file_attr": 'photo',
        "save_func": save_photo,
        "get_func": get_user_photos,
        "input_media": InputMediaPhoto,
    },
    "video": {
        "add_state": SectorStates.add_video,
        "main_state": SectorStates.video,
        "file_attr": "video",
        "save_func": save_video,
        "get_func": get_user_videos,
        "input_media": InputMediaVideo,
    },
    "document": {
        "add_state": SectorStates.add_document,
        "main_state": SectorStates.document,
        "file_attr": "document",
        "save_func": save_document,
        "get_func": get_user_documents,
        "input_media": InputMediaDocument,
    },
    "audio": {
        "add_state": SectorStates.add_audio,
        "main_state": SectorStates.audio,
        "file_attr": "audio",
        "save_func": save_audio,
        "get_func": get_user_audios,
        "input_media": InputMediaAudio,
    },
    "voice": {
        "add_state": SectorStates.add_voice,
        "main_state": SectorStates.voice,
        "file_attr": "voice",
        "save_func": save_voice,
        "get_func": get_user_voices,
        "input_media": None
    },
    "letter": {
        "add_state": SectorStates.add_letter,
        "main_state": SectorStates.letter,
        "file_attr": "text",
        "save_func": save_letter,
        "get_func": get_user_letters,
        "input_media": None,
    },
}
