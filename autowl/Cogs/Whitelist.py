import discord
from autowl import config
from autowl.bot import Bot
from discord.ext import commands
from discord import app_commands


class Whitelist(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client

    @app_commands.command()
    async def register(self, interaction: discord.Interaction, steam64: int):
        ctx: commands.Context = await self.client.get_context(interaction)
        if not ctx.guild:
            ctx.reply("This command must be ran within a discord server!")
            return

        steam64_updated = False
        for role in ctx.author.roles:
            for group in self.client.whitelist:
                if role.id == group.discord_role_id:
                    steam64_updated = True
                    group.members[ctx.author.id] = config.WhitelistMember(
                        ctx.author.name, steam64
                    )

        if steam64_updated:
            ctx.reply(f"Updated {ctx.author.name}'s whitelist steam64 to {steam64}!")
