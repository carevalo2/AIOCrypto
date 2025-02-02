from typing import Any, Coroutine

from discord import Embed, File
from bot.mvc.views.coin_view import CoinView, PriceEmbed
from bot.mvc.models.coin_model import CoinModel
from services.coin_marketcap_service import CoinMarketCapService


class CoinController:

    def __init__(self, coin_model: CoinModel, coin_view: CoinView):
        self.coin_view = coin_view
        self.coin_model = coin_model

    async def get_price_embed(self) -> tuple[PriceEmbed, File]:
        service: CoinMarketCapService = CoinMarketCapService(self.coin_model)
        self.coin_model.price = await service.get_price()
        self.coin_model.day_high_price = None
        self.coin_model.day_low_price = None
        return self.coin_view.create_price_embed()
