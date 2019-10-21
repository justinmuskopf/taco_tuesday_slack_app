from pprint import pprint, pformat
from loguru import logger
from slack import WebClient
from slack.errors import SlackApiError

from lib.domain.domain_error import DomainError
from lib.domain.full_order import FullOrder
from lib.domain.individual_order import IndividualOrder
from lib.slack_impl.running_order_message import RunningOrderMessage


class RunningOrderError(DomainError):
    def __init__(self, message: str):
        super().__init__(RunningOrderHandler, message)

    @classmethod
    def assert_order_is_running(cls, should_be):
        if RunningOrderHandler.OrderIsRunning is not should_be:
            raise RunningOrderError(f'There is {"no" if should_be else "already an"} ongoing order!')

    @classmethod
    def assert_first_message_sent(cls, should_be):
        cls.assert_order_is_running(True)
        if RunningOrderHandler.FirstMessageSent is not should_be:
            raise RunningOrderError(f'First message {"has not" if should_be else "has already"} been sent!')


class RunningOrderHandler:
    TS: str = None
    RunningOrder: FullOrder = None
    SlackClient: WebClient = None
    OrderIsRunning: bool = False
    FirstMessageSent: bool = False
    ChannelId: str = None

    def __init__(self, slack_client: WebClient):
        if RunningOrderHandler.SlackClient is None:
            RunningOrderHandler.SlackClient = slack_client

    @classmethod
    def start_order(cls, channel_id: str):
        try:
            cls.SlackClient.channels_info(channel=channel_id)
        except SlackApiError:
            raise RunningOrderError(f'Invalid channel ID: {channel_id} !')

        cls.RunningOrder = FullOrder()
        cls.OrderIsRunning = True
        cls.ChannelId = channel_id

    @classmethod
    def end_order(cls):
        cls.OrderIsRunning = False
        cls.FirstMessageSent = False
        cls.RunningOrder = FullOrder()

    @classmethod
    def add_order(cls, order: IndividualOrder):
        RunningOrderError.assert_order_is_running(True)

        if not cls.FirstMessageSent:
            cls.send_running_order_message()

        if cls.RunningOrder.has_employee_order(order.slack_id):
            cls.RunningOrder.update_order(order)
        else:
            cls.RunningOrder.add_order(order)

        cls.update_running_order_message()

    @classmethod
    def send_running_order_message(cls):
        RunningOrderError.assert_first_message_sent(False)
        RunningOrderError.assert_order_is_running(True)

        message = RunningOrderMessage()
        pprint(message)

        response = cls.SlackClient.chat_postMessage(channel=cls.ChannelId,
                                                    blocks=message.get_blocks())
        try:
            cls.TS = response['message']['ts']
            logger.debug(f'Running Order TS: {cls.TS}')
        except KeyError as ke:
            return logger.error(f'ERROR: Invalid response received: {ke}')

        logger.info("Created new RunningOrderMessage!")
        #logger.debug(f'New running order response: {pformat(str(response))}')

        cls.FirstMessageSent = True

    @classmethod
    def update_running_order_message(cls):
        RunningOrderError.assert_first_message_sent(True)

        message = RunningOrderMessage(cls.RunningOrder)
        logger.debug(f'Running order message: {pformat(message)}')

        response = cls.SlackClient.chat_update(channel=cls.ChannelId,
                                               ts=cls.TS,
                                               blocks=message.get_blocks())

        logger.info("Updated existing RunningOrderMessage!")
        #logger.debug(f'Updated running order response: {pformat(str(response))}')
