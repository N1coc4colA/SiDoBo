import discord.ui as ui
import discord

import src.db as db

from src.views.view import BaseView


class ReserveView(BaseView):
    def __init__(self, ctrl):
        super().__init__(ctrl)

        so0 = discord.SelectOption(label="1A")
        so0.value = "1"
        so1 = discord.SelectOption(label="2A")
        so1.value = "2"

        self.year = ui.Select(options=[so0, so1], placeholder="Mon année")
        self.year.callback = self.icallback
        self.add_item(self.year)

        self.selection = ui.Select(options=[], placeholder="Créneau")
        self.selection.callback = self.icallback
        self.add_item(self.selection)

    def reset(self) -> bool:
        availables = []

        for i in db.get_availables(self.ctrl.current_date.strftime("%d/%m/%Y")):
            so0 = discord.SelectOption(label=str(i))
            so0.value = str(i)
            availables.append(so0)

        self.selection.options = availables

        return len(availables) != 0

    @discord.ui.button(label="Valider", style=discord.ButtonStyle.primary)
    async def on_submit(self, interaction: discord.Interaction, any) -> None:
        if len(self.selection.values) == 0 or len(self.year.values) == 0:
            await interaction.response.defer()
            return

        await self.ctrl.reservation_request(self.selection.values[0], self.year.values[0], interaction)

