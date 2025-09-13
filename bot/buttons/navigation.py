from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bot.dispatcher import dp
from bot.states import SectorStates


@dp.message(F.text == __("🏠 Main menu"))
async def universal_main_menu_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.main_menu)
    await message.answer(_("🏠 Main menu"), reply_markup=get_main_menu_keyboard())


def build_keyboard(buttons: list[list[str]]) -> ReplyKeyboardBuilder:
    rkb = ReplyKeyboardBuilder()
    for row in buttons:
        rkb.row(*[KeyboardButton(text=_(text)) for text in row])
    return rkb


def get_add_view_keyboard():
    buttons = [
        [_("⏬ Add"), _("👀 View")],
        [_("⬅️ Back")]
    ]
    return build_keyboard(buttons).as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_view_keyboard():
    buttons = [
        [_("Last week"), _("Last month")],
        [_("Last 6 months"), _("All")],
        [_("⬅️ Back")]
    ]
    return build_keyboard(buttons).as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_main_menu_keyboard():
    buttons = [
        [_("🖼 Photos"), _("🎥 Videos"), _("📄 Documents")],
        [_("✉️ Text messages"), _("🎵 Audios"), _("👤 Contacts")],
        [_("🎙 Voice messages"), _("📞 Contact us")],
        [_("⚙️ Settings")]
    ]
    return build_keyboard(buttons).as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_settings_keyboard():
    buttons = [
        [_("👤 Change username"), _("🔢 Change password")],
        [_("🏳️ Change language"), _("🏌🏻‍♀️ Delete account")],
        [_("🚫 Logout")],
        [_("⬅️ Back")],
    ]
    return build_keyboard(buttons).as_markup(resize_keyboard=True, one_time_keyboard=True)


def add_done_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=_('✅ Done'))],
                  [KeyboardButton(text=_('⬅️ Back'))]],
        resize_keyboard=True, one_time_keyboard=True
    )


def get_back_keyboard():
    return build_keyboard([[_("⬅️ Back")]]).as_markup(resize_keyboard=True, one_time_keyboard=True)


def delete_account_markup():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="✅ Yes, delete", callback_data="delete_yes"),
        InlineKeyboardButton(text="⬅️ Back", callback_data="delete_cancel"),
    )
    keyboard.adjust(2)
    return keyboard.as_markup()
