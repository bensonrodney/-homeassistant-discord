"""The Discord Webhook integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PLATFORM, Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv, discovery
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_AVATAR_URL,
    CONF_NAME,
    CONF_TTS,
    CONF_USERNAME,
    CONF_WEBHOOKS,
    CONF_WEBHOOK_URL,
    DEFAULT_NAME,
    DEFAULT_TTS,
    DOMAIN,
    SERVICE_SEND_MESSAGE,
)

_LOGGER = logging.getLogger(__name__)

WEBHOOK_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_WEBHOOK_URL): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_USERNAME): cv.string,
        vol.Optional(CONF_AVATAR_URL): cv.url,
        vol.Optional(CONF_TTS, default=DEFAULT_TTS): cv.boolean,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            # Support legacy configuration format for backward compatibility
            vol.Any(
                WEBHOOK_SCHEMA,
                {vol.Required(CONF_WEBHOOKS): [WEBHOOK_SCHEMA]},
            )
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Discord Webhook component."""
    if DOMAIN not in config:
        return True
        
    conf = config[DOMAIN]
    
    # Handle both legacy and new configuration formats
    if CONF_WEBHOOKS in conf:
        webhooks = conf[CONF_WEBHOOKS]
    else:
        # Convert legacy config to new format
        webhooks = [conf]
    
    # Register each webhook as a notification service
    for webhook in webhooks:
        name = webhook[CONF_NAME]
        webhook_url = webhook[CONF_WEBHOOK_URL]
        username = webhook.get(CONF_USERNAME)
        avatar_url = webhook.get(CONF_AVATAR_URL)
        tts = webhook.get(CONF_TTS, DEFAULT_TTS)
        
        # Create a service for each webhook
        async def send_message_service(call: ServiceCall) -> None:
            """Handle sending messages to Discord webhook."""
            from .notify import DiscordNotificationService
            
            message = call.data.get("message")
            if not message:
                _LOGGER.error("No message provided in service call")
                return
                
            service_username = call.data.get("username", username)
            service_avatar_url = call.data.get("avatar_url", avatar_url)
            service_tts = call.data.get("tts", tts)
            
            service = DiscordNotificationService(
                name=name,
                webhook_url=webhook_url,
                username=service_username,
                avatar_url=service_avatar_url,
                tts=service_tts,
            )
            
            try:
                await service.async_send_message(message, **call.data)
            except Exception as err:
                _LOGGER.error("Error sending message: %s", err)
                raise
        
        # Set up the notify platform for this webhook
        hass.async_create_task(
            discovery.async_load_platform(
                hass,
                Platform.NOTIFY,
                DOMAIN,
                {
                    CONF_PLATFORM: DOMAIN,
                    CONF_NAME: name,
                    CONF_WEBHOOK_URL: webhook_url,
                    **({CONF_USERNAME: username} if username else {}),
                    **({CONF_AVATAR_URL: avatar_url} if avatar_url else {}),
                    **({CONF_TTS: tts} if tts != DEFAULT_TTS else {}),
                },
                config,
            )
        )

    return True
