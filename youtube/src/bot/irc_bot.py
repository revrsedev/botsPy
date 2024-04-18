import irc.bot
import re
import requests
import isodate
import threading
import time
from src.module.youtube.youtube_bot import YouTubeBot
from src.config.configuration import ConfigManager
import datetime
from src.module.youtube.search_youtube import search_youtube
import sys

sys.path.append("/home/debian/irc/comlatina/bots_Py/youtube")

config_manager = ConfigManager()
server, port, channel, bot_name, authorized_users = config_manager.get_irc_settings()
api_key = config_manager.get_youtube_api_key()

class CustomYouTubeBot(YouTubeBot):
    def __init__(self):
        config_manager = ConfigManager()
        server, port, channel, self.bot_name, authorized_users = config_manager.get_irc_settings()
        api_key = config_manager.get_youtube_api_key()
        YouTubeBot.__init__(self, server, port, channel, self.bot_name, authorized_users, api_key)
        self.ping_thread = threading.Thread(target=self.ping_server, daemon=True)
        self.ping_thread.start()

    def ping_server(self):
        while True:
            if self.connection.is_connected():
                self.send_ping()
            time.sleep(200)  # Send PING 

    def send_ping(self):
        self.connection.ping("ping")
        
    def on_pong(self, connection, event):
        print("Received PONG response from server.")

    def on_welcome(self, connection, event):
        connection.join(self.channel)

    def on_privmsg(self, connection, event):
        nick = event.source.nick
        hostmask = event.source.host
        msg = event.arguments[0]

        if hostmask in self.authorized_users:
            if msg.startswith("!leave"):
                self.leave_channel(connection, event)  # Pass event to the method
            elif msg.startswith("!join"):
                self.join_channel(connection, event)   # Pass event to the method
        else:
            print(f"Unauthorized attempt by {hostmask} to use leave or join command.")

    def on_pubmsg(self, connection, event):
        msg = event.arguments[0]
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if msg.startswith("!search"):
            search_query = msg[len("!search "):].strip()
            video_url = search_youtube(search_query, self.api_key)
            formatted_message = f"\x02\x0301,00You\x0F\x02\x0300,04Tube\x0F Mejor resultado: {video_url}"
            connection.privmsg(self.channel, formatted_message)
        else:
            youtube_links = re.findall(self.youtube_pattern, msg)
            if youtube_links:
                self.process_youtube_links(connection, youtube_links, event.target)

    def leave_channel(self, connection, event):
        nick = event.source.nick
        hostmask = event.source.host
        if hostmask in self.authorized_users:
            channel_name = event.arguments[0].split()[1]
            connection.part(channel_name, f"Leaving channel {channel_name} requested by {nick}.")
            print(f"Leaving channel {channel_name}")
        else:
            print(f"Unauthorized attempt by {hostmask} to use leave command.")

    def join_channel(self, connection, event):
        nick = event.source.nick
        hostmask = event.source.host
        if hostmask in self.authorized_users:
            channel_name = event.arguments[0].split()[1]
            if channel_name in self.channels:
                connection.privmsg(nick, f"I'm already on {channel_name}.")
            else:
                connection.join(channel_name)
                self.channels[channel_name] = {}
                print(f"Joining channel {channel_name}")
        else:
            print(f"Unauthorized attempt by {hostmask} to use join command.")

    

