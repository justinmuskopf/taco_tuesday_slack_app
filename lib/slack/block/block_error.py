class BlockError:
    def __init__(self):
        self.errors = {}
        self.error_count = 0

    @staticmethod
    def get() -> {str}:
        return BlockError().get_block_error()

    def add_error(self, block_id: str, error: str):
        if self.errors[block_id] is None:
            self.error_count += 1
        self.errors[block_id] = error
        
    def get_block_error(self) -> {str}:
        return {
            'response_action': 'errors',
            'errors': self.errors
        }

    def num_errors(self) -> int:
        return self.error_count

    def error(self):
        return self.error_count > 0
