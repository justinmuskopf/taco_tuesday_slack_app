
class Text:
    def __init__(self, text: str, markdown_enabled: bool = False):
        self.text_type = 'mrkdwn' if markdown_enabled else 'plain_text'
        self.text = text

    def get_text(self):
        return {
            'text': self.text,
            'type': self.text_type
        }