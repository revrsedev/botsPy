import configparser

class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def get_irc_settings(self):
        return (
            self.config.get('IRCSettings', 'server'),
            self.config.getint('IRCSettings', 'port'),
            self.config.get('IRCSettings', 'channel'),
            self.config.get('IRCSettings', 'bot_name'),
            [self.config.get('AuthorizedUsers', key) for key in self.config['AuthorizedUsers']]
        )

    def get_youtube_api_key(self):
        return self.config.get('YouTubeAPI', 'api_key')
