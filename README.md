# Discord Webhook Integration for Home Assistant

This is a custom integration for Home Assistant that allows you to send messages to Discord using webhooks. It supports both the legacy service and the new notification platform.

The reason this project was created is because I found the use of Discord webhooks to be so much easier than the official Home Assistant Discord integration.

At the time of writing this README, the entire integration was written by Windsurf AI.

ℹ️ There is a full README.md in the `custom_components/discord_webhook` directory.

## Installation

Copy the `discord_webhook` folder to your Home Assistant's `custom_components` directory (found in the `config` directory of your Home Assistant installation, if not, you need to create it).

## Configuration

### Option 1: Using the Notification Platform (Recommended)

```yaml
# Example configuration.yaml entry
notify:
  - name: discord
    platform: discord_webhook
    webhook_url: "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"
    username: "Home Assistant"  # Optional
    avatar_url: "https://www.home-assistant.io/images/favicon-192x192-full.png"  # Optional
    tts: false  # Optional, default false
```

### Option 2: Legacy Configuration

```yaml
# Legacy configuration (still supported)
discord_webhook:
  webhook_url: "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"
  username: "Home Assistant"  # Optional
  avatar_url: "https://www.home-assistant.io/images/favicon-192x192-full.png"  # Optional
  tts: false  # Optional, default false
```
