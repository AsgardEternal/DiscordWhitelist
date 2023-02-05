import discord
from sys import stderr

MY_GUILD = discord.Object(id=1064037361786302475)
adminsroleids = [1067044106439761950]
generalwl = dict(name='Whitelist', discordid=1067044106439761950, permslist=['reserve'], members=[])
masterwllist = [generalwl]


def removewlmember(wllist, userid):
    memberrmindex = -1
    for i in range(len(wllist['members'])):
        if wllist['members'][i]['userid'] == userid:
            memberrmindex = i
    if memberrmindex < 0:
        return
    wllist['members'].remove(wllist['members'][memberrmindex])
    

async def updatefile(wllist):
    with open(f"remoteAdmins/{wllist['name']}", 'w') as file:
        rawperm = ''
        for perm in wllist['permslist']:
            rawperm = f"{rawperm},{perm}"
        file.write(f"Group={wllist['name']}:{rawperm}\n\n")
        for wluser in wllist['members']:
            file.write(f"Admin={wluser['steamid']}:{wllist['name']} // discord:{wluser['username']} ({wluser['userid']})\n")


class WhiteLister(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_member_update(self, before, after):
        print(f"user '{after.name} ({after.id})' started member update")
        rmrolesid = []
        for befrole in before.roles:
            rmrolesid.append(befrole.id)
        for aftrole in after.roles:
            for befrole in before.roles:
                if befrole.id == aftrole.id:
                    rmrolesid.remove(aftrole.id)

        for rmroleid in rmrolesid:
            for wllist in masterwllist:
                if wllist['discordid'] == rmroleid:
                    removewlmember(wllist, before.id)
                    await updatefile(wllist)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


async def hellofunc(interaction: discord.Interaction, steam64id: str):
    print(f"user '{interaction.user.name} ({interaction.user.id})' attempting whitelist")
    hasrole = False
    for userrole in interaction.user.roles:
        if userrole.id == WHITELISTID:
            hasrole = True
    if not hasrole:
        print(f"user '{interaction.user.name} ({interaction.user.id})' does not have whitelist role")
        await interaction.response.send_message(f"ERROR: user does not have whitelist role!")
        return
    for wlentry in generalwhitelist:
        if wlentry[0] == steam64id:
            print(f"user '{interaction.user.name} ({interaction.user.id})' used an existing steam id")
            await interaction.response.send_message(f"ERROR: steam64id already exists in whitelist!")
            return
        if wlentry[1] == interaction.user.id:
            print(f"user '{interaction.user.name} ({interaction.user.id})' used an existing discord id")
            await interaction.response.send_message(f"ERROR: discord user id already exists in whitelist!")
            return
    username = interaction.user.name
    if not (interaction.user.nick is None):
        username = interaction.user.nick
    newwlentry = dict(steamid=steam64id, userid=interaction.user.id, username=username)
    generalwl["members"].append(newwlentry)
    print(f"user '{interaction.user.name} ({interaction.user.id})' added with steamid '{steam64id}'")
    await updateFile()
    await interaction.response.send_message(
        f'Added {newwlentry[2]} ({newwlentry[1]}) with steamid: {newwlentry[0]}, to glbwhitelist!')

def startBot(discordtoken):
    print("starting discord bot")
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    client = WhiteLister(intents=intents)

    @client.tree.command()
    async def hello(interaction: discord.Interaction, steam64id: str):
        await hellofunc(interaction, steam64id)

    try:
        print("discord bot started!")
        client.run(discordtoken)
    except:
        print("Invalid discord token!", file=stderr)
        exit(1)
