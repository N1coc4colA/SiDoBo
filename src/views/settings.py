import discord

from src.views.view import BaseView


class SettingsView(BaseView):
    def __init__(self, ctrl):
        super().__init__(ctrl)

    def reset(self):
        return True

    @discord.ui.button(label="Aj. membre", style=discord.ButtonStyle.green)
    async def add_member_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.add_member_modal(interaction)

    @discord.ui.button(label="Suppr. membre", style=discord.ButtonStyle.danger)
    async def remove_member_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.remove_member_modal(interaction)

    @discord.ui.button(label="Suppr. serveur", style=discord.ButtonStyle.danger)
    async def remove_server_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.remove_server_modal(interaction)

    @discord.ui.button(label="Aj. ban", style=discord.ButtonStyle.danger)
    async def add_ban_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.add_ban_modal(interaction)

    @discord.ui.button(label="Suppr. ban", style=discord.ButtonStyle.primary)
    async def remove_ban_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.remove_ban_modal(interaction)

    @discord.ui.button(label="Vider logs", style=discord.ButtonStyle.primary)
    async def empty_logs_action(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.empty_logs(interaction)
