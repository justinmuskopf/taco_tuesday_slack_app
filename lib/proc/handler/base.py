from slack import WebClient


class BaseHandler:
    SlackClient: WebClient = None

    def __init__(self, slack_client: WebClient):
        BaseHandler.SlackClient = slack_client
