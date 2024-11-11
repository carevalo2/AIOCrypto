import time
import os
from aiohttp import ClientSession, ClientTimeout, ClientError
from AIOCrypto.models.coin_model import CoinModel
from asyncio import TimeoutError
from decimal import Decimal
from dotenv import load_dotenv
import logging

load_dotenv()

class CoinMarketCapService:

    UPDATE_INTERVAL_SECONDS: float = 30
    SESSION = None
    CLIENT_TIMEOUT_SECONDS: float = 10
    URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    HEADERS = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.getenv('X-CMC_PRO_API_KEY'),
    }

    def __init__(self, coin: CoinModel):
        self.coin = coin
        if not CoinMarketCapService.session:
            CoinMarketCapService.session = ClientSession(
                headers=self.HEADERS, timeout=ClientTimeout(total=CoinMarketCapService.CLIENT_TIMEOUT_SECONDS)
            )

    async def get_price(self) -> Decimal:
        current_time = int(time.time())
        if self.is_price_outdated(current_time):
            await self._update_price(current_time)
        return self.coin.price

    async def _update_price(self, current_time: int) -> Decimal:
        parameters = {
            'symbol': self.coin.symbol,
            'convert': 'USD'
        }
        try:
            async with CoinMarketCapService.SESSION.get(self.URL, params=parameters) as response:
                data = await response.json()
                new_price = Decimal(data['data'][self.coin.symbol]['quote']['USD']['price'])
                self.update_price(new_price, current_time)
                return new_price
        except (ClientError, TimeoutError) as e:
            logging.error(f"Error fetching price: {e}")
            return Decimal(0)

    def update_price(self, new_price: Decimal, current_time: int) -> None:
        self.coin = new_price
        self.coin.last_updated = current_time

    def is_price_outdated(self, current_time: int) -> bool:
        return (self.coin.price is None
                or self.coin.last_updated is None
                or (current_time - self.coin.last_updated) > self.UPDATE_INTERVAL_SECONDS)

    # TODO implement get_day_high_price
    async def get_day_high_price(self) -> Decimal:
        pass

    # TODO implement get_day_low_price
    async def get_day_low_price(self) -> Decimal:
        pass
