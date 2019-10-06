from lib.block.taco_block import TacoBlock
from lib.domain.individual_order import IndividualOrder
from lib.domain.taco import Taco


class ViewParser:
    def parse_submission_into_individual_order(self, view_submission: {}) -> IndividualOrder:
        # TODO: Throw
        if 'state' not in view_submission: return None
        if 'values' not in view_submission['state']: return None

        order = IndividualOrder()
        block_ids: dict = view_submission['state']['values']

        for block_id in block_ids.keys():
            action_object = block_ids[block_id]
            action_id = TacoBlock.block_id_to_action_id(block_id)

            # TODO: Try/Catch on keys instead?
            if action_id not in action_object:
                continue
            if 'value' not in action_object[action_id]:
                continue

