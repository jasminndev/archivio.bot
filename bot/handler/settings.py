import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.handler import valid_username
from bot.states import SectorStates

router_username = Router()


@router_username.message(SectorStates.settings, F.text == __("👤 Change username"))
async def change_username(message: Message, state: FSMContext):
    await state.set_state(SectorStates.change_username)
    await message.answer(_("Enter your new username"))


@router_username.message(SectorStates.change_username)
async def process_username(message: Message, state: FSMContext):
    username = message.text.strip()

    if not (3 <= len(username) <= 20):
        await message.answer(_("❌ Username must be between 3 and 20 characters."))
        return

    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        await message.answer(_("❌ Username can only contain letters, numbers, and underscores."))
        return

    data = await state.get_data()
    current_username = data.get('current_username')
    if username == current_username:
        await message.answer(_("❌ This is already your current username."))
        return

    if not await valid_username(username):
        await message.answer(_("❌ This username is already taken. Please choose another."))
        return

    await save_username(message.from_user.id, username)

    await message.answer(_("✅ Username changed successfully to {username}!").format(username=username))
    await state.set_state(SectorStates.settings)
