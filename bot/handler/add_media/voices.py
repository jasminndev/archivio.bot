import asyncio
import logging
from collections import defaultdict

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram_media_group import media_group_handler

from bot.buttons.navigation import add_done_keyboard, get_back_keyboard
from bot.states import SectorStates
from db.models import User, Voice

router_voice = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_locks = defaultdict(asyncio.Lock)


@router_voice.message(SectorStates.voice, F.text == __("⏬ Add"))
async def add_voice_handler(message: Message, state: FSMContext):
    await message.answer(
        text=_("🎙️ Please send the voice messages you want to save. After finishing, click the '✅ Done' button!"),
        reply_markup=add_done_keyboard()
    )
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)
    if user:
        await state.set_state(SectorStates.add_voice)
        await state.update_data(voices=[], user_id=user.id, reminder_sent=False)
    else:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        await state.clear()


@router_voice.message(SectorStates.add_voice, F.media_group_id, F.voice)
@media_group_handler
async def handle_media_group_voices(messages: list[Message], state: FSMContext):
    user_id = messages[0].chat.id
    async with user_locks[user_id]:
        new_voices = [msg.voice.file_id for msg in messages]
        data = await state.get_data()
        existing_voices = data.get('voices', [])
        await state.update_data(voices=existing_voices + new_voices)

        if not data.get("reminder_sent"):
            await messages[-1].answer(
                _("✅ You can send more or click the '✅ Done' button!")
            )
            await state.update_data(reminder_sent=True)


@router_voice.message(SectorStates.add_voice, F.voice, F.media_group_id == None)
async def handle_single_voice(message: Message, state: FSMContext):
    user_id = message.chat.id
    async with user_locks[user_id]:
        file_id = message.voice.file_id
        data = await state.get_data()
        voices = data.get('voices', [])
        voices.append(file_id)
        await state.update_data(voices=voices)

        if not data.get("reminder_sent"):
            await message.answer(
                _("✅ You can send more or click the '✅ Done' button!")
            )
            await state.update_data(reminder_sent=True)


@router_voice.message(SectorStates.add_voice, F.text == "✅ Done")
async def handle_done_button(message: Message, state: FSMContext):
    data = await state.get_data()
    voices = data.get("voices", [])

    if not voices:
        await message.answer(_("❗️You didn't send any voice messages!"))
        return

    user_id = data.get("user_id")
    if not user_id:
        await message.answer(_("⚠️ User ID not found. Please start again."))
        await state.clear()
        return

    async with user_locks[message.chat.id]:
        for file_id in voices:
            try:
                await Voice.create(
                    file_id=file_id,
                    user_id=user_id,
                )
                logger.info(f"Voice saved with file_id: {file_id}, user_id: {user_id}")
            except Exception as e:
                logger.error(f"Failed to save voice with file_id: {file_id}, error: {e}")
                await message.answer(_("⚠️ An error occurred while saving a voice message. Please try again."))
                return

    await state.clear()
    await message.answer(
        _("✅ All voice messages saved! Thank you!"),
        reply_markup=get_back_keyboard()
    )


@router_voice.message(SectorStates.add_voice)
async def not_voice_warning(message: Message):
    if not (message.voice or message.text == "✅ Done"):
        await message.answer(_("❗️Please send voice messages or click the '✅ Done' button!"))
