import discord.ui as ui
import discord
from typing import Any


class BaseView(ui.View):
    def __init__(self, ctrl):
        super().__init__()
        self.ctrl = ctrl

    async def interaction_check(self, interaction: discord.Interaction, /) -> bool:
        return await self.ctrl.validate(interaction)

    async def empty_callback(*args, **kwargs) -> None:
        pass

    @staticmethod
    async def icallback(interaction: discord.Interaction) -> Any:
        await interaction.response.defer()
