import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from bot.buttons.constants import MEDIA_TYPES
from bot.states import SectorStates
from db.model import get_db

router = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.message(F.text == __("⏬ Add"))
async def handle_add_command(message: Message, state: FSMContext):
    current_state = await state.set_state()
    for media, config in MEDIA_TYPES.items():
        if current_state == getattr(SectorStates, config["main_state"]).state:
            await message.answer(_("Please send {} to add.").format(media))
            await state.set_state(getattr(SectorStates, config["add_state"]))
            return


@router.message(SectorStates.photo, F.text == __("👀 View"))
async def handle_view_command(message: Message, state: FSMContext):
    current_state = await state.set_state()
    user_id = message.from_user.id
    for media, config in MEDIA_TYPES.items():
        if current_state == getattr(SectorStates, config["main_state"]).state:
            async with get_db() as db:
                try:
                    get_func = globals()[config["get_func"]]
                    items = await get_func(db, user_id)

                    if not items:
                        await message.answer(_("No {}s found.").format(media))
                        return

                    if config["input_media"]:
                        input_media_cls = config["input_media"]
                        if len(items) >= 2:
                            media_group = [input_media_cls(media=item.file_id) for item in items[:10]]
                            await message.answer_media_group(media_group)
                        else:
                            await message.answer(input_media_cls(media=items[0].file_id))

                    else:
                        for item in items[:10]:
                            await message.answer(item.file_id if media != "letter" else item.content)

                except Exception as e:
                    logger.error(f"Failed to view {media}: {e}")
                    await message.answer(_("Error fetching {}.").format(media))


@router.message()
async def handle_media_upload(message: Message, state: FSMContext):
    current_state = await state.get_state()
    user_id = message.from_user.id

    for media, config in MEDIA_TYPES.items():
        if current_state == getattr(SectorStates, config["add_state"]).state:
            files = []

            attr = config["file_attr"]
            if attr == "text" and message.text:
                files = [message.text]
            elif hasattr(message, attr):
                data = getattr(message, attr)
                files = [p.file_id for p in data] if isinstance(data, list) else [data.file_id]

            if not files:
                await message.answer(_("No valid {}s found.").format(media))
                return

            async with get_db() as db:
                save_func = globals()[config["save_func"]]
                try:
                    for file_id in files:
                        await save_func(db=db, user_id=user_id, file_id=file_id)
                    await message.answer(_("✅ {} saved successfully!").format(media.capitalize()))
                except Exception as e:
                    logger.error(f"Error saving {media}: {e}")
                    await message.answer(_("❌ Failed to save {}.").format(media))
            await state.set_state(getattr(SectorStates, config["main_state"]))
            return
