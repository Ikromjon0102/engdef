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


async def get_users_count():
    async with db_pool.acquire() as conn:
        count = await conn.fetchval("""
            SELECT COUNT(tg_id) FROM users;
        """)
        return count

async def get_users():
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT tg_id FROM users;
        """)
        user_list = [row['tg_id'] for row in rows]
        # print(user_list)
        return user_list
