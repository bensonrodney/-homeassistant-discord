"""Support for Discord Webhook notifications."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_TITLE,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
from homeassistant.const import CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    ATTR_EMBEDS,
    ATTR_IMAGES,
    CONF_AVATAR_URL,
    CONF_TTS,
    CONF_WEBHOOK_URL,
    DEFAULT_TTS,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_WEBHOOK_URL): cv.string,
        vol.Optional(CONF_USERNAME): cv.string,
        vol.Optional(CONF_AVATAR_URL): cv.url,
        vol.Optional(CONF_TTS, default=DEFAULT_TTS): cv.boolean,
    }
)


def get_service(
    hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> DiscordNotificationService:
    """Get the Discord notification service."""
    return DiscordNotificationService(
        webhook_url=config[CONF_WEBHOOK_URL],
        username=config.get(CONF_USERNAME),
        avatar_url=config.get(CONF_AVATAR_URL),
        tts=config[CONF_TTS],
    )


class DiscordNotificationService(BaseNotificationService):
    """Implement the notification service for Discord."""

    def __init__(
        self,
        webhook_url: str,
        username: str | None = None,
        avatar_url: str | None = None,
        tts: bool = DEFAULT_TTS,
    ) -> None:
        """Initialize the service."""
        self._webhook_url = webhook_url
        self._username = username
        self._avatar_url = avatar_url
        self._tts = tts

    async def async_send_message(self, message: str, **kwargs: Any) -> None:
        """Send a message to a Discord webhook."""
        title = kwargs.get(ATTR_TITLE)
        data = kwargs.get(ATTR_DATA) or {}
        
        # Build the message content
        if title:
            text = f"**{title}**\n{message}"
        else:
            text = message
            
        payload = {
            "content": text,
            "tts": data.get(CONF_TTS, self._tts),
        }

        # Add optional parameters
        if self._username:
            payload["username"] = self._username
        if self._avatar_url:
            payload["avatar_url"] = self._avatar_url
            
        # Handle embeds if provided
        if ATTR_EMBEDS in data:
            payload["embeds"] = data[ATTR_EMBEDS]
            
        # Handle images if provided (as URLs)
        if ATTR_IMAGES in data:
            if "embeds" not in payload:
                payload["embeds"] = []
            for image_url in data[ATTR_IMAGES]:
                payload["embeds"].append({"image": {"url": image_url}})

        # Send the request
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self._webhook_url, json=payload) as response:
                    if response.status != 204:
                        response_text = await response.text()
                        _LOGGER.error(
                            "Error sending message: %s (Status: %s)",
                            response_text,
                            response.status,
                        )
            except aiohttp.ClientError as err:
                _LOGGER.error("Error sending message: %s", err)
