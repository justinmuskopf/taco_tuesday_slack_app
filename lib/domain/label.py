from lib.domain.text import Text


class Label(Text):
    def __init__(self, text: str, markdown_enabled: bool = False, emoji_supported: bool = False):
        super().__init__(text, markdown_enabled)
        self.emoji_supported = emoji_supported

    def get_label(self) -> {}:
        label = super().get_text()
        label['emoji'] = self.emoji_supported

        return label
