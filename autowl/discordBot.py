import discord
from sys import stderr


class WhiteLister(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")


def startBot(discordtoken):
    print("starting discord bot")
    intents = discord.Intents.default()
    intents.message_content = True

    client = WhiteLister(intents=intents)
    try:
        print("discord bot started!")
        client.run(discordtoken)
    except:
        print("Invalid discord token!", file=stderr)
        exit(1)
