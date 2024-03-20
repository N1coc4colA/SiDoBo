import discord
import discord.ui as ui

import src.db as db

from src.views.view import BaseView


class CancellerView(BaseView):
    def __init__(self, ctrl):
        super().__init__(ctrl)
        self.selection = ui.Select(options=[], placeholder="Créneau")
        self.selection.callback = self.icallback

    def reset(self) -> bool:
        reserved = []

        for e in db.query_by_date(self.ctrl.current_date.strftime("%d/%m/%Y"), self.ctrl.ctx.author.id):
            so0 = discord.SelectOption(label=e)
            so0.value = e
            reserved.append(so0)

        self.selection.options = reserved
        self.add_item(self.selection)

        return len(reserved) != 0

    @discord.ui.button(label="Valider", style=discord.ButtonStyle.primary)
    async def on_submit(self, interaction: discord.Interaction, any) -> None:
        if len(self.selection.values) == 0:
            await interaction.response.defer()
            return

        await self.ctrl.cancellation_request(self.selection.values[0], interaction)

