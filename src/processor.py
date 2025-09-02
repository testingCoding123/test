from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Any, Dict


IHERB_REF_PATTERN = re.compile(r"(?<=rcode=)[A-Z0-9]+")
CHANNEL_LINK_PATTERN = re.compile(r"t\.me/[A-Za-z0-9_]+")


class PostProcessor:
    """Process messages replacing referral and channel links."""

    def __init__(self, config: Dict[str, Any], logger: logging.Logger | None = None) -> None:
        self.referral_code = config["replacements"]["referral_code"]
        self.channel_link = config["replacements"]["channel_link"]
        self.signature = config["settings"].get("custom_signature", "")
        self.logger = logger or logging.getLogger("iherb_bot")

    def replace_iherb_links(self, text: str) -> str:
        return IHERB_REF_PATTERN.sub(self.referral_code, text)

    def replace_channel_links(self, text: str) -> str:
        return CHANNEL_LINK_PATTERN.sub(self.channel_link, text)

    def process(self, text: str) -> str:
        original = text
        text = self.replace_iherb_links(text)
        text = self.replace_channel_links(text)
        if self.signature:
            text += f"\n\n{self.signature}"
        if text != original:
            self.logger.info("links replaced", extra={"time": datetime.utcnow().isoformat()})
        return text
