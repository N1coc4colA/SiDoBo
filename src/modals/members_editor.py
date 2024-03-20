import discord.ui as ui
import discord

import src.settings as settings
from src.logs import log


class MembersEditorModal(ui.Modal):
    def __init__(self, ctrl, mode: bool):
        super().__init__(title=("Ajout d'un membre" if mode else "Suppression d'un membre"))
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
            settings.get_admins().append(self.target.value)
            log(f"{interaction.user.id} added {self.target.value}")
            await interaction.response.send_message(f"Membre {self.target.value} ajouté.", ephemeral=True)
        else:
            settings.get_admins().remove(self.target.value)
            log(f"{interaction.user.id} removed {self.target.value}")
            await interaction.response.send_message(f"Membre {self.target.value} supprimé.", ephemeral=True)
