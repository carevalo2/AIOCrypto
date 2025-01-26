import asyncio
import asyncpg
import os
from bot.aio_crypto import AIOCrypto
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('AIOCrypto/.env')
load_dotenv(dotenv_path=dotenv_path)

async def main():
    db_name = os.getenv('DATABASE_NAME')
    db_username = os.getenv('DATABASE_USERNAME')
    db_password = os.getenv('DATABASE_PASSWORD')

    async with asyncpg.create_pool(user=db_username, database=db_name, password=db_password) as pool:
        async with AIOCrypto() as bot:
            bot.db = pool
            await bot.run()

if __name__ == '__main__':
    asyncio.run(main())
