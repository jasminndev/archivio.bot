from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.functions import hash_password
from bot.handler import valid_password
from bot.states import SectorStates
from db.models import User

router_password = Router()


@router_password.message(SectorStates.settings, F.text == __("🔢 Change password"))
async def change_password(message: Message, state: FSMContext):
    await state.set_state(SectorStates.change_password)
    await message.answer(_("Enter your new password."))


@router_password.message(SectorStates.change_password)
async def process_password(message: Message, state: FSMContext):
    password = message.text.strip()

    if not await valid_password(password):
        await message.answer(
            _("❌ Password must be at least 6 characters long and contain both letters and numbers. Please create another."))
        return

    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please register first."))
        await state.clear()
        return

    hashed = await hash_password(password)
    await User.update(_id=user.id, password=hashed)

    await state.clear()
    await message.answer(_("🔄 Password successfully changed."))
