MEDIA_TYPES = {
    "photo": {
        "add_state": "add_photo",
        "main_state": "photo",
        "file_attr": "photo",  # aiogram types.Message.photo
        "save_func": "save_photo",
        "get_func": "get_user_photos",
        "input_media": "InputMediaPhoto",
    },
    "video": {
        "add_state": "add_video",
        "main_state": "video",
        "file_attr": "video",
        "save_func": "save_video",
        "get_func": "get_user_videos",
        "input_media": "InputMediaVideo",
    },
    "document": {
        "add_state": "add_document",
        "main_state": "document",
        "file_attr": "document",
        "save_func": "save_document",
        "get_func": "get_user_documents",
        "input_media": "InputMediaDocument",
    },
    "audio": {
        "add_state": "add_audio",
        "main_state": "audio",
        "file_attr": "audio",
        "save_func": "save_audio",
        "get_func": "get_user_audios",
        "input_media": "InputMediaAudio",
    },
    "voice": {
        "add_state": "add_voice",
        "main_state": "voice",
        "file_attr": "voice",
        "save_func": "save_voice",
        "get_func": "get_user_voices",
        "input_media": None  # voice can't be grouped
    },
    "letter": {
        "add_state": "add_letter",
        "main_state": "letter",
        "file_attr": "text",
        "save_func": "save_letter",
        "get_func": "get_user_letters",
        "input_media": None,
    }
}
