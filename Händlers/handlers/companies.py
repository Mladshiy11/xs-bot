# handlers/companies.py
# Kompaniyalar bo'limi

from aiogram import Router, F
from aiogram.types import CallbackQuery

import keyboards as kb
import texts as t
from config import COMPANIES, PAGE_SIZE

router = Router()

def generate_numbers(offset, limit):
    raqamlar = []
    for i in range(offset, offset + limit):
        if i >= 100:
            break
        raqam = f"+998 XX XXX {i:02d} {i:02d}"
        raqamlar.append((raqam,))
    return raqamlar

@router.callback_query(F.data.startswith("comp_"))
async def show_company(call: CallbackQuery):
    kompaniya = call.data.replace("comp_", "")
    await show_page(call, kompaniya, 0)

@router.callback_query(F.data.startswith("page_"))
async def change_page(call: CallbackQuery):
    parts = call.data.split("_")
    kompaniya = parts[1]
    sahifa = int(parts[2])
    await show_page(call, kompaniya, sahifa)

async def show_page(call: CallbackQuery, kompaniya: str, sahifa: int):
    nomi = COMPANIES.get(kompaniya, kompaniya)
    offset = sahifa * PAGE_SIZE
    raqamlar = generate_numbers(offset, PAGE_SIZE)

    if not raqamlar:
        await call.answer("Bu sahifada raqam yo'q", show_alert=True)
        return

    await call.message.edit_text(
        t.company_page(nomi, sahifa + 1),
        reply_markup=kb.numbers_page(kompaniya, raqamlar, sahifa)
    )
    await call.answer()

@router.callback_query(F.data.startswith("pick_"))
async def pick_number(call: CallbackQuery):
    parts = call.data.split("_", 2)
    kompaniya = parts[1]
    raqam = parts[2]
    nomi = COMPANIES.get(kompaniya, kompaniya)

    await call.message.edit_text(
        t.number_selected(nomi, raqam),
        reply_markup=kb.number_detail()
    )
    await call.answer()
