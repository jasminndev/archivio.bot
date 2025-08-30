import logging
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.navigation import get_back_keyboard
from bot.buttons.navigation import get_view_keyboard
from bot.states import SectorStates
from db.models import Photo, User

router_view_photo = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router_view_photo.message(SectorStates.photo, F.text == __("👀 View"))
async def letters_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.view_photo)
    await message.answer(_("👀 View"), reply_markup=get_view_keyboard())


@router_view_photo.message(SectorStates.view_photo, F.text == __("Last week"))
async def view_last_week_photos(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    one_week_ago = datetime.now() - timedelta(days=7)

    photos = await Photo.filter_views(user=user, created_at__gte=one_week_ago)

    if not photos:
        await message.answer(_("📂 You don't have any saved photos from the last week."))
        return

    for photo in photos:
        try:
            await message.answer_photo(photo.file_id)
        except Exception as e:
            logger.error(f"Failed to send photo {photo.file_id}: {e}")

    await message.answer(_("✅ All last week's photos have been shown."), reply_markup=get_back_keyboard())


@router_view_photo.message(SectorStates.view_photo, F.text == __("Last month"))
async def view_last_month_photos(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    one_month_ago = datetime.now() - timedelta(days=30)

    photos = await Photo.filter_views(user=user, created_at__gte=one_month_ago)

    if not photos:
        await message.answer(_("📂 You don't have any saved photos from the last month."))
        return

    for photo in photos:
        try:
            await message.answer_photo(photo.file_id)
        except Exception as e:
            logger.error(f"Failed to send photo {photo.file_id}: {e}")

    await message.answer(_("✅ All last month's photos have been shown."), reply_markup=get_back_keyboard())


@router_view_photo.message(SectorStates.view_photo, F.text == __("Last 6 months"))
async def view_last_six_month_photos(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    six_month_ago = datetime.now() - timedelta(weeks=24)

    photos = await Photo.filter_views(user=user, created_at__gte=six_month_ago)

    if not photos:
        await message.answer(_("📂 You don't have any saved photos from the last 6 months."))
        return

    for photo in photos:
        try:
            await message.answer_photo(photo.file_id)
        except Exception as e:
            logger.error(f"Failed to send photo {photo.file_id}: {e}")

    await message.answer(_("✅ All last 6 months' photos have been shown."), reply_markup=get_back_keyboard())


@router_view_photo.message(SectorStates.view_photo, F.text == __("All"))
async def view_all_photos(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    photos = await Photo.filter(user=user)

    if not photos:
        await message.answer(_("📂 You don't have any saved photos."))
        return

    for photo in photos:
        try:
            await message.answer_photo(photo.file_id)
        except Exception as e:
            logger.error(f"Failed to send photo {photo.file_id}: {e}")

    await message.answer(_("✅ All photos have been shown."), reply_markup=get_back_keyboard())
