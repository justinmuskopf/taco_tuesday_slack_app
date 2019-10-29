from lib.slack.accessory.accessory import Accessory
from lib.slack.text.label import Label


class StaticSelectBlock(Accessory):
    def __init__(self, unique=False, action_id: str = None):
        super().__init__('static_select')
        self.unique = unique
        self.options = set() if unique else []
        self.action_id = action_id

    @staticmethod
    def _get_placeholder():
        return Label.get('Select an item')

    @staticmethod
    def get_value_for_option(option: str):
        return f'{option}_SelectValue'

    @classmethod
    def get_option(cls, option: str):
        return {
            'text': Label.get(option),
            'value': cls.get_value_for_option(option)
        }

    def add_option(self, option: str):
        if self.unique:
            self.options.add(self.get_option(option))
        else:
            self.options.append(self.get_option(option))

    def get_accessory(self):
        accessory = super().get_accessory()
        accessory['placeholder'] = self._get_placeholder()
        accessory['options'] = list(self.options) if self.unique else self.options

        if self.action_id is not None:
            accessory['action_id'] = self.action_id

        return accessory
