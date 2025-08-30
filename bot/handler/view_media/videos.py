import logging
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.navigation import get_back_keyboard
from bot.buttons.navigation import get_view_keyboard
from bot.states import SectorStates
from db.models import Video, User

router_view_video = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router_view_video.message(SectorStates.video, F.text == __("👀 View"))
async def letters_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.view_video)
    await message.answer(_("👀 View"), reply_markup=get_view_keyboard())


@router_view_video.message(SectorStates.view_video, F.text == __("Last week"))
async def view_last_week_videos(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    one_week_ago = datetime.now() - timedelta(days=7)

    videos = await Video.filter_views(user=user, created_at__gte=one_week_ago)

    if not videos:
        await message.answer(_("📂 You don't have any saved videos from the last week."))
        return

    for video in videos:
        try:
            await message.answer_video(video.file_id)
        except Exception as e:
            logger.error(f"Failed to send video {video.file_id}: {e}")

    await message.answer(_("✅ All last week's videos have been shown."), reply_markup=get_back_keyboard())


@router_view_video.message(SectorStates.view_video, F.text == __("Last month"))
async def view_last_month_videos(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    one_month_ago = datetime.now() - timedelta(days=30)

    videos = await Video.filter_views(user=user, created_at__gte=one_month_ago)

    if not videos:
        await message.answer(_("📂 You don't have any saved videos from the last month."))
        return

    for video in videos:
        try:
            await message.answer_video(video.file_id)
        except Exception as e:
            logger.error(f"Failed to send video {video.file_id}: {e}")

    await message.answer(_("✅ All last month's videos have been shown."), reply_markup=get_back_keyboard())


@router_view_video.message(SectorStates.view_video, F.text == __("Last 6 months"))
async def view_last_six_month_videos(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    six_month_ago = datetime.now() - timedelta(weeks=24)

    videos = await Video.filter_views(user=user, created_at__gte=six_month_ago)

    if not videos:
        await message.answer(_("📂 You don't have any saved videos from the last 6 months."))
        return

    for video in videos:
        try:
            await message.answer_video(video.file_id)
        except Exception as e:
            logger.error(f"Failed to send video {video.file_id}: {e}")

    await message.answer(_("✅ All last 6 months' videos have been shown."), reply_markup=get_back_keyboard())


@router_view_video.message(SectorStates.view_video, F.text == __("All"))
async def view_all_videos(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    videos = await Video.filter(user=user)

    if not videos:
        await message.answer(_("📂 You don't have any saved videos."))
        return

    for video in videos:
        try:
            await message.answer_video(video.file_id)
        except Exception as e:
            logger.error(f"Failed to send video {video.file_id}: {e}")

    await message.answer(_("✅ All videos have been shown."), reply_markup=get_back_keyboard())
