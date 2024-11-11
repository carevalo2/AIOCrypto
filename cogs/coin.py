from logging import Formatter

from discord import Interaction
from discord.ext import commands
from discord.app_commands import command as slash_command, Choice, choices, describe
from AIOCrypto.controllers.coin_controller import CoinController
from AIOCrypto.models.coin_model import CoinModel
from AIOCrypto.services.formatter_service import FormatterService
from AIOCrypto.views.coin_view import CoinView
import traceback


class Coin(commands.Cog):

    cache: dict[CoinController] = {}

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="price", description="Get the current price in USD of BTC, ETH, or LTC.")
    @describe(coin="Select a supported cryptocurrency.")
    @choices(coin=[
        Choice(name='Bitcoin', value='Bitcoin (BTC)'),
        Choice(name='Ethereum', value='Ethereum (ETH)'),
        Choice(name='Litecoin', value='Litecoin (LTC)')
    ])
    async def price(self, interaction: Interaction, coin: Choice[str]) -> None:
        await interaction.response.defer()
        name, symbol = coin.value.split("(", 1)
        name: str = name.strip()
        symbol: str = symbol.strip(")").strip()
        controller: CoinController = self.cache.get(name)
        if controller:
            price_embed = await controller.get_price_embed()
            return await interaction.followup.send(embed=price_embed)
        else:
            try:
                model: CoinModel = CoinModel(name, symbol)
                view: CoinView = CoinView(model, FormatterService())
                controller: CoinController = CoinController(model, view)
                if self.cache.get(name) is None:
                    self.cache[name] = controller
                price_embed = await controller.get_price_embed()
                await interaction.followup.send(embed=price_embed)
            except Exception as e:
                print(traceback.format_exc())


async def setup(bot):
    await bot.add_cog(Coin(bot))
