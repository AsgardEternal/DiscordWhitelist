import discord
import logging
from autowl import config
from autowl.bot import Bot
from discord.ext import commands
from discord import app_commands


log = logging.getLogger(__name__)


class Whitelist(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client

    @app_commands.command()
    async def register(self, interaction: discord.Interaction, steam64: int):
        if not interaction.guild:
            await interaction.response.send_message(
                "This command must be ran within a discord server!"
            )
            return

        if not len(self.client.whitelist.keys()):
            await interaction.response.send_message(
                "There are no Whitelist roles defined, unable to continue!"
            )
            return

        steam64_updated = False
        for role in interaction.user.roles:
            for group in self.client.whitelist:
                if role.id == self.client.whitelist[group].discord_role_id:
                    steam64_updated = True
                    self.client.whitelist[group].members[
                        interaction.user.id
                    ] = config.WhitelistMember(interaction.user.name, steam64)

        if steam64_updated:
            log.info(
                f"Updated {interaction.user.name}'s ({interaction.user.id}) whitelist steam64 to {steam64}"
            )
            await interaction.response.send_message(
                f"Updated `{interaction.user.name}`'s whitelist steam64 to `{steam64}`!"
            )
        else:
            await interaction.response.send_message(f"Unable to update `{interaction.user.name}`'s whitelist steam64 as they are not in a valid Whitelisted group")
