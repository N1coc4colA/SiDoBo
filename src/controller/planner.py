import discord
from datetime import datetime, timedelta

from src.controller.controller import Controller
import src.db as db
import src.shared as shared

from src.views.timeslot import TimeSlotAddView, TimeSlotRmView
from src.views.planner import PlannerView


class PlannerStep:
    See: int = 0
    Remove: int = 1
    Add: int = 2


class PlannerController(Controller):
    def __init__(self, ctx):
        super().__init__(
            ctx,
            step=PlannerStep.See,
            views=[PlannerView(self), TimeSlotRmView(self), TimeSlotAddView(self)],
            generators=[self.planner_embed, self.planner_rm_embed, self.planner_add_embed]
        )

        self.current_date = datetime.now()

    async def planner_embed(self) -> discord.Embed:
        date = self.current_date.strftime("%d/%m/%Y")
        embed = discord.Embed(title=f"Soutien - Mode édition {date}", color=0xf5ce42)
        embed.set_thumbnail(url="https://em-content.zobj.net/source/google/298/pen_1f58a-fe0f.png")
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
        return embed

    async def planner_rm_embed(self) -> discord.Embed:
        date = self.current_date.strftime("%d/%m/%Y")
        embed = discord.Embed(title=f"Supprimer un créneau du {date}", color=0xf5ce42)
        embed.set_thumbnail(url="https://em-content.zobj.net/source/google/298/pen_1f58a-fe0f.png")
        embed.set_footer(text="Fait par n1coc4cola ❤️")
        field_name = "Créneaux disponibles:"
        field_value = ""

        lst = db.get_availables(date)
        if lst:
            for e in lst:
                field_value += f"{e} "
        else:
            field_value = "Aucun."

        embed.add_field(name=field_name, value=field_value)
        return embed

    async def planner_add_embed(self) -> discord.Embed:
        date = self.current_date.strftime("%d/%m/%Y")
        embed = discord.Embed(title=f"Ajouter un créneau au {date}", color=0xf5ce42)
        embed.set_thumbnail(url="https://em-content.zobj.net/source/google/298/pen_1f58a-fe0f.png")
        embed.set_footer(text="Fait par n1coc4cola ❤️")
        field_name = "Créneaux déjà disponibles:"
        field_value = ""

        lst = db.get_availables(date)
        if lst:
            for e in lst:
                field_value += f"{e} "
        else:
            field_value = "Aucun."

        embed.add_field(name=field_name, value=field_value)
        return embed

    async def next_page(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        self.current_date = self.current_date + timedelta(days=1)

        await interaction.response.defer()
        await self.next_step(PlannerStep.See, interaction)

    async def previous_page(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        self.current_date = self.current_date - timedelta(days=1)

        await interaction.response.defer()
        await self.next_step(PlannerStep.See, interaction)

    async def add_slot_view(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        await interaction.response.defer()
        await self.next_step(PlannerStep.Add, interaction)

    async def rm_slot_view(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        await interaction.response.defer()
        await self.next_step(PlannerStep.Remove, interaction)

    async def add_request(self, time: str, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        date = self.current_date.strftime("%d/%m/%Y")
        if db.add_timeslot(date, time):
            await interaction.response.send_message("Créneau ajouté.", ephemeral=True)
            await self.end()
            return

        await interaction.response.send_message("Une erreur est survenue lors de l'ajout du créneau.", ephemeral=True)
        await self.next_step(PlannerStep.See, interaction)

    async def remove_request(self, time: str, reason: str, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        await db.remove_timeslot(self.current_date.strftime("%d/%m/%Y"), time, "")
        await interaction.response.send_message("Créneau supprimé.", ephemeral=True)

        await self.next_step(PlannerStep.See, interaction)


