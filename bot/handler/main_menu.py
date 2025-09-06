from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.navigation import get_add_view_keyboard, get_main_menu_keyboard, get_settings_keyboard
from bot.handler.lang import *
from db.config import conf


@dp.message(F.text.in_([__("⬅️ Back"), __("🏠 Main menu")]))
async def main_menu_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.main_menu)
    await message.answer(_("🏠 Main menu"), reply_markup=get_main_menu_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("🖼 Photos"))
async def photos_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.photo)
    await message.answer(_("🖼 Photos"), reply_markup=get_add_view_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("🎥 Videos"))
async def videos_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.video)
    await message.answer(_("🎥 Videos"), reply_markup=get_add_view_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("📄 Documents"))
async def documents_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.document)
    await message.answer(_("📄 Documents"), reply_markup=get_add_view_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("✉️ Text messages"))
async def text_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.text_message)
    await message.answer(_("✉️ Text messages"), reply_markup=get_add_view_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("🎙 Voice messages"))
async def voices_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.voice)
    await message.answer(_("🎙 Voice messages"), reply_markup=get_add_view_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("🎵 Audios"))
async def audios_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.audio)
    await message.answer(_("🎵 Audios"), reply_markup=get_add_view_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("👤 Contacts"))
async def contacts_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.contact)
    await message.answer(_("👤 Contacts"), reply_markup=get_add_view_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("📞 Contact us"))
async def contact_us__handler(message: Message, state: FSMContext):
    tg_username = conf.bot.TG_USERNAME
    username_link = f"https://t.me/{tg_username}"
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("👮🏻‍♀️ Admin"), url=username_link)],
            [InlineKeyboardButton(text=_("⬅️ Back"), callback_data='back')]
        ]
    )
    await state.set_state(SectorStates.contact_us)
    await message.answer(text=_("Click the button to contact ⬇️"), reply_markup=ikb)


@dp.callback_query(F.data == 'back')
async def back_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SectorStates.main_menu)
    await callback.message.edit_text(_("Back to main menu"), reply_markup=None)
    await callback.answer()
    await callback.message.answer(_("🏠 Main menu"), reply_markup=get_main_menu_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("⚙️ Settings"))
async def settings(message: Message, state: FSMContext):
    await state.set_state(SectorStates.settings)
    await message.answer(_("⚙️ Settings"), reply_markup=get_settings_keyboard())
