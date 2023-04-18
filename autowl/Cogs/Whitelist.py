import discord
import logging

import mysql.connector

from autowl import config
from autowl.bot import Bot
from discord.ext import commands
from discord import app_commands


log = logging.getLogger(__name__)


class Whitelist(commands.Cog):
    def __init__(self, client: Bot):
        self.client = client

    @app_commands.command()
    async def link(self, interaction: discord.Interaction, steam64: str):
        if not interaction.guild:
            await interaction.response.send_message(
                "This command must be ran within a discord server!"
            )
            return
        updatecur = self.client.squadjs.cursor(buffered=True)
        try:
            updatecur.execute(self.client.squadjs_updateDiscordID, (interaction.user.id, steam64))
        except mysql.connector.Error as err:
            log.error("MYSQL error!")
            await interaction.response.send_message("Could not find steamID!")
            return
        for urole in interaction.user.roles:
            if urole.id in self.client.whitelistGrps.keys():
                disusername = interaction.user.nick if interaction.user.nick is not None else interaction.user.name
                self.client.whitelistGrps[urole.id].addMember(config.WhitelistMember(interaction.user.id, disusername, steam64))
        self.client.squadjs.commit()
        await interaction.response.send_message("SteamID is linked, roles updated.")
