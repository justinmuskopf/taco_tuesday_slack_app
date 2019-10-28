
class Accessory:
    ID = 1000

    def __init__(self, accessory_type: str, accessory_id: str = None):
        self._set_id()
        self.accessory_type = accessory_type
        self.accessory_id = accessory_id

    def _set_id(self):
        Accessory.ID += 1
        self.id = Accessory.ID

    def get_accessory(self) -> {}:
        return {'type': self.accessory_type}

    def get_accessory_id(self) -> str:
        return str(self.accessory_id)
