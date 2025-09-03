from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.navigation import get_back_keyboard
from bot.handler import valid_username
from bot.states import SectorStates
from db.models import User

router_username = Router()


@router_username.message(SectorStates.settings, F.text == __("👤 Change username"))
async def change_username(message: Message, state: FSMContext):
    await state.set_state(SectorStates.change_username)
    await message.answer(_("Enter your new username"))


@router_username.message(SectorStates.change_username)
async def process_username(message: Message, state: FSMContext):
    username = message.text.strip()
    tg_id = str(message.from_user.id)

    current_user = await User.get(tg_id=tg_id)
    if not current_user:
        await message.answer(_("❌ User not found. Please contact support."))
        return

    if username == current_user.username:
        await message.answer(_("❌ This is already your current username."))
        return

    if not await valid_username(username):
        await message.answer(
            _("❌ Username is invalid or already taken. "
              "It must be 3–20 characters, contain only letters, numbers, and underscores.")
        )
        return

    await User.update(current_user.id, username=username.lower())

    await message.answer(_("✅ Username changed successfully to {username}!").format(username=username),
                         reply_markup=get_back_keyboard())
    await state.set_state(SectorStates.settings)
