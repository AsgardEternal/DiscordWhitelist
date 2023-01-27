import discord
from os import environ
from sys import stderr


class WhiteLister(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")


# main runtime function
def main():
    if disToken := environ.get('DISCORD_TOKEN'):
        print(f"Received discord token: {disToken}")
        # Call into main action here, basically launch the bot via import to a lower module
    else:
        print("Unable to access DISCORD_TOKEN in environment!", file=stderr)
        exit(1)

    intents = discord.Intents.default()
    intents.message_content = True

    client = WhiteLister(intents=intents)
    try:
        client.run(disToken)
    except:
        print("Invalid discord token!", file=stderr)


main()
