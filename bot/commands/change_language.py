from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.buttons.constants import languages, map_lang
from bot.dispatcher import dp, i18n
from bot.states import LanguageStates

router = Router()
dp.include_router(router)


@router.message(Command(commands="change_language"))
async def show_language_selection(message: Message, state: FSMContext) -> None:
    keyboard = InlineKeyboardBuilder()
    for text, callback in languages:
        keyboard.add(
            InlineKeyboardButton(text=text, callback_data=callback)
        )
    keyboard.adjust(2)
    await state.set_state(LanguageStates.lang)
    await message.answer(text="Iltimos, tilni tanlang.", reply_markup=keyboard.as_markup())


@router.callback_query(F.data.startswith("lang"))
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

        keyboard = ReplyKeyboardBuilder()
        keyboard.add(KeyboardButton(text=_("🏠 Main menu")))
        markup = keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)

        await callback.message.answer(_("✅ Language changed."), reply_markup=markup)

    else:
        await callback.message.delete()
        await show_language_selection(callback.message, state)
        await callback.answer(_("Unknown language selection"), show_alert=True)
