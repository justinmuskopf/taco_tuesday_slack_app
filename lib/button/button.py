from lib.block.block import Block
from lib.text.label import Label


class Button(Block):
    PRIMARY = 'primary'
    DANGER  = 'danger'
    DEFAULT = 'default'

    ValidButtonStyles = [
        PRIMARY,
        DANGER,
        DEFAULT
    ]

    def __init__(self, text: str, style: str = DEFAULT):
        super().__init__(block_type='button')

        self.text = text

        if style not in self.ValidButtonStyles:
            raise ValueError(f'Button style must be one of {self.ValidButtonStyles}! (Provided {style})')

        self.style = style

    def get_button(self) -> {}:
        return {
            'type': 'button',
            'text': Label(self.text).get_label(),
            'style': self.style
        }
