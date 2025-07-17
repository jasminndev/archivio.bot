from aiogram.fsm.state import StatesGroup, State


class SectorStates(StatesGroup):
    username = State()
    password = State()
    confirm_password = State()
    main_menu = State()

    photo = State()
    add_photo = State()
    send_photo = State()

    video = State()
    add_video = State()

    document = State()
    add_document = State()

    audio = State()
    add_audio = State()

    voice = State()
    add_voice = State()

    letter = State()
    add_letter = State()

    contact = State()
    add_contact = State()

    contact_us = State()

    waiting_photos = State()


class LoginStates(StatesGroup):
    username = State()
    password = State()


class LanguageStates(StatesGroup):
    lang = State()
