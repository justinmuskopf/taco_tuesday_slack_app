
class ActionParser:
    @staticmethod
    def is_valid_action(action: {}) -> bool:
        if action is None:
            return False
        if 'type' not in action:
            return False

        return True

    def is_invalid_action(self, action: {}) -> bool:
        return not self.is_valid_action(action)

    def is_button_action(self, action: {}) -> bool:
        if self.is_invalid_action(action): return False

        return action['type'] == 'button'

    def is_of_block(self, action: {}, block_id: str) -> bool:
        if self.is_invalid_action(action): return False

        return False if 'block_id' not in action else action['block_id'] == block_id

    def button_was_pressed(self, action: {}, button_block_id: str) -> bool:
        if self.is_invalid_action(action): return False

        return self.is_button_action(action) and self.is_of_block(action, button_block_id)

