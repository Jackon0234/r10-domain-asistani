import aiosqlite
from datetime import datetime

DB_NAME = "bot_database.db"

class Database:
    def __init__(self):
        self.db_name = DB_NAME

    async def create_tables(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id BIGINT UNIQUE,
                    username TEXT,
                    credits INTEGER DEFAULT 10,
                    joined_at DATETIME
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS query_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id BIGINT,
                    domain TEXT,
                    status TEXT,
                    checked_at DATETIME
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS monitors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id BIGINT,
                    domain TEXT,
                    added_at DATETIME,
                    UNIQUE(user_id, domain)
                )
            """)
            await db.commit()

    async def add_user(self, telegram_id: int, username: str):
        async with aiosqlite.connect(self.db_name) as db:
            try:
                await db.execute(
                    "INSERT OR IGNORE INTO users (telegram_id, username, joined_at) VALUES (?, ?, ?)",
                    (telegram_id, username, datetime.now())
                )
                await db.commit()
            except Exception:
                pass

    async def log_query(self, telegram_id: int, domain: str, status: str):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "INSERT INTO query_history (user_id, domain, status, checked_at) VALUES (?, ?, ?, ?)",
                (telegram_id, domain, status, datetime.now())
            )
            await db.commit()

    async def add_monitor(self, user_id: int, domain: str):
        async with aiosqlite.connect(self.db_name) as db:
            try:
                await db.execute(
                    "INSERT INTO monitors (user_id, domain, added_at) VALUES (?, ?, ?)",
                    (user_id, domain, datetime.now())
                )
                await db.commit()
                return True
            except aiosqlite.IntegrityError:
                return False 

    async def get_all_monitors(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT id, user_id, domain FROM monitors") as cursor:
                return await cursor.fetchall()

    async def remove_monitor(self, monitor_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("DELETE FROM monitors WHERE id = ?", (monitor_id,))
            await db.commit()

    async def get_stats(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT COUNT(*) FROM users") as cursor:
                user_count = await cursor.fetchone()
            async with db.execute("SELECT COUNT(*) FROM query_history") as cursor:
                query_count = await cursor.fetchone()
            async with db.execute("SELECT COUNT(*) FROM monitors") as cursor:
                monitor_count = await cursor.fetchone()
        return {"users": user_count[0], "queries": query_count[0], "monitors": monitor_count[0]}