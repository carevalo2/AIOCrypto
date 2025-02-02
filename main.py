import asyncio
import asyncpg
from bot.aio_crypto import AIOCrypto
from config.config import load_config

async def main():

    config = load_config()
    database_url = config['database_url']

    async with asyncpg.create_pool(dsn=database_url) as pool:
        async with AIOCrypto(db_pool=pool, config=config) as bot:
            await bot.run()

if __name__ == '__main__':
    asyncio.run(main())
