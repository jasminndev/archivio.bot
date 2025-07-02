import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.navigation import add_done_keyboard
from bot.states import SectorStates
from aiogram_media_group import media_group_handler

from db.models import Photo

router = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.message(F.text == __("⏬ Add"))
async def add_photo_handler(message: Message, state: FSMContext):
    await message.answer(text=_("📸 Please send the photos you want to add. After finishing click the '✅ Done' button!"),
                         reply_markup=add_done_keyboard())
    await state.set_state(SectorStates.waiting_photos)


@router.message(SectorStates.waiting_photos, F.media_group_id, F.photo)
async def handle_media_group(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id

    data = await state.get_data()
    photos = data.get("photos", [])
    photos.append(file_id)
    await state.update_data(photos=photos)


@router.message(SectorStates.waiting_photos, F.photo)
async def handle_single_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id

    data = await state.get_data()
    photos = data.get("photos", [])
    photos.append(file_id)
    await state.update_data(photos=photos)

    await message.answer("✅ Rasm saqlandi. Yana yuborishingiz mumkin.")


from aiogram import F


@router.message(SectorStates.waiting_photos, F.text == "✅ Done")
@media_group_handler
async def handle_media_group_photos(messages: list[Message], state: FSMContext):
    photos = []

    for message in messages:
        file_id = message.photo[-1].file_id
        photos.append(file_id)
        await Photo.create(photo_id=file_id)

    await state.update_data(photos=photos)
    await state.set_state(WorkForm.location)

    await messages[-1].answer(
        _("Iltimos, ish joyini joylashuvini xaritadan tanlab yuboring:"),
        reply_markup=back_button()
    )

@router.message(WorkForm.photo, F.photo, ~F.media_group_id)
async def handle_single_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await Photo.create(photo_id=file_id)
    await state.update_data(photos=[file_id])
    await state.set_state(WorkForm.location)
    await message.answer(
        _("Iltimos, ish joyini joylashuvini xaritadan tanlab yuboring:"),
        reply_markup=back_button()
    )


@router.message(SectorStates.waiting_photos)
async def not_photo_warning(message: Message):
    await message.answer("❗️Iltimos, rasm yuboring yoki '✅ Done' tugmasini bosing.")
