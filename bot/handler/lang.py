from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram import html, F
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.dispatcher import dp
from bot.states import SectorStates



@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    ikb = InlineKeyboardBuilder()
    ikb.add(
        InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="lang_de"),
        InlineKeyboardButton(text="🇺🇿 O'zbek" , callback_data="lang_uz")
    )
    ikb.adjust(2,2)
    await state.set_state(SectorStates.language)
    await message.answer(text=f"Choose the language.", reply_markup=ikb.as_markup())

@dp.callback_query(F.data.startswith("lang"))
async def lang_selected_handler(callback: CallbackQuery, state: FSMContext, i18n):
    map_lang = {
        "lang_en" : 'en',
        "lang_ru" : 'ru',
        "lang_de" : 'de',
        "lang_uz" : 'uz'
    }
    code = map_lang.get(callback.data)
    await state.update_data({"locale" : code})
    i18n.current_locale = code
    text = (_(
        f"🤖 Welcome, {html.bold(callback.from_user.full_name)}!\n\n"
        "In this bot, you can store photos, videos, and documents, and even write letters that only you can read.\n\n"
        "Use the following commands to use the service:\n\n"
        "🔹 /register — to register\n"
        "🔹 /login — to login\n\n"
        "Use the /help command to get assistance."
    ))
    await callback.message.edit_text(text)
