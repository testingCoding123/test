from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict

from telethon import TelegramClient, events
from telegram import Bot

from .processor import PostProcessor


class ChannelMonitor:
    """Monitor donor channels and forward processed posts."""

    def __init__(
        self,
        client: TelegramClient,
        bot: Bot,
        config: Dict[str, Any],
        processor: PostProcessor,
        logger: logging.Logger | None = None,
    ) -> None:
        self.client = client
        self.bot = bot
        self.processor = processor
        self.logger = logger or logging.getLogger("iherb_bot")
        self.donor_channels = config["channels"]["donor_channels"]
        self.technical_channel = config["channels"]["technical_channel"]
        self.filters = config["filters"]

    async def start(self) -> None:
        @self.client.on(events.NewMessage(chats=self.donor_channels))
        async def handler(event):
            text = event.raw_text
            if any(k in text.lower() for k in self.filters["exclude_keywords"]):
                return
            if not any(p in text for p in self.filters["include_patterns"]):
                return
            processed = self.processor.process(text)
            await self.bot.send_message(self.technical_channel, processed)

        await self.client.start()
        self.logger.info("monitor started", extra={"time": datetime.utcnow().isoformat()})
        await self.client.run_until_disconnected()
