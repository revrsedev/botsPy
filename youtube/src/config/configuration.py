import configparser

class ConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_irc_settings(self):
        server = self.config.get('IRCSettings', 'server')
        port = self.config.getint('IRCSettings', 'port')
        channel = self.config.get('IRCSettings', 'channel')
        bot_name = self.config.get('IRCSettings', 'bot_name')
        authorized_users = [self.config.get('AuthorizedUsers', key) for key in self.config['AuthorizedUsers']]
        return server, port, channel, bot_name, authorized_users

    def get_youtube_api_key(self):
        return self.config.get('YouTubeAPI', 'api_key')

