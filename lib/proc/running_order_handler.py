from pprint import pprint, pformat

from slack import WebClient

from lib.domain.domain_error import DomainError
from lib.domain.full_order import FullOrder
from lib.domain.individual_order import IndividualOrder
from lib.domain.taco import Taco
from lib.slack_impl.running_order_message import RunningOrderMessage

class RunningOrderError(DomainError):
    pass


class RunningOrderHandler:
    Order: FullOrder = None
    SlackClient: WebClient = None
    OrderIsRunning: bool = False
    ChannelId: str = None

    def __init__(self, slack_client: WebClient):
        if RunningOrderHandler.SlackClient is None:
            RunningOrderHandler.SlackClient = slack_client
        if RunningOrderHandler.Order is None:
            RunningOrderHandler.Order = FullOrder()

    @classmethod
    def start_order(cls, channel_id: str):
        cls.OrderIsRunning = True
        cls.ChannelId = channel_id

    @classmethod
    def end_order(cls):
        cls.OrderIsRunning = False
        cls.Order = FullOrder()

    @classmethod
    def add_order(cls, order: IndividualOrder):
        if cls.OrderIsRunning is False or cls.ChannelId is None:
            raise RunningOrderError(f'An order has not begun! No {"running order" if cls.OrderIsRunning is False else "channel ID"}!')

        if cls.Order.has_employee_order(order.slack_id()):
            cls.Order.update_order(order)
        else:
            cls.Order.add_order(order)

        if cls.OrderIsRunning:
            cls.update_running_order_message()
        else:
            cls.send_running_order_message()

    @classmethod
    def send_running_order_message(cls, channel_id: str, trigger_id: str):
        message = RunningOrderMessage()
        pprint(message)

        response = cls.SlackClient.chat_postMessage(channel=channel_id,
                                                    trigger_id=trigger_id,
                                                    blocks=message.get_message()['blocks'])
        pprint(response)


    @classmethod
    def update_running_order_message(cls):
        message = RunningOrderMessage(cls.Order)
        logger.debug(f'Running order message: {pformat(message)}')
        
