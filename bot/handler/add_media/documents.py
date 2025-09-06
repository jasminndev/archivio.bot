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
from db.models import User, Document

router_document = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_locks = defaultdict(asyncio.Lock)


@router_document.message(SectorStates.document, F.text == __("⏬ Add"))
async def add_document_handler(message: Message, state: FSMContext):
    await message.answer(
        text=_("📸 Please send the documents you want to save. After finishing, click the '✅ Done' button!"),
        reply_markup=add_done_keyboard())
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)
    if user:
        await state.set_state(SectorStates.add_document)
        await state.update_data(documents=[], user_id=user.id, reminder_sent=False)
    else:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        await state.clear()


@router_document.message(F.media_group_id, F.document)
@media_group_handler
async def handle_media_group_documents(messages: list[Message], state: FSMContext):
    user_id = messages[0].chat.id
    async with user_locks[user_id]:
        data = await state.get_data()
        existing_documents = data.get('documents', [])
        new_documents = [msg.document.file_id for msg in messages]
        updated_documents = existing_documents + new_documents
        await state.update_data(documents=updated_documents)

        if not data.get("reminder_sent"):
            await messages[-1].answer(_("After finishing, click the '✅ Done' button!"))
            await state.update_data(reminder_sent=True)


@router_document.message(SectorStates.add_document, F.document, F.media_group_id == None)
async def handle_single_document(message: Message, state: FSMContext):
    user_id = message.chat.id
    async with user_locks[user_id]:
        data = await state.get_data()
        documents = data.get('documents', [])
        file_id = message.document.file_id
        updated_documents = documents + [file_id]
        await state.update_data(documents=updated_documents)

        if not data.get("reminder_sent"):
            await message.answer(_("You can send more or click the '✅ Done' button!"))
            await state.update_data(reminder_sent=True)


@router_document.message(SectorStates.add_document, F.text == "✅ Done")
async def handle_done_button(message: Message, state: FSMContext):
    data = await state.get_data()
    documents = data.get("documents", [])

    if not documents:
        await message.answer(_("❗️You didn't send documents!"))
        return

    user_id = data.get("user_id")
    if not user_id:
        await message.answer(_("⚠️ User ID not found. Please start again."))
        await state.clear()
        return

    for file_id in documents:
        try:
            await Document.create(file_id=file_id, user_id=user_id)
            logger.info(f"Document saved with file_id: {file_id}, user_id: {user_id}")
        except Exception as e:
            logger.error(f"Failed to save document with file_id: {file_id}, error: {e}")
            await message.answer(_("⚠️ An error occurred while saving a document. Please try again."))
            return

    await state.clear()
    await message.answer(
        _("✅ All documents saved! Thank you!"),
        reply_markup=get_back_keyboard()
    )


@router_document.message(SectorStates.add_document)
async def not_document_warning(message: Message):
    await message.answer("❗️Please, Send the documents or click the '✅ Done' button!")
