from Part import *


class Crane(Building):
    def __init__(self):
        super().__init__('crane')
        self.function_list.append(self.func1)
        self.function_list.append(self.func2)

    def func1(self):
        pass

    def func2(self):
        pass


class Lab(Building):
    pass


class Factory(Building):
    pass


class Command(Building):
    pass


class Warehouse(Building):
    pass


class Airport(Building):
    pass
