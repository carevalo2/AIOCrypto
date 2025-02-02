from discord import Embed, File
from pathlib import Path
from datetime import datetime
from bot.mvc.models.coin_model import CoinModel
from services.formatter_service import FormatterService

coin_colors: dict[str, int] = {
    "Bitcoin" : 0xf7931a,
    "Ethereum" : 0x88aaf1,
    "Litecoin" : 0x949494,
}

class PriceEmbed(Embed):

    def __init__(self, title: str, color: int):
        super().__init__(
            title=title,
            color=color,
            timestamp=datetime.now(),
        )
        self.set_footer(text="Powered by AIOCrypto")


class CoinView:

    def __init__(self, coin_model: CoinModel, formatter: FormatterService):
        self.coin_model = coin_model
        self.formatter = formatter

    def create_price_embed(self) -> tuple[PriceEmbed, File]:
        coin_icon_path = Path(f"assets/icons/{self.coin_model.name}.png")
        file = File(coin_icon_path, filename='coin_icon.png')

        embed = PriceEmbed(
            title=f"{self.coin_model.name} ({self.coin_model.symbol}) USD",
            color=coin_colors[self.coin_model.name]
        )

        price = FormatterService.format_currency(self.coin_model.price)
        last_updated = FormatterService.format_time(self.coin_model.last_updated)

        embed.add_field(name="Price", value=price)
        embed.add_field(name=f"The price was last updated:", value=f" {last_updated}")
        embed.set_thumbnail(url="attachment://coin_icon.png")

        return embed, file
