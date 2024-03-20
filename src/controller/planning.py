import discord
from datetime import datetime, timedelta

from src.controller.controller import Controller
import src.db as db
import src.shared as shared

from src.views.planning import PlanningView


class PlanningStep:
    See: int = 0


class PlanningController(Controller):
    def __init__(self, ctx):
        super().__init__(
            ctx,
            step=PlanningStep.See,
            views=[PlanningView(self)],
            generators=[self.planning_embed]
        )

        self.current_date = datetime.now()

    async def planning_embed(self) -> discord.Embed:
        date = self.current_date.strftime("%d/%m/%Y")
        embed = discord.Embed(title=f"Soutien - Données du jour {date}", color=0xf5ce42)
        embed.set_thumbnail(url="https://em-content.zobj.net/source/google/298/pen_1f58a-fe0f.png")
        embed.set_footer(text="Fait par n1coc4cola ❤️")
        field_name = "Créneaux réservés:"
        field_value = ""

        lst = db.get_reserved(date)
        if lst:
            for e in lst:
                field_value += f"{e[0]}, {e[3]}A"
        else:
            field_value = "Rien de réservé."

        embed.add_field(name=field_name, value=field_value)
        return embed

    async def next_page(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        self.current_date = self.current_date + timedelta(days=1)

        await interaction.response.defer()
        await self.next_step(PlanningStep.See, interaction)

    async def previous_page(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        self.current_date = self.current_date - timedelta(days=1)

        await interaction.response.defer()
        await self.next_step(PlanningStep.See, interaction)

    async def dump_day(self, interaction: discord.Interaction) -> None:
        if not await self.validate(interaction):
            return

        date = self.current_date.strftime("%d/%m/%Y")
        for e in db.get_reserved(date):
            people = await shared.get_client().fetch_user(e[1])
            await self.ctx.channel.send(content=f"> {date} {e[0]} - ({e[3]}A): {people.mention}\n{e[2]}")

        await interaction.response.defer()
        await self.next_step(PlanningStep.See, interaction)


