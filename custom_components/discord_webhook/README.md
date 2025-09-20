# Discord Webhook Integration for Home Assistant

This is a custom integration for Home Assistant that allows you to send messages to Discord using webhooks. It supports both the legacy service and the new notification platform.

## Installation

1. Copy the `discord_webhook` folder to your Home Assistant's `custom_components` directory.
2. Restart Home Assistant.

## Configuration

### Option 0: UI Config Flow (Recommended)

You can configure this integration from the Home Assistant UI:

1. Go to: Settings > Devices & Services > Add Integration.
2. Search for and select "Discord Webhook".
3. Enter the details for the webhook:
   - Name (used to derive the notify service name)
   - Webhook URL (required)
   - Username (optional)
   - Avatar URL (optional)
   - TTS (optional)
4. Submit to create the entry.

Notes:
- Each config flow entry creates its own notify service, so you can maintain multiple distinct Discord webhooks (e.g., alerts vs. general updates).
- You can add multiple instances by repeating the above steps. Duplicate entries with the same `webhook_url` are prevented.

### Option 1: YAML — Multiple Webhooks

You can configure multiple Discord webhooks in YAML. Each webhook will be available as a separate notification service.

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

### Option 2: YAML — Single Webhook (Legacy)

For backward compatibility, a single webhook can still be configured using the legacy format:

```yaml
# Legacy configuration (still supported)
discord_webhook:
  webhook_url: "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"
  username: "Home Assistant"  # Optional
  avatar_url: "https://www.home-assistant.io/images/favicon-192x192-full.png"  # Optional
  tts: false  # Optional, default false
```

### Option 3: YAML — Using the Notification Platform

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

## Usage

### Using Multiple Webhooks

When you configure multiple webhooks, each one will be available as a separate service. The service name will be based on the webhook name:

```yaml
# Basic notification to a specific webhook
service: notify.discord_home_alerts  # Based on the 'name' in configuration
data:
  message: "This is a test message to the home alerts channel"
  title: "Important Alert"  # Optional

# Or for the second webhook
service: notify.discord_security_alerts
data:
  message: "Security alert triggered!"
  title: "🚨 Security Alert"

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

## YAML Import (How YAML becomes UI entries)

If you configure webhooks in `configuration.yaml` under `discord_webhook:`, they will be imported into the UI as Config Entries on startup or when the integration is reloaded.

Behavior details:
- Each imported entry is normalized like the UI flow (optional empty strings become `null`, and `tts` uses the default if omitted).
- Import uses the `webhook_url` as a unique identifier to prevent duplicates. If an entry with the same `webhook_url` already exists, it will be skipped.
- Invalid entries (e.g., `webhook_url` not starting with `http`) are safely ignored during import.

After import, you can manage these entries from Settings > Devices & Services > Integrations like any other UI-added instance.

### Service Details

#### Notification Service

When using the notification platform, each webhook will be available as `notify.[service_name]` where `[service_name]` is derived from the webhook name (lowercase, with spaces replaced by underscores).

| Service data attribute | Optional | Description |
|------------------------|----------|-------------|
| `message` | No | The message to send (max 2000 characters) |
| `title` | Yes | Message title (will be displayed in bold above the message) |
| `data` | Yes | Additional data (see below) |

#### Data Attributes

Additional options can be passed in the `data` dictionary:

| Attribute | Type | Description |
|-----------|------|-------------|
| `username` | string | Override the default username for this message |
| `avatar_url` | string | Override the default avatar URL for this message |
| `tts` | boolean | Whether to use text-to-speech (default: false) |
| `images` | list | List of image URLs to include in the message |
| `embeds` | list | List of Discord embeds (advanced) |

#### Legacy Service (discord_webhook.send_message)

For backward compatibility, the legacy service is still available but not recommended for new configurations.

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
