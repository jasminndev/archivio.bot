import logging
import re

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from sqlalchemy.orm import sessionmaker

from bot.dispatcher import dp
from bot.handler.functions import hash_password
from bot.states import SectorStates
from db.model import *

logger = logging.getLogger(__name__)

user_states = {}
session = sessionmaker(engine)()


def valid_username(username: str) -> bool:
    try:
        return session.query(User).filter_by(username=username).first() is not None
    except Exception as e:
        print(f"Database error: {e}")
        return False


def valid_password(password: str) -> bool:
    return bool(re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$", password))


@dp.message(Command("register"))
async def command_register(message: Message, state: FSMContext):
    user_id = message.chat.id
    if session.get(User, user_id):
        return await message.answer(_("✅ You are already registered!"))

    await state.set_state(SectorStates.username)
    await message.answer(_("📝 Enter your username"))


@dp.message(SectorStates.username)
async def process_username(message: Message, state: FSMContext):
    username = message.text.strip()

    if not (3 <= len(username) <= 20):
        return await message.answer(_("❌ Username must be between 3 and 20 characters."))

    if valid_username(username):
        return await message.answer(_("❌ This username is already taken. Please choose another."))

    await state.update_data(username=username)
    await state.set_state(SectorStates.password)
    await message.answer(
        _("🔒 Create a password.\n\n"
          "It must be at least 6 characters long and contain both letters and numbers."))


@dp.message(SectorStates.password)
async def process_password(message: Message, state: FSMContext):
    password = message.text.strip()

    if not valid_password(password):
        return await message.answer(
            _("❌ Password must be at least 6 characters long and contain both letters and numbers. Please create another."))

    await state.update_data(password=password)
    await state.set_state(SectorStates.confirm_password)
    await message.answer(_("🔄 Please re-enter your password to confirm."))


@dp.message(SectorStates.confirm_password)
async def process_confirm_password(message: Message, state: FSMContext):
    user_input = message.text.strip()
    data = await state.get_data()

    if user_input != data.get('password'):
        return await message.answer(_("❌ Passwords do not match. Please try again."))

    try:
        new_user = User(
            user_id=message.chat.id,
            username=data['username'],
            password=hash_password(data['password'])
        )

        session.add(new_user)
        session.commit()
    except Exception as e:
        logger.error(f"Error while creating a user: {e}")
        await message.answer(_("⚠️ An error occurred while registering. Please try again later."))
        return

    await state.clear()
    await message.answer(_("🎉 You have successfully registered!\n\n"
                           "Now, you can use /login command to log in"))
