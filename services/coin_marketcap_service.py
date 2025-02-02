import time
import logging

from aiohttp import ClientSession, ClientTimeout, ClientError
from bot.mvc.models.coin_model import CoinModel
from config.config import load_config
from asyncio import TimeoutError
from decimal import Decimal

class CoinMarketCapService:

    config = load_config()

    UPDATE_INTERVAL_SECONDS: float = 30
    CLIENT_TIMEOUT_SECONDS: float = 10

    URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    HEADERS = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': config['coinmarketcap_api_key'],
    }

    SESSION = ClientSession(
        headers=HEADERS, timeout=ClientTimeout(total=CLIENT_TIMEOUT_SECONDS)
    )

    def __init__(self, coin: CoinModel):
        self.coin = coin

    async def get_price(self) -> Decimal | None:

        if not self.is_price_outdated(int(time.time())):
            return self.coin.price

        parameters = {
            'symbol': self.coin.symbol,
            'convert': 'USD'
        }

        try:
            async with CoinMarketCapService.SESSION.get(self.URL, params=parameters) as response:
                data = await response.json()
                new_price = Decimal(data['data'][self.coin.symbol]['quote']['USD']['price'])
                self.update_price(new_price)
                return new_price
        except (ClientError, TimeoutError) as e:
            logging.error(f"Error fetching price: {e}")
            return None

    def update_price(self, new_price) -> None:
        current_time = int(time.time())
        self.coin.price = new_price
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
