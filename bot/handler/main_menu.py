import os

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from dotenv import load_dotenv

from bot.buttons.navigation import get_add_view_keyboard, get_main_menu_keyboard
from bot.handler.lang import *

load_dotenv()


@dp.callback_query(SectorStates.contact_us, F.data == 'back')
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


@dp.message(SectorStates.main_menu, F.text == __("✉️ Letters"))
async def letters_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.letter)
    await message.answer(_("✉️ Letters"), reply_markup=get_add_view_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("🎙 Voice"))
async def letters_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.voice)
    await message.answer(_("🎙 Voice"), reply_markup=get_add_view_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("🎵 Audio"))
async def letters_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.audio)
    await message.answer(_("🎵 Audio"), reply_markup=get_add_view_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("👤 Contact"))
async def letters_handler(message: Message, state: FSMContext):
    await state.set_state(SectorStates.contact)
    await message.answer(_("👤 Contact"), reply_markup=get_add_view_keyboard())


@dp.message(SectorStates.main_menu, F.text == __("📞 Contact us"))
async def letters_handler(message: Message, state: FSMContext):
    tg_username = os.getenv('TG_USERNAME')
    username_link = f"https://t.me/{tg_username}"
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("👮🏻‍♀️ Admin"), url=username_link)],
            [InlineKeyboardButton(text=_("⬅️ Back"), callback_data='back')]
        ]
    )

    await state.set_state(SectorStates.contact_us)
    await message.answer(text=_("Click the button to contact ⬇️"), reply_markup=ikb)
