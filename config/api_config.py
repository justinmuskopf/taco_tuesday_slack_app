from config.config_parser import TacoTuesdayConfigParser


class TacoTuesdayApiConfig(TacoTuesdayConfigParser):
    BaseApiUrl: str = None
    TTApiKey: str = None
    GithubApiToken: str = None
    GithubRepositoryUrl: str = None
    GithubUser: str = None

    def __init__(self):
        config = super().get_config('api')

        TacoTuesdayApiConfig.BaseApiUrl = config['baseUrl']
        TacoTuesdayApiConfig.TTApiKey = config['key']
        TacoTuesdayApiConfig.GithubUser = config['githubUser']
        TacoTuesdayApiConfig.GithubApiToken = config['githubApiToken']
        TacoTuesdayApiConfig.GithubRepositoryUrl = config['githubRepositoryUrl']

    def get_base_api_url(self):
        return self.BaseApiUrl

    def get_api_key(self):
        return self.TTApiKey

    def get_github_api_info(self):
        return {'user': TacoTuesdayApiConfig.GithubUser,
                'token': TacoTuesdayApiConfig.GithubApiToken,
                'url': TacoTuesdayApiConfig.GithubRepositoryUrl}
