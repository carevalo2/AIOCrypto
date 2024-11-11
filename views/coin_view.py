from discord import Embed
from datetime import datetime
from ..models.coin_model import CoinModel
from ..services.formatter_service import FormatterService


class PriceEmbed(Embed):
    def __init__(self, title: str = None, description: str = None, color: int = 0x3498db):
        super().__init__(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.now()
        )
        self.set_footer(text="Powered by AIOCrypto")


class CoinView:

    def __init__(self, coin_model: CoinModel, formatter: FormatterService):
        self.coin_model = coin_model
        self.formatter = formatter

    def create_price_embed(self) -> Embed:
        embed = PriceEmbed(title=f"{self.coin_model.name} ({self.coin_model.symbol}) USD")
        price = FormatterService.format_currency(self.coin_model.price)
        last_updated = FormatterService.format_time(self.coin_model.last_updated)
        embed.add_field(name="Price", value=price)
        embed.add_field(name=f"The price was last updated: {self.coin_model.last_updated}", value=f"{last_updated}")
        return embed
