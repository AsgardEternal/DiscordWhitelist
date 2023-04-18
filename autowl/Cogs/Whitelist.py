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
            rowsaffected = updatecur.rowcount
            if rowsaffected <= 0:
                updatecur.execute(self.client.squadjs_findByDiscordID, [interaction.user.id])
                if updatecur.rowcount <= 0:
                    await interaction.response.send_message("Cound not find SteamID!")
                else:
                    for urole in interaction.user.roles:
                        if urole.id in self.client.whitelistGrps.keys():
                            self.client.whitelistGrps[urole.id].members[f"{interaction.user.id}"].steam64 = steam64
                            self.client.whitelistGrps[urole.id].updateGroup()
                    await interaction.response.send_message("SteamID already linked, roles updated.")
                self.client.squadjs.commit()
                return
        except mysql.connector.Error as err:
            log.error("MYSQL error!")
            await interaction.response.send_message("There was an internal server error, pls contact skillet")
            return
        for urole in interaction.user.roles:
            if urole.id in self.client.whitelistGrps.keys():
                disusername = interaction.user.nick if interaction.user.nick is not None else interaction.user.name
                self.client.whitelistGrps[urole.id].addMember(config.WhitelistMember(interaction.user.id, disusername, steam64))
        self.client.squadjs.commit()
        await interaction.response.send_message(f"discord is linked to steamID, roles updated.")
