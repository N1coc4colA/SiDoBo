import discord.ui as ui
import discord

import src.db as db
import src.shared as shared


class ReservationModal(ui.Modal, title="Motif de réservation"):
    def __init__(self, ctrl, date, time):
        super().__init__()
        self.ctrl = ctrl
        self.date = date
        self.time = time

        self.target = ui.TextInput(label="Que voulez-vous travailler ?", placeholder="La physque quantique")
        self.add_item(self.target)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if interaction.user.id != self.ctrl.ctx.author.id:
            await interaction.response.send_message("Vous n'avez pas le droit de faire l'interaction!", ephemeral=True)
            return

        date = self.ctrl.current_date.strftime("%d/%m/%Y")
        db.update_timeslot(self.date, self.ctrl.selected_time, self.target.value)
        await shared.get_client().dm_reserved(date, self.ctrl.selected_time)
        await interaction.response.send_message("Changements enregistrés.", ephemeral=True)
        await self.ctrl.end()


