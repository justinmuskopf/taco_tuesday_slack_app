import os
import random

from loguru import logger
from slack import WebClient
from flask import make_response, json

from lib.proc.handler.base import BaseHandler
from lib.slack_impl.message.error import ErrorMessage


class ErrorHandler(BaseHandler):
    DEBUG_CHANNEL = os.environ['SLACK_DEBUG_CHANNEL']
    RESPONSES = [
        "Mr. Stark, I don't feel so good...",
        "Uh-oh, something went horribly wrong!",
        "Something went wrong. I don't want to tacobout it."
    ]

    @classmethod
    def handle(cls, e: Exception):
        logger.error(f'(ErrorHandler) Handling Exception: {e}')

        msg = ErrorMessage(e)
        cls.SlackClient.chat_postMessage(channel=cls.DEBUG_CHANNEL,
                                         blocks=msg.blocks)

        logger.debug(json.dumps(msg.blocks))
        return make_response(cls.response_string(), 200)

    @classmethod
    def response_string(cls):
        return random.choice(cls.RESPONSES)
