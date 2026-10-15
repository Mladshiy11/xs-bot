# handlers/menu.py
# Asosiy menyu

from aiogram import Router, F
from aiogram.types import CallbackQuery

import database as db
import keyboards as kb
import texts as t

router = Router()

@router.callback_query(F.data == "menu")
async def show_menu(call: CallbackQuery):
    await db.set_state(call.from_user.id, "menu")
    await call.message.edit_text(
        t.MENU,
        reply_markup=kb.main_menu()
    )
    await call.answer()
