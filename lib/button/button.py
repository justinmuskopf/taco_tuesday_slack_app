from lib.block.block import Block
from lib.text.label import Label

class ButtonStyle:
    PRIMARY = 'primary'
    DANGER  = 'danger'
    DEFAULT = 'default'

    ValidButtonStyles = [
        PRIMARY,
        DANGER,
        DEFAULT
    ]

    @classmethod
    def is_valid(cls, style: str) -> bool:
        return style in cls.ValidButtonStyles


class Button(Block):
    def __init__(self, text: str, style: str = ButtonStyle.DEFAULT, value: str = 'BUTTON'):
        super().__init__(block_type='button')

        if not ButtonStyle.is_valid(style):
            raise ValueError(f'Button style must be one of {ButtonStyle.ValidButtonStyles}! (Provided {style})')

        self.text = text
        self.value = value
        self.style = style


    def get_button(self) -> {}:
        return {
            'type': 'button',
            'text': Label(self.text).get_label(),
            'style': self.style,
            'value': self.value
        }
