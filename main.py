from __future__ import annotations

import asyncio

from telethon import TelegramClient
from telegram import Bot

from src.config_manager import load_config
from src.logger import setup_logger
from src.processor import PostProcessor
from src.monitor import ChannelMonitor
from src.bot import ForwardBot


async def main() -> None:
    config = load_config()
    logger = setup_logger()
    processor = PostProcessor(config, logger)

    client = TelegramClient(
        config["user_api"]["session_name"],
        config["user_api"]["api_id"],
        config["user_api"]["api_hash"],
    )
    sender_bot = Bot(token=config["bot"]["token"])
    monitor = ChannelMonitor(client, sender_bot, config, processor, logger)
    forward_bot = ForwardBot(
        config["bot"]["token"],
        config["channels"]["technical_channel"],
        config["channels"]["target_channels"],
    )

    await asyncio.gather(monitor.start(), forward_bot.start())


if __name__ == "__main__":
    asyncio.run(main())
