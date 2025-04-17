from aiogram.fsm.state import StatesGroup, State


class SectorStates(StatesGroup):
    username = State()
    password = State()
    language = State()
    confirm_password = State()
    main_menu = State()

class LoginStates(StatesGroup):
    username = State()
    password = State()

