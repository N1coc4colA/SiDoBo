import discord.ui as ui
import discord

import src.settings as settings
from src.logs import log


class BansEditorModal(ui.Modal):
    def __init__(self, ctrl, mode: bool):
        super().__init__(title=("Ajout d'un ban" if mode else "Suppression d'un ban"))
        self.ctrl = ctrl
        self.mode = mode

        self.target = ui.TextInput(label="ID Utilisateur", placeholder="XXXXX")
        self.add_item(self.target)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if interaction.user.id != self.ctrl.ctx.author.id:
            await interaction.response.send_message("Vous n'avez pas le droit de faire l'interaction!", ephemeral=True)
            return

        if len(self.target.value) == 0:
            await interaction.response.defer()
            return

        if self.mode:
            settings.get_bans().append(self.target.value)
            log(f"{interaction.user.id} banned {self.target.value}")
            await interaction.response.send_message(f"Utilisateur {self.target.value} banni.", ephemeral=True)
        else:
            settings.get_bans().remove(self.target.value)
            log(f"{interaction.user.id} unbanned {self.target.value}")
            await interaction.response.send_message(f"Utilisateur {self.target.value} débanni.", ephemeral=True)
