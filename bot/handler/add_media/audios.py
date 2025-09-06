import logging

from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram_media_group import media_group_handler

from bot.buttons.navigation import add_done_keyboard, get_back_keyboard
from bot.states import SectorStates
from db.models import User, Audio

router_audio = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router_audio.message(SectorStates.audio, F.text == __("⏬ Add"))
async def add_audio_handler(message: Message, state: FSMContext):
    await message.answer(
        text=_("📸 Please send the audios you want to save. After finishing, click the '✅ Done' button!"),
        reply_markup=add_done_keyboard())
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)
    if user:
        await state.set_state(SectorStates.add_audio)
        await state.update_data(audios=[], user_id=user.id)
    else:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        await state.clear()


@router_audio.message(F.media_group_id, F.audio)
@media_group_handler
async def handle_media_group_audios(messages: list[Message], state: FSMContext):
    new_audios = [msg.audio.file_id for msg in messages]

    data = await state.get_data()
    existing_audios = data.get('audios', [])
    await state.update_data(audios=existing_audios + new_audios)

    await messages[-1].answer(
        _("After finishing, click the '✅ Done' button!")
    )


@router_audio.message(SectorStates.add_audio, F.audio, F.media_group_id == None)
async def handle_single_audio(message: Message, state: FSMContext):
    file_id = message.audio.file_id
    data = await state.get_data()
    audios = data.get('audios', [])
    audios.append(file_id)
    await state.update_data(audios=audios)

    await message.answer(
        _("✅ Audio saved! You can send more or click the '✅ Done' button!")
    )


@router_audio.message(SectorStates.add_audio, F.text == "✅ Done")
async def handle_done_button(message: Message, state: FSMContext):
    data = await state.get_data()
    audios = data.get("audios", [])

    if not audios:
        await message.answer(_("❗️You didn't send audios!"))
        return

    user_id = data.get("user_id")
    if not user_id:
        await message.answer(_("⚠️ User ID not found. Please start again."))
        await state.clear()
        return

    for file_id in audios:
        try:
            audio = await Audio.create(
                file_id=file_id,
                user_id=user_id,
            )
            logger.info(f"Audio saved with file_id: {file_id}, user_id: {user_id}")
        except Exception as e:
            logger.error(f"Failed to save audio with file_id: {file_id}, error: {e}")
            await message.answer(_("⚠️ An error occurred while saving a audio. Please try again."))
            return

    await state.clear()
    await message.answer(
        _("✅ All audios saved! Thank you!"),
        reply_markup=get_back_keyboard()
    )


@router_audio.message(SectorStates.add_audio)
async def not_audio_warning(message: Message):
    await message.answer("❗️Please, Send the audios or click the '✅ Done' button!")
