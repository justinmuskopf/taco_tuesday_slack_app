from lib.block.block_error import BlockError


class ViewParserError(RuntimeError):
    def __init__(self, cause: str, block_error: BlockError):
        super().__init__(cause)
        self.block_error = block_error
