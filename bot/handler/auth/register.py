import logging
import re

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.buttons.functions import hash_password
from bot.dispatcher import dp
from bot.states import SectorStates
from db.models import *

logger = logging.getLogger(__name__)


async def valid_username(username: str) -> bool:
    try:
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False
        if not (3 <= len(username) <= 20):
            return False

        existing_user = await User.filter_one(username=username)
        return not existing_user
    except Exception as e:
        logging.error(f"Error checking username availability: {e}")
        return False


async def valid_password(password: str) -> bool:
    return bool(re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$", password))


@dp.message(Command(commands=["register"]))
async def command_register(message: Message, state: FSMContext):
    tg_id = str(message.chat.id)
    existing_user = await User.filter_one(tg_id=tg_id, username__not=None)

    if existing_user:
        await message.answer(_("✅ You are already registered!"))
        return

    await state.set_state(SectorStates.username)
    await message.answer(_("📝 Enter your username"))


@dp.message(SectorStates.username)
async def process_username(message: Message, state: FSMContext):
    username = message.text.strip()

    if not await valid_username(username):
        await message.answer(_("❌ This username is already taken. Please choose another."))
        return

    await state.update_data(username=username.lower())
    await state.set_state(SectorStates.password)
    await message.answer(
        _("🔒 Create a password.\n\n"
          "It must be at least 6 characters long and contain both letters and numbers."))


@dp.message(SectorStates.password)
async def process_password(message: Message, state: FSMContext):
    password = message.text.strip()

    if not await valid_password(password):
        await message.answer(
            _("❌ Password must be at least 6 characters long and contain both letters and numbers. Please create another."))
        return

    await state.update_data(password=password)
    await state.set_state(SectorStates.confirm_password)
    await message.answer(_("🔄 Please re-enter your password to confirm."))


@dp.message(SectorStates.confirm_password)
async def process_confirm_password(message: Message, state: FSMContext):
    user_input = message.text.strip()
    data = await state.get_data()

    if user_input != data.get('password'):
        await message.answer(_("❌ Passwords do not match. Please try again."))
        return

    try:
        tg_id = str(message.chat.id)
        user = await User.filter_one(tg_id=tg_id)
        if user:
            await User.update(
                _id=user.id,
                username=data['username'],
                password=await hash_password(data['password']),
            )
        else:
            hashed = await hash_password(data['password'])
            await User.create(
                tg_id=tg_id,
                username=data['username'],
                password=hashed,
                tg_username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
            )

    except Exception as e:
        logger.error(f"Error while creating a user: {e}")
        await message.answer(_("⚠️ An error occurred while registering. Please try again later."))
        await state.set_state(SectorStates.username)
        return

    await state.clear()
    await message.answer(_("🎉 You have successfully registered!\n\n"
                           "Now, you can use /login command to log in"))
