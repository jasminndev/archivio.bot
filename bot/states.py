from aiogram.fsm.state import StatesGroup, State


class SectorStates(StatesGroup):
    username = State()
    password = State()
    confirm_password = State()
    main_menu = State()


class LoginStates(StatesGroup):
    username = State()
    password = State()

class LanguageStates(StatesGroup):
    language = State()
    lang = State()

class MainMenu(StatesGroup):
    photo = State()
    video = State()
    document = State()
    letter = State()
    main = State()
