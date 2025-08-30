import logging
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.navigation import get_back_keyboard
from bot.buttons.navigation import get_view_keyboard
from bot.states import SectorStates
from db.models import Audio, User

router_view_audio = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router_view_audio.message(SectorStates.audio, F.text == __("👀 View"))
async def letters_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.view_audio)
    await message.answer(_("👀 View"), reply_markup=get_view_keyboard())


@router_view_audio.message(SectorStates.view_audio, F.text == __("Last week"))
async def view_last_week_audios(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    one_week_ago = datetime.now() - timedelta(days=7)

    audios = await Audio.filter_views(user=user, created_at__gte=one_week_ago)

    if not audios:
        await message.answer(_("📂 You don't have any saved audios from the last week."))
        return

    for audio in audios:
        try:
            await message.answer_audio(audio.file_id)
        except Exception as e:
            logger.error(f"Failed to send audio {audio.file_id}: {e}")

    await message.answer(_("✅ All last week's audios have been shown."), reply_markup=get_back_keyboard())


@router_view_audio.message(SectorStates.view_audio, F.text == __("Last month"))
async def view_last_month_audios(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    one_month_ago = datetime.now() - timedelta(days=30)

    audios = await Audio.filter_views(user=user, created_at__gte=one_month_ago)

    if not audios:
        await message.answer(_("📂 You don't have any saved audios from the last month."))
        return

    for audio in audios:
        try:
            await message.answer_audio(audio.file_id)
        except Exception as e:
            logger.error(f"Failed to send audio {audio.file_id}: {e}")

    await message.answer(_("✅ All last month's audios have been shown."), reply_markup=get_back_keyboard())


@router_view_audio.message(SectorStates.view_audio, F.text == __("Last 6 months"))
async def view_last_six_month_audios(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    six_month_ago = datetime.now() - timedelta(weeks=24)

    audios = await Audio.filter_views(user=user, created_at__gte=six_month_ago)

    if not audios:
        await message.answer(_("📂 You don't have any saved audios from the last 6 months."))
        return

    for audio in audios:
        try:
            await message.answer_audio(audio.file_id)
        except Exception as e:
            logger.error(f"Failed to send audio {audio.file_id}: {e}")

    await message.answer(_("✅ All last 6 months' audios have been shown."), reply_markup=get_back_keyboard())


@router_view_audio.message(SectorStates.view_audio, F.text == __("All"))
async def view_all_audios(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    audios = await Audio.filter(user=user)

    if not audios:
        await message.answer(_("📂 You don't have any saved audios."))
        return

    for audio in audios:
        try:
            await message.answer_audio(audio.file_id)
        except Exception as e:
            logger.error(f"Failed to send audio {audio.file_id}: {e}")

    await message.answer(_("✅ All audios have been shown."), reply_markup=get_back_keyboard())
