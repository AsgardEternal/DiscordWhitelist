from os import environ
from sys import stderr
from multiprocessing import Process
import autowl.fileServer as fileServer
import autowl.discordBot as discordBot


# main runtime function
def main():
    if disToken := environ.get('DISCORD_TOKEN'):
        print(f"Received discord token: {disToken}")
        # Call into main action here, basically launch the bot via import to a lower module
    else:
        print("Unable to access DISCORD_TOKEN in environment!", file=stderr)
        exit(1)

    fsproc = Process(target=fileServer.startServer)
    disbot = Process(target=discordBot.startBot, args=(disToken,))

    fsproc.start()
    disbot.start()

    fsproc.join()
    disbot.join()

    exit(0)


main()
