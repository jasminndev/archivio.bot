import logging
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.states import SectorStates
from db.models import User

router_logout = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router_logout.message(SectorStates.settings, F.text == __("🚫 Logout"))
async def logout(message: Message, state: FSMContext):
    tg_id = str(message.from_user.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        await state.clear()
        return

    try:
        await User.update(_id=user.id, logged_in=False)
        logger.info(f"User logged out: tg_id={tg_id}")
    except Exception as e:
        logger.error(f"Failed to log out user with tg_id={tg_id}, error: {e}")
        await message.answer(_("⚠️ An error occurred while logging out. Please try again."))
        return

    await message.answer(
        _("✅ You have been logged out. Use /login to log in again."),
    )