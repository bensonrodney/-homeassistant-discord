"""The Discord Webhook integration."""
from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PLATFORM, Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_AVATAR_URL,
    CONF_TTS,
    CONF_USERNAME,
    CONF_WEBHOOK_URL,
    DEFAULT_TTS,
    DOMAIN,
    SERVICE_SEND_MESSAGE,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_WEBHOOK_URL): cv.string,
                vol.Optional(CONF_USERNAME): cv.string,
                vol.Optional(CONF_AVATAR_URL): cv.url,
                vol.Optional(CONF_TTS, default=DEFAULT_TTS): cv.boolean,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Discord Webhook component."""
    # Only set up the legacy service if configured in configuration.yaml
    if DOMAIN not in config:
        return True
        
    conf = config[DOMAIN]
    webhook_url = conf[CONF_WEBHOOK_URL]
    default_username = conf.get(CONF_USERNAME)
    default_avatar_url = conf.get(CONF_AVATAR_URL)
    tts = conf.get(CONF_TTS, DEFAULT_TTS)

    async def send_message_service(call: ServiceCall) -> None:
        """Handle sending messages to Discord (legacy service)."""
        from .notify import DiscordNotificationService
        
        message = call.data["message"]
        username = call.data.get("username", default_username)
        avatar_url = call.data.get("avatar_url", default_avatar_url)
        tts = call.data.get("tts", tts)
        
        service = DiscordNotificationService(
            webhook_url=webhook_url,
            username=username,
            avatar_url=avatar_url,
            tts=tts,
        )
        
        await service.async_send_message(message, **call.data)

    # Register the legacy service
    hass.services.async_register(
        DOMAIN,
        SERVICE_SEND_MESSAGE,
        send_message_service,
        schema=vol.Schema(
            {
                vol.Required("message"): cv.string,
                vol.Optional("username"): cv.string,
                vol.Optional("avatar_url"): cv.url,
                vol.Optional("tts"): cv.boolean,
                vol.Optional("data"): dict,
            }
        ),
    )

    # Set up the notify platform
    hass.async_create_task(
        hass.helpers.discovery.async_load_platform(
            Platform.NOTIFY, DOMAIN, {CONF_PLATFORM: DOMAIN, **conf}, config
        )
    )

    return True
