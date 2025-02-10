#!.venv/bin/python
from __future__ import annotations

from os import getenv

import hikari
from dotenv import load_dotenv

from slurs import load_slur_data

load_dotenv()
bot = hikari.GatewayBot(
    intents=hikari.Intents.ALL_MESSAGES | hikari.Intents.MESSAGE_CONTENT,
    token=getenv("DISCORD_TOKEN", "DISCORD_TOKEN"),
)

SLUR_REGEX = load_slur_data()


@bot.listen()
async def slur_detect(event: hikari.GuildMessageCreateEvent) -> None:
    """Detects usage of slurs in message and keeps track of the slur count."""
    if not event.is_human:
        return

    message_body = event.message.content
    if message_body is None:
        return

    match_result = [{k: v for k, v in m.groupdict().items() if v is not None} for m in SLUR_REGEX.finditer(message_body)]

    await event.message.respond(match_result, reply=True)


def main() -> None:
    """Main function for the bot."""
    bot.run()


if __name__ == "__main__":
    main()
