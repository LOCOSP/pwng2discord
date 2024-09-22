import logging
import os
import requests # type: ignore
from pwnagotchi import plugins # type: ignore

class DiscordInfo(plugins.Plugin):
    __author__ = 'LOCOSP'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'Sends handshake info to a Discord webhook when a handshake is captured.'

    def __init__(self):
        self.ready = False

    def on_loaded(self):
        # Check if the plugin is enabled in the config
        if 'enabled' not in self.options or not self.options['enabled']:
            logging.info("DiscordInfo: Plugin is disabled in the config")
            return

        # Check if webhook_url is provided in config
        if 'webhook_url' not in self.options or not self.options['webhook_url']:
            logging.error("DiscordInfo: Webhook URL is not set, cannot post to Discord")
            return
        
        # Set the username from options or default to hostname
        if 'username' not in self.options or not self.options['username']:
            with open('/etc/hostname') as fp:
                self.options['username'] = fp.read().strip()

        self.ready = True
        logging.info("DiscordInfo: Plugin loaded and ready")

    def on_handshake(self, agent, filename, access_point, client_station):
        logging.info("DiscordInfo: handshake received")
        if self.ready and self.is_enabled():
            ssid = access_point["hostname"]
            bssid = access_point["mac"]
            message = f"New handshake captured for SSID: {ssid} (BSSID: {bssid})\nFile: {filename}"
            logging.info(f"DiscordInfo: Sending message to Discord: {message}")
            self.send_message(message)
        else:
            logging.warning("DiscordInfo: Plugin not ready or disabled, cannot send message")

    def is_enabled(self):
        # Check if the plugin is enabled in the config
        return 'enabled' in self.options and self.options['enabled']

    def send_message(self, message):
        try:
            url = self.options['webhook_url']
            username = self.options['username']  # Use the configurable username
            data = {
                "content": message,
                "username": username
            }
            response = requests.post(url, json=data)
            if response.status_code == 204:
                logging.info("DiscordInfo: Message successfully sent to Discord")
            else:
                logging.error(f"DiscordInfo: Failed to send message to Discord, status code: {response.status_code}, response: {response.text}")
        except requests.exceptions.RequestException as e:
            logging.exception(f"DiscordInfo: Exception occurred while sending the message: {e}")
        except Exception as e:
            logging.exception(f"DiscordInfo: Unexpected exception occurred: {e}")

    def on_unload(self):
        self.ready = False
        logging.info("DiscordInfo: Plugin unloaded")