from src.bot.irc_bot import CustomYouTubeBot
from src.config.configuration import ConfigManager

def main():
    config_manager = ConfigManager()
    irc_settings = config_manager.get_irc_settings()
    server, port, channel, bot_name, password = irc_settings
    api_key = config_manager.get_youtube_api_key()
    bot = CustomYouTubeBot(server, port, channel, bot_name, api_key=api_key, password=password)
    bot.start()

if __name__ == "__main__":
    main()


