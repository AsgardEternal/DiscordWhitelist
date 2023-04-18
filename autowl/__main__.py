import logging
import sys
import autowl.bot as bot
from os import environ
from autowl.config import DiscordClientConfig

log = logging.getLogger(__name__)

class CustomFormat(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = (
        "[%(asctime)s][%(levelname)s][%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    )

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logging():
    log_level = environ.get("LOG_LEVEL") or "INFO"

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setFormatter(CustomFormat())

    log.setLevel(log_level)
    discord_log = logging.getLogger("discord")
    discord_log.setLevel(log_level)
    discord_http_log = logging.getLogger("discord.http")
    discord_http_log.setLevel(log_level)

    logging.basicConfig(level=log_level, handlers=[ch])


def main():
    setup_logging()

    if disToken := environ.get("DISCORD_TOKEN"):
        bot_config = DiscordClientConfig(disToken)
        if not (dbpass := environ.get("DBPASS")):
            log.error("Unable to access DBPASS in environment!")
            exit(1)
        try:
            bot.Bot(bot_config, dbpass).start_bot()
        except Exception as e:
            log.critical(f"Bot exited critically, error: {e}")
            raise e
    else:
        log.error("Unable to access DISCORD_TOKEN in environment!")
        exit(1)

    exit(0)


main()
