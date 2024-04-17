from src.module.youtube.youtube_bot import YouTubeBot
from src.config.configuration import ConfigManager

config_manager = ConfigManager()
server, port, channel, bot_name, authorized_users = config_manager.get_irc_settings()
api_key = config_manager.get_youtube_api_key()

class CustomYouTubeBot(YouTubeBot):
    def __init__(self):
        if api_key:
            super().__init__(server, port, channel, bot_name, api_key)
        else:
            super().__init__(server, port, channel, bot_name)
        self.channels = {}

    def on_privmsg(self, connection, event):
        nick = event.source.nick
        hostmask = event.source.host
        msg = event.arguments[0]

        if hostmask in self.authorized_users:
            if msg.startswith("!leave"):
                self.leave_channel(connection, event, hostmask)  # Pass hostmask to the method
            elif msg.startswith("!join"):
                self.join_channel(connection, event, hostmask)   # Pass hostmask to the method
        else:
            print(f"Unauthorized attempt by {hostmask} to use leave or join command.")

    def leave_channel(self, connection, event, hostmask):
        nick = event.source.nick
        if hostmask in self.authorized_users:
            channel_name = event.arguments[0].split()[1]
            connection.part(channel_name, f"Leaving channel {channel_name} requested by {nick}.")
            print(f"Leaving channel {channel_name}")
        else:
            print(f"Unauthorized attempt by {hostmask} to use leave command.")

    def join_channel(self, connection, event, hostmask):
        nick = event.source.nick
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

def main():
    bot = CustomYouTubeBot()
    bot.start()

if __name__ == "__main__":
    main()
