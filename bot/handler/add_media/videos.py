import logging

from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram_media_group import media_group_handler

from bot.buttons.navigation import add_done_keyboard, get_back_keyboard
from bot.states import SectorStates
from db.models import User, Video

router = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.message(SectorStates.video, F.text == __("⏬ Add"))
async def add_video_handler(message: Message, state: FSMContext):
    logger.info(f"add_video_handler triggered for user {message.chat.id}")
    await message.answer(
        text=_("📸 Please send the videos you want to save. After finishing, click the '✅ Done' button!"),
        reply_markup=add_done_keyboard())
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)
    if user:
        await state.set_state(SectorStates.add_video)
        await state.update_data(videos=[], user_id=user.id)
    else:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        await state.clear()


@router.message(SectorStates.video)
async def log_video_state(message: Message, state: FSMContext):
    logger.info(f"Received message in SectorStates.video: {message.text}, state: {await state.get_state()}")


@router.message(F.media_group_id, F.video)
@media_group_handler
async def handle_media_group_videos(messages: list[Message], state: FSMContext):
    new_videos = [msg.video.file_id for msg in messages]

    data = await state.get_data()
    existing_videos = data.get('videos', [])
    await state.update_data(videos=existing_videos + new_videos)

    await messages[-1].answer(
        _("Videos saved. After finishing, click the '✅ Done' button!")
    )


@router.message(SectorStates.add_video, F.video, F.media_group_id is None)
async def handle_single_video(message: Message, state: FSMContext):
    file_id = message.video.file_id
    data = await state.get_data()
    videos = data.get('videos', [])
    videos.append(file_id)
    await state.update_data(videos=videos)

    await message.answer(
        _("✅ Video saved! You can send more or click the '✅ Done' button!")
    )


@router.message(SectorStates.add_video, F.text == "✅ Done")
async def handle_done_button(message: Message, state: FSMContext):
    data = await state.get_data()
    videos = data.get("videos", [])

    if not videos:
        await message.answer(_("❗️You didn't send videos!"))
        return

    user_id = data.get("user_id")
    if not user_id:
        await message.answer(_("⚠️ User ID not found. Please start again."))
        await state.clear()
        return

    for file_id in videos:
        try:
            video = await Video.create(
                file_id=file_id,
                user_id=user_id,
            )
            logger.info(f"Video saved with file_id: {file_id}, user_id: {user_id}")
        except Exception as e:
            logger.error(f"Failed to save video with file_id: {file_id}, error: {e}")
            await message.answer(_("⚠️ An error occurred while saving a video. Please try again."))
            return

    await state.clear()
    await message.answer(
        _("✅ All videos saved! Thank you!"),
        reply_markup=get_back_keyboard()
    )


@router.message(SectorStates.add_video)
async def not_video_warning(message: Message):
    await message.answer("❗️Please, Send the videos or click the '✅ Done' button!")
