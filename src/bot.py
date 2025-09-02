from __future__ import annotations

from typing import List

from telegram.ext import Application, MessageHandler, filters


class ForwardBot:
    """Forward messages from technical channel to target channels."""

    def __init__(self, token: str, technical_channel: str, target_channels: List[str]):
        self.application = Application.builder().token(token).build()
        self.technical_channel = technical_channel
        self.target_channels = target_channels
        self.application.add_handler(
            MessageHandler(filters.Chat(username=technical_channel), self._forward)
        )

    async def _forward(self, update, context):
        text = update.effective_message.text or ""
        for channel in self.target_channels:
            await context.bot.send_message(channel, text)

    async def start(self) -> None:
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        await self.application.updater.idle()
