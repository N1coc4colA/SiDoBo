import discord.ui as ui
import discord

import src.db as db

from src.views.view import BaseView


class ModifyView(BaseView):
    def __init__(self, ctrl):
        super().__init__(ctrl)

        self.selection = ui.Select(options=[], placeholder="Créneau")
        self.selection.callback = self.icallback
        self.add_item(self.selection)

    def reset(self) -> bool:
        availables = []

        for i in db.query_by_date(self.ctrl.current_date.strftime("%d/%m/%Y"), self.ctrl.ctx.author.id):
            so0 = discord.SelectOption(label=str(i))
            so0.value = str(i)
            availables.append(so0)

        self.selection.options = availables

        return len(availables) != 0

    @discord.ui.button(label="Valider", style=discord.ButtonStyle.primary)
    async def on_submit(self, interaction: discord.Interaction, any) -> None:
        if len(self.selection.values) == 0:
            await interaction.response.defer()
            return

        await self.ctrl.modify_modal(self.selection.values[0], interaction)

