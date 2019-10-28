from lib.slack.accessory.accessory import Accessory
from lib.slack.block.block import Block
from lib.slack.text.label import Label

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


class Button(Accessory):
    def __init__(self, text: str, style: str = ButtonStyle.DEFAULT, value: str = 'BUTTON'):
        super().__init__(accessory_type='button')

        if not ButtonStyle.is_valid(style):
            raise ValueError(f'Button style must be one of {ButtonStyle.ValidButtonStyles}! (Provided {style})')

        self.text = text
        self.value = value
        self.style = style

    def get_accessory(self)-> {}:
        accessory = super().get_accessory()
        accessory['text'] = Label(self.text).get_label()
        accessory['style'] = self.style
        accessory['value'] = self.value

        return accessory
