Here's the revised `README.md` without sensitive information:

---

# DiscordInfo Plugin for Pwnagotchi

The `DiscordInfo` plugin sends a notification to a Discord channel using a webhook whenever a Wi-Fi handshake is captured by Pwnagotchi. It can also send location data if GPS information is available. This plugin enhances your Pwnagotchi experience by providing real-time updates on captured handshakes.

## Features

- Sends a Discord notification when a handshake is captured.
- Includes the SSID and BSSID of the network.
- Optionally attaches the `.22000` handshake file.
    
    this option requires aditional [plugin](https://github.com/PwnPeter/pwnagotchi-plugins/blob/master/hashie-hcxpcapngtool.py) !
- Sends GPS location if available for the network.

## Prerequisites

- A working Pwnagotchi device - best 64bit.
- A Discord account with a webhook URL for your channel.
- Internet access on your Pwnagotchi for sending notifications.

## Installation

1. When on Jayofelony's Image clone the `DiscordInfo` plugin repository into your Pwnagotchi custom-plugins directory:
    ```bash
    cd /usr/local/share/pwnagotchi/custom-plugins

    sudo git clone https://github.com/LOCOSP/pwng2discord.git
    ```
    or
    ```bash
    cd /usr/local/share/pwnagotchi/custom-plugins

    sudo wget https://raw.githubusercontent.com/LOCOSP/pwng2discord/refs/heads/main/discord-info.py
    ```

2. Edit the Pwnagotchi `config.toml` file to add the configuration for the `DiscordInfo` plugin:
    ```bash
    sudo nano /etc/pwnagotchi/config.toml
    ```

3. Add the following lines to your `config.toml`:
    ```toml
    # DiscordInfo Plugin Configuration
    main.plugins.discord-info.enabled = true
    main.plugins.discord-info.webhook_url = "your-discord-webhook-url"
    main.plugins.discord-info.username = "PwnagotchiBot"  # Optional, defaults to hostname
    ```

4. Restart your Pwnagotchi to apply the changes:
    ```bash
    sudo systemctl restart pwnagotchi
    ```
    or
    ```bash
    pwnkill
    ```

## How It Works

- **on_handshake**: This callback is triggered whenever a handshake is captured. It sends a message to your Discord channel with the SSID, BSSID, and optionally the `.22000` file and GPS location if available.
  
- **on_internet_available**: The plugin waits until there is an active internet connection before sending a notification to avoid errors when offline.

## Configuration

You can configure the following settings in your `config.toml`:

- `webhook_url`: Your Discord webhook URL where the notifications will be sent.
- `username`: The bot username that will appear in the Discord message. If not specified, the hostname of your Pwnagotchi will be used.

### Example Configuration in `config.toml`
```toml
main.plugins.discord-info.enabled = true
main.plugins.discord-info.webhook_url = "your-discord-webhook-url"
main.plugins.discord-info.username = "PwnagotchiBot"
```

## Troubleshooting

- **Logs**: To check the logs of the `DiscordInfo` plugin, use the following command:
    ```bash
    tail -f /etc/pwnagotchi/log/pwnagotchi.log | grep Discord
    ```
    or

    ```bash
    pwnlog
    ```

- **No notifications**: Ensure your Pwnagotchi has internet access when handshakes are captured. The plugin will not send notifications if there is no active connection.

## License

This plugin is licensed under GPL3.

## Authors

- **LOCOSP** - *Initial work* - [LOCOSP]
- **NeonLightnig** - most powerups and features - [NeonLightning repo](https://github.com/NeonLightning)
