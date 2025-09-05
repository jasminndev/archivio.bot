from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.states import SectorStates
from db.models import User

router_logout = Router()


@router_logout.message(SectorStates.settings, F.text == __("🚪 Logout"))
async def logout(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)
    user = await User.filter_one(tg_id=tg_id)

    if user:
        await User.update(_id=user.id, logged_in=False)

    await state.clear()
    await message.answer(_("✅ You have been logged out. Use /login to log in again."))
