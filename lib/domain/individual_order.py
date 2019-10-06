from lib.domain.taco import Taco


class IndividualOrder:
    def __init__(self):
        self.price: float = 0
        self.tacos: dict = {}

    def add(self, taco: Taco, count: int):
        # TODO: Throw
        if count <= 0:
            return

        if taco.taco_type not in self.tacos:
            self.tacos[taco.taco_type] = 0

        self.tacos[taco.taco_type] += count
        self.price += taco.price * count
