import asyncpg

db_pool = None

async def create_db_pool():
    global db_pool
    db_pool = await asyncpg.create_pool(
        user='postgres',
        password='0000',
        database='engdef',
        host='localhost',
        port='5432'
    )

async def add_user(telegram_id, first_name, last_name):
    async with db_pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (tg_id, first_name, last_name)
            VALUES ($1, $2, $3)
            ON CONFLICT (tg_id) DO NOTHING;
        """, telegram_id, first_name, last_name)
