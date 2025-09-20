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

### Option 0: UI Config Flow (Recommended)

You can configure this integration entirely from the Home Assistant UI:

1. Go to: Settings > Devices & Services > Add Integration.
2. Search for and select "Discord Webhook".
3. Enter the details for the webhook:
   - Name (used for the service name)
   - Webhook URL (required)
   - Username (optional)
   - Avatar URL (optional)
   - TTS (optional)
4. Submit to create the entry.

Notes:
- Each config flow entry creates its own notify service, allowing you to maintain multiple distinct Discord webhooks (e.g., alerts vs. general updates).
- You can add multiple instances by repeating the above steps. Duplicate entries with the same `webhook_url` are prevented.

### Option 1: YAML — Multiple Webhooks

Configure multiple Discord webhooks in YAML. Each webhook will be available as a separate notification service.

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

### Option 2: YAML — Using the Notification Platform

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

### Option 3: YAML — Legacy Configuration (Single Webhook)

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

## YAML Import (How YAML becomes UI entries)

If you configure webhooks in `configuration.yaml` under `discord_webhook:`, they will be imported into the UI as Config Entries on startup or when the integration is reloaded. Behavior details:

- Each imported entry is normalized like the UI flow (optional empty strings become `null`, and `tts` defaults if omitted).
- Import uses the `webhook_url` as a unique identifier to prevent duplicates. If an entry with the same `webhook_url` already exists, it will be skipped.
- Invalid entries (e.g., `webhook_url` not starting with `http`) are safely ignored during import.

After import, you can manage these entries from Settings > Devices & Services > Integrations like any other UI-added instance.

## Showing the Discord icon locally (no external PRs)

Home Assistant displays integration icons/logos from the central brands service. If you prefer not to submit a PR to the official brands repository yet, you can still show the Discord icon locally using a HACS add-on like "custom-brand-icons" (or similar community tools).

This repository includes a scaffold for the required brand assets at:

- `assets/brands/discord_webhook/`

Expected PNG files (per Home Assistant brands spec):

- `icon.png` — 256x256, square
- `icon@2x.png` — 512x512, square
- `logo.png` — landscape; shortest side 256 px (max 256)
- `logo@2x.png` — landscape; shortest side 512 px (max 512)

Notes:

- The directory name must match the integration domain: `discord_webhook`.
- All files should be PNG, trimmed (minimal transparent padding), optimized, and preferably interlaced.
- If you only have the square Discord Clyde glyph, the icon can be used without logos; some tools will fall back to the icon when a logo is missing.

Using HACS custom-brand-icons (example):

1. Install HACS if not already installed.
2. Add and install the community repository for custom brand icons (follow their documentation).
3. Place the prepared images (`icon.png`, `icon@2x.png`, and optionally `logo*.png`) in the path expected by that tool (commonly under your Home Assistant `config/www/` directory). Refer to the tool's README for the exact path.
4. Restart Home Assistant and clear the browser cache. The Integrations UI tile for `discord_webhook` should display the Discord icon.

When you're ready to make the icon official, submit these files to the Home Assistant `brands` repository under `custom_integrations/discord_webhook/`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
