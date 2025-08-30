import logging
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.navigation import get_back_keyboard
from bot.buttons.navigation import get_view_keyboard
from bot.states import SectorStates
from db.models import Contact, User

router_view_contact = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router_view_contact.message(SectorStates.contact, F.text == __("👀 View"))
async def letters_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.view_contact)
    await message.answer(_("👀 View"), reply_markup=get_view_keyboard())


@router_view_contact.message(SectorStates.view_contact, F.text == __("Last week"))
async def view_last_week_contacts(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    one_week_ago = datetime.now() - timedelta(days=7)

    contacts = await Contact.filter_views(user=user, created_at__gte=one_week_ago)

    if not contacts:
        await message.answer(_("📂 You don't have any saved contacts from the last week."))
        return

    for contact in contacts:
        try:
            await message.answer_contact(
                phone_number=contact.phone_number,
                first_name=contact.first_name or "",
                last_name=contact.last_name or ""
            )
        except Exception as e:
            logger.error(f"Failed to send contact {contact.id}: {e}")

    await message.answer(
        _("✅ All last week's contacts have been shown."),
        reply_markup=get_back_keyboard()
    )


@router_view_contact.message(SectorStates.view_contact, F.text == __("Last month"))
async def view_last_month_contacts(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    one_month_ago = datetime.now() - timedelta(days=30)

    contacts = await Contact.filter_views(user=user, created_at__gte=one_month_ago)

    if not contacts:
        await message.answer(_("📂 You don't have any saved contacts from the last month."))
        return

    for contact in contacts:
        try:
            await message.answer_contact(
                phone_number=contact.phone_number,
                first_name=contact.first_name or "",
                last_name=contact.last_name or ""
            )
        except Exception as e:
            logger.error(f"Failed to send contact {contact.id}: {e}")

    await message.answer(
        _("✅ All last week's contacts have been shown."),
        reply_markup=get_back_keyboard()
    )


@router_view_contact.message(SectorStates.view_contact, F.text == __("Last 6 months"))
async def view_last_six_month_contacts(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    six_month_ago = datetime.now() - timedelta(weeks=24)

    contacts = await Contact.filter_views(user=user, created_at__gte=six_month_ago)

    if not contacts:
        await message.answer(_("📂 You don't have any saved contacts from the last 6 months."))
        return

    for contact in contacts:
        try:
            await message.answer_contact(
                phone_number=contact.phone_number,
                first_name=contact.first_name or "",
                last_name=contact.last_name or ""
            )
        except Exception as e:
            logger.error(f"Failed to send contact {contact.id}: {e}")

    await message.answer(
        _("✅ All last week's contacts have been shown."),
        reply_markup=get_back_keyboard()
    )


@router_view_contact.message(SectorStates.view_contact, F.text == __("All"))
async def view_all_contacts(message: Message):
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)

    if not user:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        return

    contacts = await Contact.filter(user=user)

    if not contacts:
        await message.answer(_("📂 You don't have any saved contacts."))
        return

    for contact in contacts:
        try:
            await message.answer_contact(
                phone_number=contact.phone_number,
                first_name=contact.first_name or "",
                last_name=contact.last_name or ""
            )
        except Exception as e:
            logger.error(f"Failed to send contact {contact.id}: {e}")

    await message.answer(
        _("✅ All last week's contacts have been shown."),
        reply_markup=get_back_keyboard()
    )
