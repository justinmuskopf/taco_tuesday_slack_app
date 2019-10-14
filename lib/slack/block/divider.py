
class Divider:
    ONE_DIVIDER_TO_DIVIDE_THEM_ALL = {'type': 'divider'}

    @staticmethod
    def get():
        return Divider().get_divider()

    def get_divider(self):
        return self.ONE_DIVIDER_TO_DIVIDE_THEM_ALL.copy()
