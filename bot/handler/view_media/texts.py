import logging
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.navigation import get_back_keyboard
from bot.buttons.navigation import get_view_keyboard
from bot.states import SectorStates
from db.models import TextMessage, User

router_view_text_message = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router_view_text_message.message(SectorStates.text_message, F.text == __("👀 View"))
async def letters_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.view_text_message)
    await message.answer(_("👀 View"), reply_markup=get_view_keyboard())


@router_view_text_message.message(SectorStates.view_text_message, F.text == __("Last week"))
async def view_last_week_text_messages(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    one_week_ago = datetime.now() - timedelta(days=7)

    text_messages = await TextMessage.filter_views(user=user, created_at__gte=one_week_ago)

    if not text_messages:
        await message.answer(_("📂 You don't have any saved text messages from the last week."))
        return

    for text_message in text_messages:
        try:
            await message.answer(text_message.content)
        except Exception as e:
            logger.error(f"Failed to send text_message {text_message.content}: {e}")

    await message.answer(_("✅ All last week's text messages have been shown."), reply_markup=get_back_keyboard())


@router_view_text_message.message(SectorStates.view_text_message, F.text == __("Last month"))
async def view_last_month_text_messages(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    one_month_ago = datetime.now() - timedelta(days=30)

    text_messages = await TextMessage.filter_views(user=user, created_at__gte=one_month_ago)

    if not text_messages:
        await message.answer(_("📂 You don't have any saved text messages from the last month."))
        return

    for text_message in text_messages:
        try:
            await message.answer(text_message.content)
        except Exception as e:
            logger.error(f"Failed to send text_message {text_message.content}: {e}")

    await message.answer(_("✅ All last month's text messages have been shown."), reply_markup=get_back_keyboard())


@router_view_text_message.message(SectorStates.view_text_message, F.text == __("Last 6 months"))
async def view_last_six_month_text_messages(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    six_month_ago = datetime.now() - timedelta(weeks=24)

    text_messages = await TextMessage.filter_views(user=user, created_at__gte=six_month_ago)

    if not text_messages:
        await message.answer(_("📂 You don't have any saved text messages from the last 6 months."))
        return

    for text_message in text_messages:
        try:
            await message.answer(text_message.content)
        except Exception as e:
            logger.error(f"Failed to send text_message {text_message.content}: {e}")

    await message.answer(_("✅ All last 6 months' text messages have been shown."), reply_markup=get_back_keyboard())


@router_view_text_message.message(SectorStates.view_text_message, F.text == __("All"))
async def view_all_text_messages(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    text_messages = await TextMessage.filter(user=user)

    if not text_messages:
        await message.answer(_("📂 You don't have any saved text messages."))
        return

    for text_message in text_messages:
        try:
            await message.answer(text_message.content)
        except Exception as e:
            logger.error(f"Failed to send text_message {text_message.content}: {e}")

    await message.answer(_("✅ All text messages have been shown."), reply_markup=get_back_keyboard())
