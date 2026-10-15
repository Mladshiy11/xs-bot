# handlers/start.py
# /start buyrug'i va ismni qabul qilish

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import database as db
import keyboards as kb
import texts as t

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)

    if user and user[1]:
        await message.answer(
            t.WELCOME_BACK.format(ism=user[1]),
            reply_markup=kb.main_menu()
        )
        await db.set_state(user_id, "menu")
        return

    await db.add_user(user_id, None)
    await message.answer(t.WELCOME)
    await message.answer(t.ASK_NAME)
    await db.set_state(user_id, "ism_kutilmoqda")
