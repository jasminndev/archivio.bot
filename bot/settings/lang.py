from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.buttons.constants import languages, map_lang
from bot.dispatcher import i18n
from bot.states import SectorStates
from db.models import User

router_language = Router()


async def show_language_selection(message: Message, state: FSMContext) -> None:
    keyboard = InlineKeyboardBuilder()
    for text, callback in languages:
        keyboard.add(InlineKeyboardButton(text=text, callback_data=callback))
    keyboard.adjust(2)

    await state.set_state(SectorStates.change_language)
    await message.answer(text=_("🌐 Please choose a language:"), reply_markup=keyboard.as_markup())


@router_language.message(SectorStates.settings, F.text == __("🏳️ Change language"))
async def change_language(message: Message, state: FSMContext):
    await show_language_selection(message, state)


@router_language.callback_query(F.data.startswith("lang"))
async def lang_selected_handler(callback: CallbackQuery, state: FSMContext):
    code = map_lang.get(callback.data)
    if not code:
        await callback.answer(_("❌ Unknown language selection"), show_alert=True)
        return

    i18n.ctx_locale.set(code)
    await state.update_data(locale=code)

    tg_id = str(callback.from_user.id)
    user = await User.filter_one(tg_id=tg_id)
    if user:
        await User.update(_id=user.id, locale=code)

    await callback.message.delete()
    await callback.message.answer(_("✅ Language successfully changed!"))
    await state.set_state(SectorStates.main_menu)
