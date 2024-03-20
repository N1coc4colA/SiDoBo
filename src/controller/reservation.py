import discord
from datetime import datetime, timedelta

import src.db as db

from src.controller.controller import Controller
from src.views.reservation import ReservationView
from src.views.canceller import CancellerView
from src.views.reserve import ReserveView
from src.views.modify import ModifyView
from src.modals.reservation import ReservationModal


class ReservationStep:
    See: int = 0
    Cancel: int = 1
    Reserve: int = 2
    Modify: int = 3


class ReservationController(Controller):
    def __init__(self, ctx):
        super().__init__(
            ctx,
            step=ReservationStep.See,
            views=[ReservationView(self), CancellerView(self), ReserveView(self), ModifyView(self)],
            generators=[self._reservation_embed, self._cancel_embed, self._reserve_embed, self._modify_embed]
        )

        self.selected_time = ""
        self.current_date: datetime = datetime.now()

    async def _reservation_embed(self) -> discord.Embed:
        date: str = self.current_date.strftime("%d/%m/%Y")
        embed = discord.Embed(title=f"Planning Soutien - Réservation {date}", color=0xf5ce42)
        embed.set_thumbnail(url="https://em-content.zobj.net/source/twitter/348/calendar_1f4c5.png")
        embed.set_footer(text="Fait par n1coc4cola ❤️")
        field_name = "Créneaux disponibles:"
        field_value = ""

        lst = db.get_availables(date)
        if lst:
            for e in lst:
                field_value += f"{e} "
        else:
            field_value = "Rien de disponible."
        embed.add_field(name=field_name, value=field_value)

        field_name = "Vous avez réservé:"
        field_value = ""

        lst = db.query_by_date(date, self.ctx.author.id)
        if lst:
            for e in lst:
                field_value += f"{e} "
        else:
            field_value = "Aucun créneau."
        embed.add_field(name=field_name, value=field_value)

        return embed

    async def _reserve_embed(self) -> discord.Embed:
        embed = discord.Embed(title=f"Réserver un créneau", color=0xf5ce42)
        embed.set_thumbnail(url="https://em-content.zobj.net/source/twitter/348/calendar_1f4c5.png")
        embed.set_footer(text="Fait par n1coc4cola ❤️")

        field_name = "Faire une réservation le:"
        field_value = self.current_date.strftime("%d/%m/%Y")
        embed.add_field(name=field_name, value=field_value)

        return embed

    async def _modify_embed(self) -> discord.Embed:
        embed = discord.Embed(title=f"Modifier la description d'une scéance", color=0xf5ce42)
        embed.set_thumbnail(url="https://em-content.zobj.net/source/twitter/348/calendar_1f4c5.png")
        embed.set_footer(text="Fait par n1coc4cola ❤️")

        field_name = "Modifier une réservation du:"
        field_value = self.current_date.strftime("%d/%m/%Y")
        embed.add_field(name=field_name, value=field_value)

        return embed

    async def _cancel_embed(self) -> discord.Embed:
        embed = discord.Embed(title=f"Annuler une réservation", color=0xf5ce42)
        embed.set_thumbnail(url="https://em-content.zobj.net/source/twitter/348/calendar_1f4c5.png")
        embed.set_footer(text="Fait par n1coc4cola ❤️")

        field_name = "Annuler une réservation le:"
        field_value = self.current_date.strftime("%d/%m/%Y")
        embed.add_field(name=field_name, value=field_value)

        return embed

    async def next_page(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        self.current_date = self.current_date + timedelta(days=1)

        await interaction.response.defer()
        await self.next_step(ReservationStep.See, interaction)

    async def previous_page(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        self.current_date = self.current_date - timedelta(days=1)

        await interaction.response.defer()
        await self.next_step(ReservationStep.See, interaction)

    async def cancel_view(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        await interaction.response.defer()
        await self.next_step(ReservationStep.Cancel, interaction)

    async def reserve_view(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        await interaction.response.defer()
        await self.next_step(ReservationStep.Reserve, interaction)

    async def modify_view(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        await interaction.response.defer()
        await self.next_step(ReservationStep.Modify, interaction)

    async def modify_modal(self, time: str, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        date: str = self.current_date.strftime("%d/%m/%Y")

        await interaction.response.send_modal(ReservationModal(self, date, time))
        await self.next_step(ReservationStep.See, interaction)

    async def cancellation_request(self, time: str, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        if db.cancel_timeslot(self.current_date.strftime("%d/%m/%Y"), time, interaction.user.id):
            await interaction.response.send_message("Scéance annulée.", ephemeral=True)
            await self.end()
            return

        await interaction.response.send_message("Une erreur est survenue lors de l'annulation.", ephemeral=True)
        await self.next_step(ReservationStep.See, interaction)

    async def reservation_request(self, time: str, year: str, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        date = self.current_date.strftime("%d/%m/%Y")
        if db.reserve_timeslot(date, time, interaction.user.id, year):
            self.selected_time = time
            await interaction.response.send_modal(ReservationModal(self, date, time))
            await self.end()
            return

        await interaction.response.send_message("Une erreur est survenue lors de la réservation.", ephemeral=True)
        await self.next_step(ReservationStep.See, interaction)


