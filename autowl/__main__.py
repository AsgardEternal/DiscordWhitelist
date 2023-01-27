import discord
from os import environ
from sys import stderr


# main runtime function
def main():
    if disToken := environ.get('DISCORD_TOKEN'):
        print(f"Received discord token: {disToken}")
        # Call into main action here, basically launch the bot via import to a lower module
    else:
        print("Unable to access DISCORD_TOKEN in environment!", file=stderr)
        exit(1)


main()
