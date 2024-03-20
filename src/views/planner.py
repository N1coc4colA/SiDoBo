import discord

from src.views.view import BaseView


class PlannerView(BaseView):
    def __init__(self, ctrl):
        super().__init__(ctrl)

    def reset(self) -> bool:
        return True

    @discord.ui.button(label="Préc.", style=discord.ButtonStyle.primary)
    async def previous_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.previous_page(interaction)

    @discord.ui.button(label="Ajouter", style=discord.ButtonStyle.success)
    async def add_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.add_slot_view(interaction)

    @discord.ui.button(label="Suppr.", style=discord.ButtonStyle.danger)
    async def remove_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.rm_slot_view(interaction)

    @discord.ui.button(label="Suiv.", style=discord.ButtonStyle.primary)
    async def next_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.next_page(interaction)
