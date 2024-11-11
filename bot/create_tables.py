
async def create_coin_table(db_pool):
    query: str = """
        CREATE TABLE IF NOT EXISTS coins (
            name TEXT,
            symbol TEXT,
            most_recent_price_usd NUMERIC(19, 4),
            high_past_day NUMERIC(19,4),
            low_past_day NUMERIC(19,4),
        );
    """
    async with db_pool.acquire() as connection:
        await connection.execute(query)
