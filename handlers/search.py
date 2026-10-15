# handlers/search.py
# Raqam qidirish bo'limi

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

import database as db
import keyboards as kb
import texts as t
from config import ADMIN_ID, CARD_NUMBER, CARD_OWNER, SEARCH_PRICE

router = Router()

# === QIDIRUVNI BOSHLASH ===

@router.callback_query(F.data == "search")
async def start_search(call: CallbackQuery):
    await db.set_state(call.from_user.id, "qidiruv_raqam_kutilmoqda")
    await call.message.edit_text(t.SEARCH_ASK_NUMBER)
    await call.answer()

# === RAQAMNI QABUL QILISH ===

@router.message(F.text, F.text.startswith("+"))
async def handle_search_number(message: Message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)

    if not user or user[2] != "qidiruv_raqam_kutilmoqda":
        return

    raqam = message.text.strip()
    await db.set_state(user_id, "qidiruv_skrinshot_kutilmoqda")
    await db.save_search_request(user_id, raqam, 0)

    await message.answer(
        t.search_payment(CARD_NUMBER, CARD_OWNER, SEARCH_PRICE)
    )

# === SKRINSHOTNI QABUL QILISH ===

@router.message(F.photo)
async def handle_screenshot(message: Message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)

    if not user or user[2] != "qidiruv_skrinshot_kutilmoqda":
        return

    # Oxirgi qidiruvni olish
    last = await db.get_last_search(user_id)
    raqam = last[0] if last else "Noma'lum"

    # Adminga forward qilish
    sent = await message.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )

    # Adminga izoh yuborish
    await message.bot.send_message(
        ADMIN_ID,
        t.admin_notification(user[1] or "Nomsiz", user_id, raqam)
    )

    # Bazani yangilash
    await db.update_search_request(user_id, raqam, sent.message_id)
    await db.set_state(user_id, "menu")

    await message.answer(t.SEARCH_SCREENSHOT_SENT)
