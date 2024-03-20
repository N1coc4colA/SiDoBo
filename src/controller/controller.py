import discord

from src.timer import Timer
from src.logs import log


class Controller:
    def __init__(self, ctx, views: list = [], generators: list = [], step: int = 0):
        self.ctx = ctx
        self.message = None
        self.views = views
        self.step = step
        self.prev_step = step
        self.generators = generators
        self.deleter = None
        self.timer = Timer(30.0, self._on_timeout)

    async def _on_timeout(self) -> None:
        if self.message:
            try:
                await self.message.delete()
            except discord.NotFound or discord.Forbidden or discord.HTTPException or ValueError:
                log("Error while deleting message.")
            finally:
                self.message = None

    async def initialize(self) -> None:
        await self._generate_page(None)

    async def validate(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("Vous n'avez pas le droit de faire l'interaction!", ephemeral=True)
            return False

        return True

    async def next_step(self, future_step: int, interaction: discord.Interaction) -> None:
        self.prev_step = self.step
        self.step = future_step
        await self._generate_page(interaction)

    async def _generate_page(self, interaction: discord.Interaction) -> None:
        embed = await self.generators[self.step]()

        success = True
        # Reset the view.
        try:
            success = self.views[self.step].reset()
        finally:
            pass

        if not success:
            if interaction and not interaction.response.is_done():
                await interaction.response.send_message("Impossible de réaliser l'action.", ephemeral=True)
            await self.next_step(self.prev_step, interaction)
            return

        if self.message:
            try:
                await self.message.delete()
            except discord.NotFound or discord.Forbidden or discord.HTTPException or ValueError:
                log("Error while deleting message")
            finally:
                self.message = None

        self.message = await self.ctx.channel.send(embed=embed, view=self.views[self.step])

        if self.timer.run:
            self.timer.reset()
        else:
            self.timer.start()

    async def end(self) -> None:
        if self.message:
            try:
                await self.message.delete()
            except discord.NotFound or discord.Forbidden or discord.HTTPException or ValueError:
                log("Error while deleting message")
            finally:
                self.message = None

        self.deleter(self)

