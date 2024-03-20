import discord

from src.views.view import BaseView


class ReservationView(BaseView):
    def __init__(self, ctrl):
        super().__init__(ctrl)

    def reset(self) -> bool:
        return True

    @discord.ui.button(label="Préc.", style=discord.ButtonStyle.primary)
    async def previous_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.previous_page(interaction)

    @discord.ui.button(label="Réserver", style=discord.ButtonStyle.success)
    async def reserve_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.reserve_view(interaction)

    @discord.ui.button(label="Modifier", style=discord.ButtonStyle.success)
    async def edit_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.modify_view(interaction)

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.danger)
    async def cancel_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.cancel_view(interaction)

    @discord.ui.button(label="Suiv.", style=discord.ButtonStyle.primary)
    async def next_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.next_page(interaction)
