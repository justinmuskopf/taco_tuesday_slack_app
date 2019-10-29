from loguru import logger
from slack import WebClient
from slack.errors import SlackApiError

from lib.domain.domain_error import DomainError


class ChannelValidationError(DomainError):
    def __init__(self, channel_id: str):
        super().__init__(ChannelValidator, f'No public or private channel for ID {channel_id}! Is the bot allowed there?')


class ChannelValidator:
    Instance = None
    SlackClient: WebClient = None

    def __init__(self, slack_client: WebClient):
        if ChannelValidator.SlackClient is None:
            ChannelValidator.SlackClient = slack_client

        if ChannelValidator.Instance is None:
            ChannelValidator.Instance = self

    @classmethod
    def instance(cls, slack_client: WebClient = None):
        return cls.Instance or ChannelValidator(slack_client)

    @classmethod
    def validate(cls, channel_id: str):
        try:
            cls.SlackClient.conversations_info(channel=channel_id)
        except SlackApiError:
            ChannelValidationError(channel_id)

        return True
