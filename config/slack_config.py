from config.config_parser import TacoTuesdayConfigParser


class TacoTuesdaySlackConfig(TacoTuesdayConfigParser):
    DebugChannel: str = None
    BotToken: str = None

    def __init__(self):
        config = TacoTuesdayConfigParser.Yaml['slack']

        TacoTuesdaySlackConfig.DebugChannel = config['debugChannel']
        TacoTuesdaySlackConfig.BotToken = config['botToken']

    def get_debug_channel(self):
        return self.DebugChannel

    def get_bot_token(self):
        return self.BotToken
