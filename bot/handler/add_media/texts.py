import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.navigation import add_done_keyboard, get_back_keyboard
from bot.states import SectorStates
from db.models import User, TextMessage

router_text_message = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router_text_message.message(SectorStates.text_message, F.text == __("⏬ Add"))
async def add_text_message_handler(message: Message, state: FSMContext):
    await message.answer(
        text=_("📝 Please send the text messages you want to save. After finishing, click the '✅ Done' button!"),
        reply_markup=add_done_keyboard()
    )
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)
    if user:
        await state.set_state(SectorStates.add_text_message)
        await state.update_data(text_messages=[], user_id=user.id)
    else:
        await message.answer(_("⚠️ User not found. Please start with /start first."))
        await state.clear()


@router_text_message.message(SectorStates.add_text_message, F.text & (F.text != "✅ Done"))
async def handle_single_text_message(message: Message, state: FSMContext):
    text_content = message.text

    data = await state.get_data()
    text_messages = data.get('text_messages', [])
    text_messages.append(text_content)
    await state.update_data(text_messages=text_messages)

    await message.answer(
        _("✅ You can send more or click the '✅ Done' button!")
    )


@router_text_message.message(SectorStates.add_text_message, F.text == "✅ Done")
async def handle_done_button(message: Message, state: FSMContext):
    data = await state.get_data()
    text_messages = data.get("text_messages", [])

    if not text_messages:
        await message.answer(_("❗️You didn't send any text messages!"))
        return

    user_id = data.get("user_id")
    if not user_id:
        await message.answer(_("⚠️ User ID not found. Please start again."))
        await state.clear()
        return

    for content in text_messages:
        try:
            await TextMessage.create(
                user_id=user_id,
                content=content,
            )
            logger.info(f"Text message saved: {content}, user_id: {user_id}")
        except Exception as e:
            logger.error(f"Failed to save text message '{content}', error: {e}")
            await message.answer(_("⚠️ An error occurred while saving a text message. Please try again."))
            return

    await state.clear()
    await message.answer(
        _("✅ All text messages saved! Thank you!"),
        reply_markup=get_back_keyboard()
    )


@router_text_message.message(SectorStates.add_text_message)
async def not_text_message_warning(message: Message):
    await message.answer(_("❗️Please send text messages or click the '✅ Done' button!"))
