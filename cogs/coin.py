from discord import Interaction
from discord.ext import commands
from discord.app_commands import command as slash_command, Choice, choices, describe

from services.formatter_service import FormatterService

from bot.mvc.controllers.coin_controller import CoinController
from bot.mvc.models.coin_model import CoinModel
from bot.mvc.views.coin_view import CoinView

class Coin(commands.Cog):

    controller_cache: dict[str] = {}

    coin_tickers: dict[str] = {
        'Bitcoin': 'BTC',
        'Ethereum': 'ETH',
        'Litecoin': 'LTC'
    }

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="price", description="Get the current price in USD of BTC, ETH, or LTC.")
    @describe(coin="Defaults to Bitcoin.")
    @choices(coin=[
        Choice(name='Bitcoin', value='Bitcoin'),
        Choice(name='Ethereum', value='Ethereum'),
        Choice(name='Litecoin', value='Litecoin')
    ])
    async def price(self, interaction: Interaction, coin: Choice[str] = None) -> None:
        await interaction.response.defer()

        if not coin:
            coin_name = "Bitcoin"
            coin_ticker = "BTC"
        else:
            coin_name: str = coin.value
            coin_ticker: str = self.coin_tickers[coin_name]

        try:
            controller: CoinController = self.controller_cache[coin_name]
            price_embed, file = await controller.get_price_embed()
            await interaction.followup.send(embed=price_embed, file=file)
        except KeyError:
            model: CoinModel = CoinModel(coin_name, coin_ticker)
            view : CoinView = CoinView(model, formatter=FormatterService())
            controller: CoinController = CoinController(model, view)

            self.controller_cache[coin_name] = controller

            price_embed, file = await controller.get_price_embed()

            await interaction.followup.send(embed=price_embed, file=file)


async def setup(bot):
    await bot.add_cog(Coin(bot))
