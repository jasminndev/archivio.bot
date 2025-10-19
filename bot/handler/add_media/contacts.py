import asyncio
import logging
from collections import defaultdict

from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.navigation import add_done_keyboard, get_back_keyboard
from bot.states import SectorStates
from db.models import User, Contact

router_contact = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_locks = defaultdict(asyncio.Lock)


@router_contact.message(SectorStates.contact, F.text == __("⏬ Add"))
async def add_contact_handler(message: Message, state: FSMContext):
    await message.answer(
        text=_("📸 Please send the contacts you want to save. After finishing, click the '✅ Done' button!"),
        reply_markup=add_done_keyboard())
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)
    if user:
        await state.set_state(SectorStates.add_contact)
        await state.update_data(contacts=[], user_id=user.id, reminder_sent=False)
    else:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        await state.clear()


@router_contact.message(SectorStates.add_contact, F.contact, F.media_group_id == None)
async def handle_contact(message: Message, state: FSMContext):
    user_id = message.chat.id
    async with user_locks[user_id]:
        data = await state.get_data()
        contacts = data.get("contacts", [])
        # Validate and create contact data
        contact_data = {
            "phone_number": message.contact.phone_number or "",
            "first_name": message.contact.first_name or "",
            "last_name": message.contact.last_name or "",
        }
        contacts.append(contact_data)
        await state.update_data(contacts=contacts)

        if not data.get("reminder_sent"):
            await message.answer(_("✅ You can send more or click the '✅ Done' button!"))
            await state.update_data(reminder_sent=True)


@router_contact.message(SectorStates.add_contact, F.text == "✅ Done")
async def handle_done_button(message: Message, state: FSMContext):
    data = await state.get_data()
    contacts = data.get("contacts", [])

    if not contacts:
        await message.answer(_("❗️You didn't send contacts!"))
        return

    user_id = data.get("user_id")
    if not user_id:
        await message.answer(_("⚠️ User ID not found. Please start again."))
        await state.clear()
        return

    for contact in contacts:
        try:
            await Contact.create(
                user_id=user_id,
                phone_number=contact["phone_number"],
                first_name=contact["first_name"],
                last_name=contact["last_name"],
            )
            logger.info(f"Contact saved with details: {contact}, user_id: {user_id}")
        except Exception as e:
            logger.error(f"Failed to save contact with details: {contact}, error: {e}")
            await message.answer(_("⚠️ An error occurred while saving a contact. Please try again."))
            return

    await state.clear()
    await message.answer(
        _("✅ All contacts saved! Thank you!"),
        reply_markup=get_back_keyboard()
    )


@router_contact.message(SectorStates.add_contact)
async def not_contact_warning(message: Message):
    if not (message.contact or message.text == "✅ Done"):
        await message.answer(_("❗️Please, Send the contacts or click the '✅ Done' button!"))
