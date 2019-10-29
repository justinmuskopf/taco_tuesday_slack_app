import json
import os
import threading

from slack import WebClient
from loguru import logger
from lib.api.taco_tuesday_api_handler import TacoTuesdayApiHandler
from lib.domain.domain_error import DomainError
from lib.domain.taco import Taco
from lib.proc.handler.base import BaseHandler
from lib.proc.handler.feedback import FeedbackHandler
from lib.proc.handler.running_order import RunningOrderHandler
from lib.slack.modal.modal import Modal
from lib.slack_impl.modal.feedback import FeedbackModal
from lib.slack_impl.modal.order_cancel import OrderCancelModal
from lib.slack_impl.modal.order_submit import OrderSubmitModal
from lib.slack_impl.modal.taco_order import TacoOrderModal
from lib.proc.view_parser import ViewParser
from pprint import pformat


class ViewHandler(BaseHandler):
    TACOS: [Taco] = TacoTuesdayApiHandler.get_tacos_from_api()
    ViewParser: ViewParser = ViewParser()

    @staticmethod
    def is_view_interaction(interaction):
        if 'type' not in interaction: return False

        return interaction['type'] == 'view_submission'

    @classmethod
    def handle_submission(cls, view_submission: {}):
        logger.debug(json.dumps(view_submission))

        logger.debug(f'Given view: {view_submission}')
        callback_id = view_submission['view']['callback_id']
        slack_id = view_submission['user']['id']

        if TacoOrderModal.is_taco_order_submission(callback_id):
            order = cls.ViewParser.parse_submission_into_individual_order(view_submission)
            RunningOrderHandler.add_order(order)
        elif OrderSubmitModal.is_order_submit_submission(callback_id):
            logger.warning('Handling forced Order submission!')
            RunningOrderHandler.submit_order()
        elif OrderCancelModal.is_order_cancel_submission(callback_id):
            RunningOrderHandler.remove_order(slack_id)
        elif FeedbackModal.is_feedback_submission(callback_id):
            feedback = cls.ViewParser.parse_submission_into_feedback(view_submission)
            FeedbackHandler.handle(feedback)

    @classmethod
    def handle(cls, view: {}):
        logger.debug(f'View type: {view["type"]}')
        if view['type'] == 'view_submission': cls.handle_submission(view)

    @classmethod
    def send_modal(cls, trigger_id: str, modal: Modal):
        logger.debug(f'Sending Modal: {pformat(modal.get_modal())}')
        response = cls.SlackClient.views_open(trigger_id=trigger_id, view=modal.get_modal())
        assert response['ok']

    @classmethod
    def send_new_taco_order_modal(cls, trigger_id: str):
        cls.send_modal(trigger_id, TacoOrderModal())

    @classmethod
    def send_order_submit_modal(cls, trigger_id: str):
        cls.send_modal(trigger_id, OrderSubmitModal())

    @classmethod
    def send_order_cancel_modal(cls, trigger_id: str):
        cls.send_modal(trigger_id, OrderCancelModal())

    @classmethod
    def send_feedback_modal(cls, trigger_id: str):
        cls.send_modal(trigger_id, FeedbackModal())
