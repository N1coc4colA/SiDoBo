import discord.ui as ui
import discord

import src.settings as settings
from src.logs import log


class ServersEditorModal(ui.Modal, title="Suppression d'un serveur"):
    def __init__(self, ctrl):
        super().__init__()
        self.ctrl = ctrl

        self.target = ui.TextInput(label="GUILD", placeholder="XXXXX")
        self.add_item(self.target)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if interaction.user.id != self.ctrl.ctx.author.id:
            await interaction.response.send_message("Vous n'avez pas le droit de faire l'interaction!", ephemeral=True)
            return

        log(f"{interaction.user.id} removed GUILD {self.target.value}")
        settings.get_guilds().remove(self.target.value)

        await interaction.response.send_message(f"Serveur {self.target.value} supprimé.", ephemeral=True)

