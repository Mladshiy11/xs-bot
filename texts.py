# texts.py
# XS Mobile Numbers Bot — barcha matnlar

# === START ===

WELCOME = (
    "🔥 XS Raqamlar — siz izlagan chiroyli va premium telefon raqamlari shu yerda!\n\n"
    "📱 Istalgan raqamni toping\n"
    "🔎 Raqamni tekshiring\n"
    "💳 Qulay to'lov qiling\n"
    "⚡ Tezkor va ishonchli xizmat\n\n"
    "✨ O'zingizga mos raqamni tanlang va XS bilan ajralib turing!"
)

ASK_NAME = "Iltimos, ismingizni kiriting:"

WELCOME_BACK = "Xush kelibsiz, {ism}!"

MENU = "🏠 Asosiy menyu:"

# === KOMPANIYA ===

def company_page(kompaniya_nomi, sahifa_raqami):
    return f"📱 {kompaniya_nomi} — {sahifa_raqami}-sahifa"

def number_selected(kompaniya_nomi, raqam):
    return (
        f"📱 {kompaniya_nomi}\n"
        f"🔢 Tanlangan raqam: {raqam}\n\n"
        f"💎 To'liq raqam va narxni bilish uchun\n"
        f"admin bilan bog'laning."
    )

# === QIDIRUV ===

SEARCH_ASK_NUMBER = "Tekshirmoqchi bo'lgan raqamingizni to'liq kiriting:\n\nMasalan: +998901234567"

def search_payment(card, owner, price):
    return (
        f"💳 Raqamni tekshirish uchun {price} to'lov qiling.\n\n"
        f"Karta: {card}\n"
        f"Egasi: {owner}\n\n"
        f"To'lovni amalga oshirgach, skrinshotni shu botga yuboring."
    )

SEARCH_SCREENSHOT_SENT = "✅ Skrinshot adminga yuborildi. Javobni kuting."

# === ADMIN ===

def admin_notification(ism, user_id, raqam):
    return (
        f"🔔 Yangi tekshiruv so'rovi\n\n"
        f"👤 Ism: {ism}\n"
        f"🆔 ID: {user_id}\n"
        f"📱 Raqam: {raqam}\n\n"
        f"✍️ Javob yozish uchun shu xabarga reply qiling:"
    )

ADMIN_BROADCAST_ASK = "📢 Yubormoqchi bo'lgan xabaringizni kiriting:"

def admin_broadcast_confirm(jami):
    return f"📢 Bu xabar {jami} ta foydalanuvchiga yuboriladi.\n\nTasdiqlaysizmi?"

ADMIN_BROADCAST_STARTED = "⏳ Yuborish boshlandi..."

def admin_broadcast_done(yuborildi, xato):
    return f"✅ Yuborildi: {yuborildi}\n❌ Xato: {xato}"

ADMIN_BROADCAST_CANCELED = "❌ Bekor qilindi."

# === XATOLIK ===

ERROR_UNKNOWN = "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
