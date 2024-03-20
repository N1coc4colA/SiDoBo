import discord

from src.views.view import BaseView


class PlanningView(BaseView):
    def __init__(self, ctrl):
        super().__init__(ctrl)

    def reset(self) -> bool:
        return True

    @discord.ui.button(label="Préc.", style=discord.ButtonStyle.primary)
    async def previous_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.previous_page(interaction)

    @discord.ui.button(label="Dump", style=discord.ButtonStyle.success)
    async def dump_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.dump_day(interaction)

    @discord.ui.button(label="Suiv.", style=discord.ButtonStyle.primary)
    async def next_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.next_page(interaction)
