import logging, requests, pwnagotchi, os, glob, time, re, json
from pwnagotchi import plugins

class DiscordInfo(plugins.Plugin):
    __author__ = 'locospnoreply@gmail.com'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'Sends handshake info to a Discord webhook when a handshake is captured.'

    def __init__(self):
        self.ready = False

    def on_config_changed(self, config):
        self.config = config
        
    def on_ready(self, agent):
        if 'webhook_url' not in self.options or not self.options['webhook_url']:
            logging.error("DiscordInfo: Webhook URL is not set, cannot post to Discord")
            return
        if 'username' not in self.options or not self.options['username']:
            with open('/etc/hostname') as fp:
                self.options['username'] = fp.read().strip()
        self.ready = True
        logging.info("DiscordInfo: Plugin loaded and ready")

    def on_handshake(self, agent, filename, access_point, client_station):
        logging.info("DiscordInfo: Handshake received")
        if not self.ready:
            logging.warning("DiscordInfo: Plugin not ready or disabled, cannot send message")
            return
        ssid = access_point.get("hostname", "Unknown SSID")
        bssid = access_point.get("mac", "Unknown BSSID")
        message = f"New handshake captured for SSID: {ssid} (BSSID: {bssid})\nFile: {filename}"
        time.sleep(2)
        logging.debug(f"DiscordInfo: Sending message to Discord: {message}")
        handshake_base = os.path.splitext(filename)[0]
        h22000_files = glob.glob(f"{handshake_base}*.22000")
        if not h22000_files:
            logging.debug(f"DiscordInfo: No matching .22000 file found for {filename}")
        else:
            h22000_filepath = h22000_files[0]
            message = f"New handshake captured for SSID: {ssid} (BSSID: {bssid})\nFile: {h22000_filepath}"
            logging.debug(f"DiscordInfo: Found matching .22000 file: {h22000_filepath}")
        lat, lng, google_maps_link = self._get_location_info(ssid, bssid)
        if google_maps_link:
            message += f"\nLocation: [{lat}, {lng}](<{google_maps_link}>)"
            logging.debug(f"DiscordInfo: Added location data to message: {google_maps_link}")
        else:
            logging.debug("DiscordInfo: No location data found, not adding to message.")
        self.send_message(message, ssid, bssid, h22000_filepath, filename)

    def send_message(self, message, ssid, bssid, filename, filepath=None):
        try:
            url = self.options['webhook_url']
            username = self.options['username']

            # Webhook data with embedded content
            data = {
                "username": username,
                "embeds": [
                    {
                        "title": "🚨 New 🤝 handshake captured! 🚨",
                        "description": "**Handshake Details:**\n\n🔐 **File**: " + filename + "\n\n",
                        "color": 16753920, 
                        "fields": [
                            {
                                "name": "📡 SSID",
                                "value": ssid,
                                "inline": True
                            },
                            {
                                "name": "⚙️ BSSID",
                                "value": bssid,
                                "inline": True
                            },
                            {
                                "name": "🏴‍☠️ Location",
                                "value": "comming soon",
                                "inline": True
                            }
                        ],
                        "footer": {
                            "text": "pwng2discord (^‿‿^) powered by Pwnagotchi",
                            "icon_url": "https://www.pwnagotchi.com/cdn/shop/files/pwnagotchishop_Icon_1589a659-8ed6-4c50-b511-34cf195c8671.png"
                        }
                    }
                ]
            }

            if filepath and os.path.exists(filepath):
                with open(filepath, 'rb') as file:
                    files = {
                        'file': (os.path.basename(filepath), file, 'application/octet-stream')
                    }
                    response = requests.post(url, data={"payload_json": json.dumps(data)}, files=files)
            else:
                response = requests.post(url, json=data)

            if response.status_code in [200, 204]:
                logging.debug("DiscordInfo: Message successfully sent to Discord")
            else:
                logging.error(f"DiscordInfo: Failed to send message to Discord, status code: {response.status_code}, response: {response.text}")
        except requests.exceptions.RequestException as e:
            logging.exception(f"DiscordInfo: Exception occurred while sending the message: {e}")
        except Exception as e:
            logging.exception(f"DiscordInfo: Unexpected exception occurred: {e}")


            
    def _get_location_info(self, ssid, bssid):
        ssid = re.sub(r'\W+', '', ssid)
        bssid = bssid.replace(':', '')
        geojson_file = f"{self.config['bettercap']['handshakes']}{ssid}_{bssid}.gps.json"
        if os.path.exists(geojson_file):
            logging.debug(f"DiscordInfo: Found geo.json file: {geojson_file}")
            with open(geojson_file, 'r') as geo_file:
                data = json.load(geo_file)
            if data is not None:
                lat = data.get('Latitude') or data.get('location', {}).get('lat')
                lng = data.get('Longitude') or data.get('location', {}).get('lng')
                if lat is not None and lng is not None:
                    google_maps_link = f"https://www.google.com/maps?q={lat},{lng}"
                    return lat, lng, google_maps_link
        logging.info(f"DiscordInfo: No location information found for SSID: {ssid}, BSSID: {bssid}")
        return None, None, None

    def on_unload(self, ui):
        self.ready = False
        logging.info("DiscordInfo: Plugin unloaded")