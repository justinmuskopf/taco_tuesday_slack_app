from config.config_parser import TacoTuesdayConfigParser


class TacoTuesdayApiConfig(TacoTuesdayConfigParser):
    BaseApiUrl: str = None
    TTApiKey: str = None

    def __init__(self):
        config = super().get_config('api')

        TacoTuesdayApiConfig.BaseApiUrl = config['baseUrl']
        TacoTuesdayApiConfig.TTApiKey = config['key']

    def get_base_api_url(self):
        return self.BaseApiUrl

    def get_api_key(self):
        return self.TTApiKey
