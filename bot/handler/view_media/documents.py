import logging
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.navigation import get_back_keyboard
from bot.buttons.navigation import get_view_keyboard
from bot.states import SectorStates
from db.models import Document, User

router_view_document = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router_view_document.message(SectorStates.document, F.text == __("👀 View"))
async def letters_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.view_document)
    await message.answer(_("👀 View"), reply_markup=get_view_keyboard())


@router_view_document.message(SectorStates.view_document, F.text == __("Last week"))
async def view_last_week_documents(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    one_week_ago = datetime.now() - timedelta(days=7)

    documents = await Document.filter_views(user=user, created_at__gte=one_week_ago)

    if not documents:
        await message.answer(_("📂 You don't have any saved documents from the last week."))
        return

    for document in documents:
        try:
            await message.answer_document(document.file_id)
        except Exception as e:
            logger.error(f"Failed to send document {document.file_id}: {e}")

    await message.answer(_("✅ All last week's documents have been shown."), reply_markup=get_back_keyboard())


@router_view_document.message(SectorStates.view_document, F.text == __("Last month"))
async def view_last_month_documents(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    one_month_ago = datetime.now() - timedelta(days=30)

    documents = await Document.filter_views(user=user, created_at__gte=one_month_ago)

    if not documents:
        await message.answer(_("📂 You don't have any saved documents from the last month."))
        return

    for document in documents:
        try:
            await message.answer_document(document.file_id)
        except Exception as e:
            logger.error(f"Failed to send document {document.file_id}: {e}")

    await message.answer(_("✅ All last month's documents have been shown."), reply_markup=get_back_keyboard())


@router_view_document.message(SectorStates.view_document, F.text == __("Last 6 months"))
async def view_last_six_month_documents(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    six_month_ago = datetime.now() - timedelta(weeks=24)

    documents = await Document.filter_views(user=user, created_at__gte=six_month_ago)

    if not documents:
        await message.answer(_("📂 You don't have any saved documents from the last 6 months."))
        return

    for document in documents:
        try:
            await message.answer_document(document.file_id)
        except Exception as e:
            logger.error(f"Failed to send document {document.file_id}: {e}")

    await message.answer(_("✅ All last 6 months' documents have been shown."), reply_markup=get_back_keyboard())


@router_view_document.message(SectorStates.view_document, F.text == __("All"))
async def view_all_documents(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    documents = await Document.filter(user=user)

    if not documents:
        await message.answer(_("📂 You don't have any saved documents."))
        return

    for document in documents:
        try:
            await message.answer_document(document.file_id)
        except Exception as e:
            logger.error(f"Failed to send document {document.file_id}: {e}")

    await message.answer(_("✅ All documents have been shown."), reply_markup=get_back_keyboard())
