from pprint import pprint, pformat
from loguru import logger
from slack import WebClient
from slack.errors import SlackApiError

from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.domain.domain_error import DomainError
from lib.domain.full_order import FullOrder
from lib.domain.individual_order import IndividualOrder
from lib.proc.handler.base import BaseHandler
from lib.proc.channel_validator import ChannelValidator, ChannelValidationError
from lib.slack_impl.message.completed_order import CompletedOrderMessage
from lib.slack_impl.message.running_order import RunningOrderMessage


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


class RunningOrderHandler(BaseHandler):
    TS: str = None
    RunningOrder: FullOrder = None
    OrderIsRunning: bool = False
    FirstMessageSent: bool = False
    ChannelId: str = None

    @classmethod
    def start_order(cls, channel_id: str):
        try:
            ChannelValidator.validate(channel_id)
        except ChannelValidationError:
            raise RunningOrderError(f'Could not validate channel: {channel_id}!')

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
    def remove_order(cls, slack_id: str):
        RunningOrderError.assert_order_is_running(True)
        cls.RunningOrder.remove_employee_order(slack_id)
        cls.update_running_order_message()

    @classmethod
    def has_employee_order(cls, slack_id):
        RunningOrderError.assert_order_is_running(True)
        return cls.RunningOrder.has_employee_order(slack_id)

    @classmethod
    def number_of_orders(cls):
        RunningOrderError.assert_order_is_running(True)
        return len(cls.RunningOrder.individual_orders)

    @classmethod
    def send_running_order_message(cls):
        RunningOrderError.assert_first_message_sent(False)
        RunningOrderError.assert_order_is_running(True)

        response = cls.SlackClient.chat_postMessage(channel=cls.ChannelId,
                                                    text='<!here> I go, taking orders again!')
        assert response['ok']

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

        cls.FirstMessageSent = True

    @classmethod
    def _update_message(cls, blocks):
        response = cls.SlackClient.chat_update(channel=cls.ChannelId,
                                               ts=cls.TS,
                                               blocks=blocks)

        assert response['ok']

    @classmethod
    def update_running_order_message(cls):
        RunningOrderError.assert_first_message_sent(True)

        message = RunningOrderMessage(cls.RunningOrder)

        cls._update_message(message.get_blocks())

        logger.info("Updated existing RunningOrderMessage!")

    @classmethod
    def submit_order(cls):
        RunningOrderError.assert_order_is_running(True)
        logger.info('Submitting Running Order!')

        TacoTuesdayApiHandler.submit_order(cls.RunningOrder)

        logger.debug(f'Submitted Order: {pformat(cls.RunningOrder.get_dict())}')

        completed_message = CompletedOrderMessage(cls.RunningOrder)

        cls._update_message(completed_message.get_blocks())

        cls.end_order()
