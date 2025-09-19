# Discord Webhook Integration for Home Assistant

A powerful Home Assistant integration for sending rich notifications to Discord using webhooks. This integration supports multiple webhooks, rich embeds, images, and more.

## Features

- 🚀 **Multiple Webhooks** - Configure multiple Discord webhooks with different settings
- 📱 **Rich Notifications** - Send formatted messages with titles, images, and embeds
- 🔔 **Flexible Configuration** - Multiple configuration options to suit your needs
- 🔄 **Backward Compatible** - Supports legacy configuration format

## Installation

1. Copy the `discord_webhook` folder to your Home Assistant's `custom_components` directory (found in the `config` directory of your Home Assistant installation).
2. Restart Home Assistant to load the integration.

## Configuration

### Option 1: Multiple Webhooks (Recommended)

Configure multiple Discord webhooks, each with its own settings. Each webhook will be available as a separate notification service.

```yaml
# Example configuration.yaml entry
discord_webhook:
  webhooks:
    - name: "Home Alerts"  # Optional, defaults to "Discord Webhook"
      webhook_url: "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"
      username: "Home Assistant"  # Optional
      avatar_url: "https://www.home-assistant.io/images/favicon-192x192-full.png"  # Optional
      tts: false  # Optional, default false
    - name: "Security Alerts"
      webhook_url: "https://discord.com/api/webhooks/another_webhook_id/another_token"
      username: "Home Security"
```

### Option 2: Using the Notification Platform

You can also configure webhooks directly in the notify platform:

```yaml
notify:
  - name: discord_alerts
    platform: discord_webhook
    webhook_url: "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"
    username: "Home Assistant"  # Optional
    avatar_url: "https://www.home-assistant.io/images/favicon-192x192-full.png"  # Optional
    tts: false  # Optional, default false
```

### Option 3: Legacy Configuration (Single Webhook)

For backward compatibility, a single webhook can still be configured:

```yaml
discord_webhook:
  webhook_url: "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"
  username: "Home Assistant"  # Optional
  avatar_url: "https://www.home-assistant.io/images/favicon-192x192-full.png"  # Optional
  tts: false  # Optional, default false
```

## Basic Usage

Send a notification to a specific webhook:

```yaml
service: notify.discord_home_alerts  # Based on the 'name' in configuration
data:
  message: "This is a test message to the home alerts channel"
  title: "Important Alert"  # Optional
```

## Documentation

For complete documentation, including advanced features like embeds, images, and automation examples, please see the [full documentation](custom_components/discord_webhook/README.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
