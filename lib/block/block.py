from lib.domain.text import Text


class Block:
    def __init__(self, block_type: str, block_id: str = None):
        self.block_type = block_type
        self.block_id = block_id

    def get_block(self):
        block = {
            'type': self.block_type
        }

        if self.block_id is not None:
            block['block_id'] = self.block_id

        return block
