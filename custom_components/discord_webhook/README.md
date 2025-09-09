# Discord Webhook Integration for Home Assistant

This is a custom integration for Home Assistant that allows you to send messages to Discord using webhooks. It supports both the legacy service and the new notification platform.

## Installation

1. Copy the `discord_webhook` folder to your Home Assistant's `custom_components` directory.
2. Restart Home Assistant.

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

## Usage

### Using the Notification Service (Recommended)

```yaml
# Basic notification
service: notify.discord
data:
  message: "This is a test message"
  title: "Important Alert"  # Optional

# Notification with images
service: notify.discord
data:
  message: "Check out these images!"
  data:
    images:
      - "https://example.com/image1.jpg"
      - "https://example.com/image2.jpg"

# Custom username and avatar for a specific message
service: notify.discord
data:
  message: "Custom message"
  data:
    username: "Custom Bot"
    avatar_url: "https://example.com/avatar.png"
    tts: true  # Enable text-to-speech
```

### Legacy Service (discord_webhook.send_message)

| Service data attribute | Optional | Description |
|------------------------|----------|-------------|
| `message` | No | The message to send |
| `username` | Yes | Override the default username |
| `avatar_url` | Yes | Override the default avatar URL |
| `tts` | Yes | Whether to use text-to-speech (default: false) |
| `data` | Yes | Additional data including `images` and `embeds` |

### Example Automations

```yaml
# Example automation using the notification platform
automation:
  - alias: "Front door opened notification"
    trigger:
      platform: state
      entity_id: binary_sensor.front_door
      to: 'on'
    action:
      service: notify.discord
      data:
        title: "🚪 Door Alert"
        message: "Front door has been opened!"

# Send daily summary with images
automation:
  - alias: "Daily summary"
    trigger:
      platform: time
      at: "09:00:00"
    action:
      service: notify.discord
      data:
        message: "🌅 Good morning! Here's your daily summary."
        data:
          images:
            - "https://example.com/weather.png"
            - "https://example.com/calendar.png"
```

## Advanced Usage

### Sending Embeds

You can send rich embeds using the `embeds` field in the `data` parameter. Here's an example:

```yaml
service: notify.discord
data:
  message: "Check out this embed!"
  data:
    embeds:
      - title: "Embed Title"
        description: "This is a rich embed"
        color: 5814783
        fields:
          - name: "Field 1"
            value: "Value 1"
            inline: true
          - name: "Field 2"
            value: "Value 2"
            inline: true
```

## Troubleshooting

If messages are not being sent, check the Home Assistant logs for any error messages. Common issues include:
- Incorrect webhook URL
- Network connectivity issues
- Discord rate limiting (max 2000 messages per 10 minutes per webhook)
- Missing required permissions for the webhook

## License

This project is licensed under the MIT License - see the LICENSE file for details.
