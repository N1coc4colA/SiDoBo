import discord.ui as ui
import discord

import src.db as db

from src.views.view import BaseView


class TimeSlotAddView(BaseView):
    def __init__(self, ctrl):
        super().__init__(ctrl)

        hours = []
        minutes = []

        for i in range(0, 24):
            so0 = discord.SelectOption(label=str(i))
            so0.value = str(i)
            hours.append(so0)

        i = 0
        while i < 60:
            so0 = discord.SelectOption(label=str(i))
            so0.value = str(i)
            minutes.append(so0)
            i += 15

        self.hours = ui.Select(options=hours, placeholder="Heure")
        self.hours.callback = self.icallback
        self.add_item(self.hours)
        self.minutes = ui.Select(options=minutes, placeholder="Minute")
        self.minutes.callback = self.icallback
        self.add_item(self.minutes)

    def reset(self) -> bool:
        return True

    @discord.ui.button(label="Valider", style=discord.ButtonStyle.primary)
    async def on_submit(self, interaction: discord.Interaction, any) -> None:
        await self.ctrl.add_request(self.hours.values[0] + ":" + self.minutes.values[0], interaction)


class TimeSlotRmView(BaseView):
    def __init__(self, ctrl):
        super().__init__(ctrl)

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
        if len(self.selection.values) == 0:
            await interaction.response.defer()
            return

        await self.ctrl.remove_request(self.selection.values[0], "Raison inconnue.", interaction)

