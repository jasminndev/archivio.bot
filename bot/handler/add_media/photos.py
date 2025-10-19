import asyncio
import logging
from collections import defaultdict

from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram_media_group import media_group_handler

from bot.buttons.navigation import add_done_keyboard, get_back_keyboard
from bot.states import SectorStates
from db.models import Photo, User

router_photo = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_locks = defaultdict(asyncio.Lock)


@router_photo.message(SectorStates.photo, F.text == __("⏬ Add"))
async def add_photo_handler(message: Message, state: FSMContext):
    await message.answer(
        text=_("📸 Please send the photos you want to save. After finishing, click the '✅ Done' button!"),
        reply_markup=add_done_keyboard())
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)
    if user:
        await state.set_state(SectorStates.add_photo)
        await state.update_data(photos=[], user_id=user.id, reminder_sent=False)
    else:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        await state.clear()


@router_photo.message(F.media_group_id, F.photo)
@media_group_handler
async def handle_media_group_photos(messages: list[Message], state: FSMContext):
    user_id = messages[0].chat.id
    async with user_locks[user_id]:
        data = await state.get_data()
        existing_photos = data.get('photos', [])
        new_photos = [msg.photo[-1].file_id for msg in messages]
        updated_photos = existing_photos + new_photos
        await state.update_data(photos=updated_photos)

        if not data.get("reminder_sent"):
            await messages[-1].answer(_("You can send more or click the '✅ Done' button!"))
            await state.update_data(reminder_sent=True)


@router_photo.message(SectorStates.add_photo, F.photo | F.forward_from, F.media_group_id == None)
async def handle_single_photo(message: Message, state: FSMContext):
    user_id = message.chat.id
    async with user_locks[user_id]:
        data = await state.get_data()
        photos = data.get('photos', [])
        # Check for direct photo
        file_id = message.photo[-1].file_id if message.photo else None
        # Check for forwarded photo, including as document
        if not file_id and message.forward_from:
            if message.document and message.document.file_id:
                mime_type = message.document.mime_type or ''
                if mime_type.startswith('image/') or 'image' in mime_type.lower():
                    file_id = message.document.file_id
        if file_id:
            updated_photos = photos + [file_id]
            await state.update_data(photos=updated_photos)

            if not data.get("reminder_sent"):
                await message.answer(_("You can send more or click the '✅ Done' button!"))
                await state.update_data(reminder_sent=True)


@router_photo.message(SectorStates.add_photo, F.text == "✅ Done")
async def handle_done_button(message: Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get("photos", [])

    if not photos:
        await message.answer(_("❗️You didn't send photos!"))
        return

    user_id = data.get("user_id")
    if not user_id:
        await message.answer(_("⚠️ User ID not found. Please start again."))
        await state.clear()
        return

    for file_id in photos:
        try:
            photo = await Photo.create(
                file_id=file_id,
                user_id=user_id,
            )
            logger.info(f"Photo saved with file_id: {file_id}, user_id: {user_id}")
        except Exception as e:
            logger.error(f"Failed to save photo with file_id: {file_id}, error: {e}")
            await message.answer(_("⚠️ An error occurred while saving a photo. Please try again."))
            return

    await state.clear()
    await message.answer(
        _("✅ All photos saved! Thank you!"),
        reply_markup=get_back_keyboard()
    )


@router_photo.message(SectorStates.add_photo)
async def not_photo_warning(message: Message):
    if not (message.photo or (
            message.forward_from and message.document and message.document.mime_type and message.document.mime_type.startswith(
        'image/')) or message.text == "✅ Done"):
        await message.answer(_("❗️Please, Send the photos or click the '✅ Done' button!"))
