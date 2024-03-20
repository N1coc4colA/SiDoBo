import discord

import src.settings as settings
import src.logs as logs
from src.logs import log
import src.shared as shared

from src.views.settings import SettingsView
from src.controller.controller import Controller
from src.modals.members_editor import MembersEditorModal
from src.modals.bans_editor import BansEditorModal
from src.modals.servers_editor import ServersEditorModal


class SettingsController(Controller):
    def __init__(self, ctx):
        super().__init__(
            ctx,
            step=0,
            views=[SettingsView(self)],
            generators=[self._settings_embed],
        )

    async def _settings_embed(self) -> discord.Embed:
        # Embed
        embed = discord.Embed(title="Soutien - Paramètres", color=0xf5ce42)
        embed.set_thumbnail(url="https://em-content.zobj.net/source/apple/118/gear_2699.png")
        embed.set_footer(text="Fait par n1coc4cola ❤️")

        field_name = "Administrateurs:"
        field_value = ""
        lst = settings.get_admins()
        if lst:
            for e in lst:
                people = await shared.get_client().fetch_user(e)
                field_value += f"{people.mention}\n{e}\n"
        else:
            field_value = "Aucun administrateur pour le serveur."
        embed.add_field(name=field_name, value=field_value)

        field_name = "GUILDs:"
        field_value = ""
        lst = settings.get_guilds()
        if lst:
            for e in lst:
                field_value += f"{e[1]}\n{e[0]}\n"
        else:
            field_value = "Aucun GUILD enregistré."
        embed.add_field(name=field_name, value=field_value)

        field_name = "Bannis:"
        field_value = ""
        lst = settings.get_bans()
        if lst:
            for e in lst:
                people = await shared.get_client().fetch_user(e)
                field_value += f"{people.mention}\n{e}\n"
        else:
            field_value = "Aucun banni pour le moment."
        embed.add_field(name=field_name, value=field_value)

        return embed

    async def remove_server_modal(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        await interaction.response.send_modal(ServersEditorModal(self))

    async def add_member_modal(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        await interaction.response.send_modal(MembersEditorModal(self, True))

    async def remove_member_modal(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        await interaction.response.send_modal(MembersEditorModal(self, False))

    async def add_ban_modal(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        await interaction.response.send_modal(BansEditorModal(self, True))

    async def remove_ban_modal(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        await interaction.response.send_modal(BansEditorModal(self, False))

    async def empty_logs(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        interaction.response.defer()

        logs.logs.local = []
        log(f"{interaction.user.id} cleared logs.")




