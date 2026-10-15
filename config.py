# config.py
# XS Mobile Numbers Bot — sozlamalar fayli

import os

# === BOT ===
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "BU_YERGA_TOKEN")

# === ADMIN ===
ADMIN_ID = int(os.getenv("TELEGRAM_ADMIN_ID", "8463290119"))
ADMIN_USERNAME = os.getenv("TELEGRAM_ADMIN_USERNAME", "xs05005")

# === TO'LOV ===
CARD_NUMBER = "8600 0304 5518 5714"
CARD_OWNER = "Arziyev Asadbek"
SEARCH_PRICE = "5 000 so'm"

# === KOMPANIYALAR ===
COMPANIES = {
    "ucell":    "Ucell",
    "beeline":  "Beeline",
    "uzmobile": "Uzmobile",
    "ums":      "UMS",
}

# === SAHIFALASH ===
PAGE_SIZE = 10
TOTAL_NUMBERS = 100
