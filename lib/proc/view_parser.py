import os

from loguru import logger

from config.order_config import TacoTuesdayOrderConfig
from lib.domain.domain_error import DomainError
from lib.domain.employee import Employee
from lib.domain.feedback import Feedback
from lib.proc.handler.employee import EmployeeHandler
from lib.proc.handler.feedback import FeedbackHandler
from lib.slack.block.block_error import BlockError
from lib.domain.individual_order import IndividualOrder
from lib.slack_impl.block.taco import TacoBlock
from pprint import pformat

from lib.slack_impl.modal.feedback import FeedbackModal


class ViewParserError(DomainError):
    def __init__(self, message: str):
        super().__init__(ViewParser, message)


class ViewParserSubmissionError(ViewParserError):
    def __init__(self, cause: str, block_error: BlockError):
        self.block_error = block_error
        super().__init__(cause)


class ViewParser:
    MAX_SINGLE_TACO = int(TacoTuesdayOrderConfig().get_max_single_taco())

    @staticmethod
    def get_employee_from_submission(view_submission: {}) -> Employee:
        return EmployeeHandler.get_employee(view_submission['user']['id'])

    @staticmethod
    def validate_submission(view_submission: {}):
        err = None

        if 'user' not in view_submission:
            err = 'No user'
        elif 'view' not in view_submission:
            err = 'No view'
        elif 'state' not in view_submission['view']:
            err = 'No view/state'
        elif 'values' not in view_submission['view']['state']:
            err = 'No view/state/values'

        if err is not None:
            ViewParserError(err)

    @classmethod
    def parse_submission_into_individual_order(cls, view_submission: {}) -> IndividualOrder:
        logger.debug('Parsing submission into order...')

        cls.validate_submission(view_submission)

        employee = cls.get_employee_from_submission(view_submission)
        order = IndividualOrder(employee)

        block_ids: dict = view_submission['view']['state']['values']

        block_error = BlockError()

        all_zero = True
        first_block_id = None

        for block_id in block_ids:
            if first_block_id is None: first_block_id = block_id

            action_object = block_ids[block_id]
            action_id = TacoBlock.block_id_to_action_id(block_id)

            # TODO: Try/Catch on keys instead?
            if action_id not in action_object:
                continue
            if 'value' not in action_object[action_id]:
                continue

            value = action_object[action_id]['value']
            try:
                num_tacos = int(value)
            except ValueError:
                block_error.add_error(block_id, f'Really? You thought that "{value}" was acceptable? smh')
                continue

            if num_tacos < 0:
                block_error.add_error(block_id, 'Tacos can only be eaten in positive numbers.')
            elif num_tacos > cls.MAX_SINGLE_TACO:
                block_error.add_error(block_id, "HAHA I ORDERED A LOT OF TACOS TO TRY AND BREAK THE STUPID TACO APP!")
            elif num_tacos > 0:
                all_zero = False
                taco_type = TacoBlock.degenerate_block_id(block_id)
                order.add(taco_type, num_tacos)

        if block_error.error():
            raise ViewParserSubmissionError(cause="Bad taco amount(s)!", block_error=block_error)

        if all_zero:
            block_error.add_error(first_block_id, 'Either get tacos, or get out.')
            raise ViewParserSubmissionError(cause="No tacos ordered!", block_error=block_error)

        return order

    @classmethod
    def parse_submission_into_feedback(cls, view_submission: {}) -> Feedback:
        cls.validate_submission(view_submission)

        view = view_submission['view']
        if 'callback_id' not in view:
            raise ViewParserError(f"No callback ID for view submission: [{view}]")

        callback_id = view['callback_id']

        modal_id = FeedbackModal.get_modal_id_from_callback_id(callback_id)
        input_block_id = FeedbackModal.get_input_block_id(modal_id)
        input_action_id = FeedbackModal.get_action_id_for_text_block(modal_id)

        feedback_text = view['state']['values'][input_block_id][input_action_id]['value']

        feedback_type = FeedbackHandler.get_type(modal_id)
        employee = cls.get_employee_from_submission(view_submission)

        return Feedback(employee, feedback_type, feedback_text, employee.slack_id)

