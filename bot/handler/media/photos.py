import logging

from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram_media_group import media_group_handler

from bot.buttons.navigation import add_done_keyboard, get_back_keyboard
from bot.states import SectorStates
from db.models import Photo

router = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.message(F.text == __("⏬ Add"))
async def add_photo_handler(message: Message, state: FSMContext):
    await message.answer(
        text=_("📸 Please send the photos you want to save. After finishing, click the '✅ Done' button!"),
        reply_markup=add_done_keyboard())
    await state.set_state(SectorStates.add_photo)
    await state.update_data(photos=[])


@router.message(F.media_group_id, F.photo)
@media_group_handler
async def handle_media_group_photos(messages: list[Message], state: FSMContext):
    new_photos = [msg.photo[-1].file_id for msg in messages]

    data = await state.get_data()
    existing_photos = data.get('photos', [])
    await state.update_data(photos=existing_photos + new_photos)

    await messages[-1].answer(
        _("Photos saved. After finishing, click the '✅ Done' button!")
    )


@router.message(SectorStates.add_photo, F.photo, ~F.media_group_id)
async def handle_single_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    data = await state.get_data()
    photos = data.get('photos', [])
    photos.append(file_id)
    await state.update_data(photos=photos)

    await message.answer(
        _("✅ Photo saved! You can send more or click the '✅ Done' button!")
    )


@router.message(SectorStates.add_photo, F.text == "✅ Done")
async def handle_done_button(message: Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get("photos", [])

    if not photos:
        await message.answer(_("❗️You didn't send photos!"))
        return

    for file_id in photos:
        await Photo.create(
            file_id=file_id,
        )

    await state.clear()
    await message.answer(
        _("✅ All photos saved! Thank you!"),
        reply_markup=get_back_keyboard()
    )


@router.message(SectorStates.add_photo)
async def not_photo_warning(message: Message):
    await message.answer("❗️Please, Send the photos or click the '✅ Done' button!")
