from aiogram.fsm.state import StatesGroup, State


class SectorStates(StatesGroup):
    username = State()
    password = State()
    confirm_password = State()
    main_menu = State()

    photo = State()
    add_photo = State()
    view_photo = State()

    video = State()
    add_video = State()
    view_video = State()

    document = State()
    add_document = State()
    view_document = State()

    audio = State()
    add_audio = State()
    view_audio = State()

    voice = State()
    add_voice = State()
    view_voice = State()

    text_message = State()
    add_text_message = State()
    view_text_message = State()

    contact = State()
    add_contact = State()
    view_contact = State()

    contact_us = State()

    settings = State()
    change_username = State()
    change_password = State()


class LoginStates(StatesGroup):
    username = State()
    password = State()


class LanguageStates(StatesGroup):
    lang = State()
