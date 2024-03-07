import discord

class CroissantView(discord.ui.View):
    def __init__(self, croissanting):
        super().__init__()
        self.croissanting = croissanting

    @discord.ui.button(label="Prendre un croissant", style=discord.ButtonStyle.green)
    async def take_croissant(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.croissanting.eaters:
            await interaction.response.send_message("Vous avez déjà pris un croissant !", ephemeral=True)
            return
        if interaction.user.id == self.croissanting.ctx.author.id:
            await interaction.response.send_message("Vous ne pouvez pas prendre un croissant à vous même !", ephemeral=True)
            return
        if time.time() - self.croissanting.last_eating_time >= self.croissanting.croissant_guild.pick_delay:
            await interaction.response.send_message("Vous avez prit un croissant !", ephemeral=True)
            self.croissanting.eaters.append(interaction.user.id)
            self.croissanting.last_eating_time = time.time()
            return
        else:
            await interaction.response.send_message("Vous devez attendre encore un peu !", ephemeral=True)
            return

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.croissanting.ctx.author.id:
            await interaction.response.send_message("Vous avez stoppé la croissanting !", ephemeral=True)
            await self.croissanting.stop()
        else:
            await interaction.response.send_message("Vous n'êtes pas le croissanté !", ephemeral=True)
)
