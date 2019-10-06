from lib.block.block_error import BlockError
from lib.block.taco_block import TacoBlock
from lib.block.view_parser_error import ViewParserError
from lib.domain.individual_order import IndividualOrder
from lib.domain.taco import Taco


class ViewParser:
    def parse_submission_into_individual_order(self, view_submission: {}) -> IndividualOrder:
        # TODO: Throw
        if 'view' not in view_submission: return None
        if 'state' not in view_submission['view']: return None
        if 'values' not in view_submission['view']['state']: return None

        order = IndividualOrder()
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
