# keyboards.py
# XS Mobile Numbers Bot — tugmalar

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_USERNAME, COMPANIES, PAGE_SIZE, TOTAL_NUMBERS

# === ASOSIY MENYU ===

def main_menu():
    """Asosiy menyu — 6 ta tugma"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Ucell", callback_data="comp_ucell")],
        [InlineKeyboardButton(text="📱 Beeline", callback_data="comp_beeline")],
        [InlineKeyboardButton(text="📱 Uzmobile", callback_data="comp_uzmobile")],
        [InlineKeyboardButton(text="📱 UMS", callback_data="comp_ums")],
        [InlineKeyboardButton(text="🔎 Raqam qidirish", callback_data="search")],
        [InlineKeyboardButton(
            text="📞 Admin bilan aloqa",
            url=f"https://t.me/{ADMIN_USERNAME}"
        )],
    ])
    return kb

# === KOMPANIYA SAHIFALARI ===

def numbers_page(kompaniya, raqamlar, sahifa):
    """
    Raqamlar sahifasi.
    kompaniya — 'ucell', 'beeline', ...
    raqamlar — 10 ta raqam ro'yxati (tuple ko'rinishida)
    sahifa — 0, 1, 2, ... 9
    """
    buttons = []

    # Raqamlar tugmalari
    for r in raqamlar:
        raqam_matni = r[0] if isinstance(r, (tuple, list)) else r
        buttons.append([
            InlineKeyboardButton(
                text=raqam_matni,
                callback_data=f"pick_{kompaniya}_{raqam_matni}"
            )
        ])

    # Navigatsiya tugmalari
    nav = []
    jami_sahifa = TOTAL_NUMBERS // PAGE_SIZE  # 100 / 10 = 10

    if sahifa > 0:
        nav.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data=f"page_{kompaniya}_{sahifa - 1}"
        ))
    if sahifa < jami_sahifa - 1:
        nav.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data=f"page_{kompaniya}_{sahifa + 1}"
        ))
    if nav:
        buttons.append(nav)

    # Asosiy menyu
    buttons.append([
        InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="menu")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# === RAQAM TANLANGANDA ===

def number_detail():
    """Raqam tanlanganda ko'rsatiladigan tugmalar"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📞 Admin bilan bog'lanish",
            url=f"https://t.me/{ADMIN_USERNAME}"
        )],
        [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="menu")],
    ])
    return kb

# === QIDIRUV NATIJASI ===

def after_check_available():
    """Raqam mavjud bo'lganda"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📞 Sotib olish uchun bog'lanish",
            url=f"https://t.me/{ADMIN_USERNAME}"
        )],
        [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="menu")],
    ])
    return kb

def after_check_unavailable():
    """Raqam mavjud bo'lmaganda"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="menu")],
    ])
    return kb

# === ADMIN BROADCAST ===

def broadcast_confirm():
    """Broadcast tasdiqlash tugmalari"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ha, yuborish", callback_data="bc_yes")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="bc_no")],
    ])
    return kb
