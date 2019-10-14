from pprint import pformat

from loguru import logger

from lib.slack.block.block_error import BlockError
from lib.domain.individual_order import IndividualOrder
from lib.slack_impl.taco_block import TacoBlock


class ViewParserError(RuntimeError):
    def __init__(self, cause: str, block_error: BlockError):
        super().__init__(cause)
        self.block_error = block_error


class ViewParser:
    def parse_submission_into_individual_order(self, view_submission: {}) -> IndividualOrder:
        logger.debug('Parsing submission into order...')
        logger.debug(pformat(view_submission))
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

        order = IndividualOrder(view_submission['user']['id'])
        block_ids: dict = view_submission['view']['state']['values']

        block_error = BlockError()

        for block_id in block_ids.keys():
            action_object = block_ids[block_id]
            action_id = TacoBlock.block_id_to_action_id(block_id)

            # TODO: Try/Catch on keys instead?
            if action_id not in action_object:
                continue
            if 'value' not in action_object[action_id]:
                continue

            num_tacos = int(action_object[action_id]['value'])
            if num_tacos < 0:
                block_error.add_error(block_id, 'Tacos can only be eaten in positive numbers.')
            else:
                taco_type = TacoBlock.degenerate_block_id(block_id)
                order.add(taco_type, num_tacos)

        if block_error.error():
            raise ViewParserError(cause="Bad taco amount(s)!", block_error=block_error)

        return order
