# handlers/admin.py
# Admin panel — reply, broadcast, stats

import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import database as db
import keyboards as kb
import texts as t
from config import ADMIN_ID

router = Router()

# === ADMIN REPLY (skrinshotga javob) ===

@router.message(F.reply_to_message)
async def admin_reply(message: Message):
    # Faqat admin yoza oladi
    if message.from_user.id != ADMIN_ID:
        return

    reply_id = message.reply_to_message.message_id
    row = await db.find_user_by_screenshot(reply_id)

    if not row:
        return

    target_user_id = row[0]
    admin_text = message.text or ""

    # "mavjud" so'zi bo'lsa — sotib olish tugmasi
    matn_past = admin_text.lower()
    if "mavjud" in matn_past and "mavjud emas" not in matn_past:
        await message.bot.send_message(
            target_user_id,
            admin_text,
            reply_markup=kb.after_check_available()
        )
    else:
        await message.bot.send_message(
            target_user_id,
            admin_text,
            reply_markup=kb.after_check_unavailable()
        )

# === BROADCAST ===

@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    await db.set_state(ADMIN_ID, "broadcast_kutilmoqda")
    await message.answer(t.ADMIN_BROADCAST_ASK)

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    users = await db.get_all_users()
    await message.answer(f"📊 Foydalanuvchilar soni: {len(users)}")

# === BROADCAST MATNINI QABUL QILISH ===

@router.message(F.text, F.from_user.id == ADMIN_ID)
async def handle_admin_text(message: Message):
    user = await db.get_user(ADMIN_ID)
    if not user or user[2] != "broadcast_kutilmoqda":
        return

    # Matnni vaqtincha saqlash
    await db.set_state(ADMIN_ID, "broadcast_tasdiq")
    await message.answer(
        t.admin_broadcast_confirm(0),
        reply_markup=kb.broadcast_confirm()
    )

# === BROADCAST TASDIQLASH ===

@router.callback_query(F.data == "bc_yes")
async def broadcast_yes(call: CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return

    await db.set_state(ADMIN_ID, "menu")
    await call.message.edit_text(t.ADMIN_BROADCAST_STARTED)

    users = await db.get_all_users()
    yuborildi = 0
    xato = 0

    for (uid,) in users:
        try:
            await call.bot.send_message(uid, "📢 Yangi xabar")
            yuborildi += 1
            await asyncio.sleep(0.05)
        except Exception:
            xato += 1

    await call.message.answer(t.admin_broadcast_done(yuborildi, xato))

@router.callback_query(F.data == "bc_no")
async def broadcast_no(call: CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return
    await db.set_state(ADMIN_ID, "menu")
    await call.message.edit_text(t.ADMIN_BROADCAST_CANCELED)
