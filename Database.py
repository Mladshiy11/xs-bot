# database.py
# XS Mobile Numbers Bot — ma'lumotlar bazasi

import aiosqlite

DB_NAME = "bot.db"

async def init_db():
    """Bazani yaratish va jadvallarni tayyorlash"""
    async with aiosqlite.connect(DB_NAME) as db:
        # Foydalanuvchilar jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                ism TEXT,
                holat TEXT DEFAULT 'menu',
                vaqt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Qidiruv so'rovlari jadvali
        await db.execute("""
            CREATE TABLE IF NOT EXISTS search_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                raqam TEXT,
                skrinshot_msg_id INTEGER,
                holat TEXT DEFAULT 'kutilmoqda',
                vaqt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

# === FOYDALANUVCHILAR ===

async def add_user(user_id, ism=None):
    """Foydalanuvchini qo'shish yoki yangilash"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """INSERT INTO users (user_id, ism) VALUES (?, ?)
               ON CONFLICT(user_id) DO UPDATE SET ism = COALESCE(?, ism)""",
            (user_id, ism, ism)
        )
        await db.commit()

async def get_user(user_id):
    """Foydalanuvchini olish"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            return await cursor.fetchone()

async def set_state(user_id, holat):
    """Foydalanuvchi holatini o'zgartirish"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET holat = ? WHERE user_id = ?",
            (holat, user_id)
        )
        await db.commit()

async def get_all_users():
    """Barcha foydalanuvchilarni olish (broadcast uchun)"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            return await cursor.fetchall()

# === QIDIRUV SO'ROVLARI ===

async def save_search_request(user_id, raqam, skrinshot_msg_id):
    """Qidiruv so'rovini saqlash"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """INSERT INTO search_requests (user_id, raqam, skrinshot_msg_id)
               VALUES (?, ?, ?)""",
            (user_id, raqam, skrinshot_msg_id)
        )
        await db.commit()

async def update_search_request(user_id, raqam, skrinshot_msg_id):
    """Mavjud so'rovni yangilash (skrinshot kelganda)"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """UPDATE search_requests
               SET skrinshot_msg_id = ?, holat = 'kutilmoqda'
               WHERE user_id = ? AND raqam = ? AND skrinshot_msg_id = 0""",
            (skrinshot_msg_id, user_id, raqam)
        )
        await db.commit()

async def find_user_by_screenshot(msg_id):
    """Skrinshot xabar ID si bo'yicha foydalanuvchini topish"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT user_id, raqam FROM search_requests WHERE skrinshot_msg_id = ?",
            (msg_id,)
        ) as cursor:
            return await cursor.fetchone()

async def get_last_search(user_id):
    """Foydalanuvchining oxirgi qidiruvini olish"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            """SELECT raqam FROM search_requests
               WHERE user_id = ? AND skrinshot_msg_id = 0
               ORDER BY id DESC LIMIT 1""",
            (user_id,)
        ) as cursor:
            return await cursor.fetchone()
