from pprint import pformat

from loguru import logger

from lib.proc.handler.employee import EmployeeHandler
from lib.slack.block.block_error import BlockError
from lib.domain.individual_order import IndividualOrder
from lib.slack_impl.taco_block import TacoBlock


class ViewParserError(RuntimeError):
    def __init__(self, cause: str, block_error: BlockError):
        super().__init__(cause)
        self.block_error = block_error


class ViewParser:
    @staticmethod
    def parse_submission_into_individual_order(view_submission: {}) -> IndividualOrder:
        logger.debug('Parsing submission into order...')

        # TODO: Throw
        if 'view' not in view_submission:
            logger.debug('No view in submission! Aborting order creation.')
            return None
        if 'state' not in view_submission['view']:
            logger.debug('No view/state in submission! Aborting order creation.')
            return None
        if 'values' not in view_submission['view']['state']:
            logger.debug('No view/state/values in submission! Aborting order creation.')
            return None

        employee = EmployeeHandler.get_employee(view_submission['user']['id'])
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
            elif num_tacos > 0:
                all_zero = False
                taco_type = TacoBlock.degenerate_block_id(block_id)
                order.add(taco_type, num_tacos)

        if all_zero:
            block_error.add_error(first_block_id, 'Either get tacos, or get out.')
            raise ViewParserError(cause="No tacos ordered!", block_error=block_error)

        if block_error.error():
            raise ViewParserError(cause="Bad taco amount(s)!", block_error=block_error)

        return order
