import discord
from autowl import config
from autowl.bot import Bot
from discord.ext import commands
from discord import app_commands


class Group(commands.Cog, name="group"):
    def __init__(self, client: Bot):
        self.client = client

    @app_commands.command()
    async def add(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
    ):

        if self.client.whitelist.get(role.name):
            await interaction.response.send_message(
                f"**{role.name}** is already added, cannot add it again!"
            )
            return

        dropdown = discord.ui.Select(
            min_values=1,
            max_values=20,
            placeholder="Choose group permissions in Squad",
            options=[
                discord.SelectOption(
                    label="changemap", description="Allows users to change the map"
                ),
                discord.SelectOption(
                    label="pause", description="Pause server gameplay"
                ),
                discord.SelectOption(
                    label="cheat", description="Use server cheat commands"
                ),
                discord.SelectOption(
                    label="private", description="Password protect server"
                ),
                discord.SelectOption(
                    label="balance", description="Group Ignores server team balance"
                ),
                discord.SelectOption(
                    label="chat", description="Admin chat and Server broadcast"
                ),
                discord.SelectOption(
                    label="kick",
                    description="Allows user to kick players from the server",
                ),
                discord.SelectOption(
                    label="ban",
                    description="Allows user to ban players from the server",
                ),
                discord.SelectOption(
                    label="config", description="Change server config"
                ),
                discord.SelectOption(
                    label="cameraman", description="Admin spectate mode"
                ),
                discord.SelectOption(
                    label="immune", description="Cannot be kicked / banned"
                ),
                discord.SelectOption(
                    label="manageserver", description="Shutdown server"
                ),
                discord.SelectOption(
                    label="featuretest",
                    description="Any features added for testing by dev team",
                ),
                discord.SelectOption(label="reserve", description="Reserve slot"),
                discord.SelectOption(
                    label="demos",
                    description="Record Demos on the server side via admin commands",
                ),
                discord.SelectOption(
                    label="clientdemos",
                    description="Record Demos on the client side via commands or the replay UI.",
                ),
                discord.SelectOption(
                    label="debug",
                    description="show admin stats command and other debugging info",
                ),
                discord.SelectOption(
                    label="teamchange", description="No timer limits on team change"
                ),
                discord.SelectOption(
                    label="forceteamchange",
                    description="Can issue the ForceTeamChange command",
                ),
                discord.SelectOption(
                    label="canseeadminchat",
                    description="This group can see the admin chat and teamkill/admin-join notifications",
                ),
            ],
        )
        view = discord.ui.View()
        view.add_item(dropdown)

        async def perms_handler(interaction: discord.Interaction):
            perms = "\n  - ".join(dropdown.values)
            dropdown.disabled = True
            await interaction.response.edit_message(view=view)
            await interaction.followup.send(
                f"Adding **{role.name}** to whitelist with permissions:\n  - {perms}\n\n"
            )
            self.client.whitelist[f"{role.name}"] = config.WhitelistGroup(
                permissions=dropdown.values, discord_role_id=role.id, members={}
            )
            print(self.client.whitelist)

        dropdown.callback = perms_handler

        ctx: commands.Context = await self.client.get_context(interaction)


        await ctx.send(view=view)
