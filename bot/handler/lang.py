import logging

from aiogram import html, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.buttons.constants import languages, map_lang
from bot.dispatcher import dp, i18n
from bot.states import LanguageStates, SectorStates
from db.models import User

logger = logging.getLogger(__name__)


async def show_language_selection(message: Message, state: FSMContext) -> None:
    keyboard = InlineKeyboardBuilder()
    for text, callback in languages:
        keyboard.add(
            InlineKeyboardButton(text=text, callback_data=callback)
        )
    keyboard.adjust(2)
    await state.set_state(LanguageStates.lang)
    await message.answer(text=_("🌐 Please choose a language:"), reply_markup=keyboard.as_markup())


@dp.message(Command(commands=["start"]))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await show_language_selection(message, state)
    tg_id = str(message.chat.id)
    user = await User.filter_one(tg_id=tg_id)
    if not user:
        await User.create(
            tg_id=tg_id,
            tg_username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )


@dp.callback_query(LanguageStates.lang, F.data.startswith("lang"))
async def lang_selected_handler(callback: CallbackQuery, state: FSMContext):
    if callback.data == "lang_":
        await callback.message.delete()
        await show_language_selection(callback.message, state)
        await callback.answer()
        return

    code = map_lang.get(callback.data)
    if code:
        await state.update_data(locale=code)
        i18n.ctx_locale.set(code)

        tg_id = str(callback.from_user.id)
        user = await User.filter_one(tg_id=tg_id)
        if user:
            await User.update(_id=user.id, locale=code)

        text = _(
            "🤖 Welcome, {full_name}!\n\n"
            "In this bot, you can store photos, videos, and documents, and even write letters that only you can read.\n\n"
            "Use the following commands to use the service:\n\n"
            "🔹 /register — to register\n"
            "🔹 /login — to login\n\n"
            "Use the /help command to get assistance."
        ).format(full_name=html.bold(callback.from_user.full_name))
        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text=_("🔄 Change the language"), callback_data="lang_"),
        )
        keyboard.adjust(1)

        await callback.message.edit_text(text=text, reply_markup=keyboard.as_markup())
        await state.set_state(SectorStates.main_menu)
    else:
        await callback.message.delete()
        await show_language_selection(callback.message, state)
        await callback.answer(_("Unknown language selection"), show_alert=True)
