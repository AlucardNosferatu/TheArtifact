import uuid

from Vessel import Vessel


class Crew:
    name: str
    uid: str
    health: float
    loc: list[int]
    dead: bool
    ship: Vessel

    def __init__(self, crew_name):
        self.health = 100
        self.uid = str(uuid.uuid4())
        self.name = crew_name
        self.dead = False
        self.loc = [0, 0]

    def spawn_at(self, x: int, y: int):
        if self.ship.parts_matrix[x][y] is not None:
            self.loc[0] = x
            self.loc[1] = y

    def work_at(self):
        x = self.loc[0]
        y = self.loc[1]
        if self.ship.parts_matrix[x][y] is not None:
            self.ship.parts_matrix[x][y].func()

    def goto(self, x, y):
        pass
        # todo
