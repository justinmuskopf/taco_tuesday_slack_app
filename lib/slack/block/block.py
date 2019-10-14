
class Block:
    ID = 1000

    def __init__(self, block_type: str, block_id: str = None):
        self._set_id()
        self.block_type = block_type
        self.block_id = block_id

    def _set_id(self):
        Block.ID += 1
        self.id = Block.ID

    def get_block(self) -> {}:
        block = {'type': self.block_type}
        if self.block_id is not None:
            block['block_id'] = self.block_id

        return block

    def get_block_id(self) -> str:
        return self.block_id
