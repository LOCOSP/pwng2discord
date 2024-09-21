import logging
import os
import requests
from pwnagotchi import plugins


class DiscordInfo(plugins.Plugin):
    __author__ = 'LOCOSP'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'Sends handshake info to a Discord webhook when a handshake is captured.'

    def __init__(self):
        self.ready = False

    def on_loaded(self):

        if 'enabled' not in self.options or not self.options['enabled']:
            logging.info("DiscordInfo: Plugin is disabled in the config")
            return


        if 'webhook_url' not in self.options or not self.options['webhook_url']:
            logging.error("DiscordInfo: Webhook URL is not set, cannot post to Discord")
            return
        

        if 'username' not in self.options or not self.options['username']:
            with open('/etc/hostname') as fp:
                self.options['username'] = fp.read().strip()

        self.ready = True
        logging.info("DiscordInfo: Plugin loaded and ready")

    def on_handshake(self, agent, filename, access_point, client_station):
        if not self.ready or not self.is_enabled():
            logging.warning("DiscordInfo: Plugin not ready or disabled, cannot send message")
            return


        ssid = access_point["essid"]
        bssid = access_point["mac"]
        message = f"New handshake captured for SSID: {ssid} (BSSID: {bssid})\nFile: {filename}"

        logging.info(f"DiscordInfo: Sending message to Discord: {message}")

        self.send_message(message)

    def is_enabled(self):

        return 'enabled' in self.options and self.options['enabled']

    def send_message(self, message):
        try:
            url = self.options['webhook_url']
            username = self.options['username']  
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
        logging.info("DiscordInfo: Plugin unloaded")