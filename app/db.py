from pathlib import Path

import aiosqlite

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    material TEXT NOT NULL,
    volume TEXT NOT NULL,
    address TEXT NOT NULL,
    when_needed TEXT NOT NULL,
    comment TEXT NOT NULL DEFAULT '',
    vk_ok INTEGER NOT NULL DEFAULT 0,
    max_ok INTEGER NOT NULL DEFAULT 0,
    telegram_ok INTEGER NOT NULL DEFAULT 0
);
"""


async def _ensure_column(db: aiosqlite.Connection, name: str) -> None:
    cursor = await db.execute("PRAGMA table_info(leads)")
    columns = {row[1] for row in await cursor.fetchall()}
    if name not in columns:
        await db.execute(f"ALTER TABLE leads ADD COLUMN {name} INTEGER NOT NULL DEFAULT 0")


async def init_db(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(path) as db:
        await db.execute(CREATE_SQL)
        await _ensure_column(db, "vk_ok")
        await _ensure_column(db, "max_ok")
        await _ensure_column(db, "telegram_ok")
        await db.commit()


async def insert_lead(
    path: Path,
    *,
    name: str,
    phone: str,
    material: str,
    volume: str,
    address: str,
    when_needed: str,
    comment: str,
    vk_ok: bool,
    max_ok: bool,
) -> int:
    async with aiosqlite.connect(path) as db:
        cursor = await db.execute(
            """
            INSERT INTO leads (
                name, phone, material, volume, address, when_needed, comment, vk_ok, max_ok
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                phone,
                material,
                volume,
                address,
                when_needed,
                comment,
                int(vk_ok),
                int(max_ok),
            ),
        )
        await db.commit()
        return int(cursor.lastrowid or 0)
