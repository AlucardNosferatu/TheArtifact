import math
from Tactics import battle_rounds


class MapEvent:
    coordinate = None
    cruise_spd = None

    def __init__(self, x, y):
        self.set_coordinate(x, y)

    def set_coordinate(self, x, y):
        self.coordinate = {'x': x, 'y': y}

    def set_cruise_spd(self, cruise_spd):
        self.cruise_spd = cruise_spd

    def move_on_map(self, heading):
        pass
        # todo

    def dist_to_xy(self, x, y):
        dx = self.coordinate['x'] - x
        dy = self.coordinate['y'] - y
        return math.sqrt(dx ** 2 + dy ** 2)

    def dist_to_me(self, map_event):
        x = map_event.coordinate['x']
        y = map_event.coordinate['y']
        return self.dist_to_xy(x, y)


class TaskForce(MapEvent):
    units = None
    confront = None
    ai_controlled = None

    def __init__(self, x, y, ai_controlled=False):
        super().__init__(x, y)
        self.ai_controlled = ai_controlled
        self.units = []
        self.confront = None

    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, index):
        return self.units.pop(index)

    def can_move(self):
        spd = []
        for unit in self.units:
            if not unit.can_move():
                return False
            else:
                spd.append(unit.thrust)
                # todo:use speed instead of thrust
        self.set_cruise_spd(min(spd))
        return True

    def move_on_map(self, heading):
        if self.can_move():
            super().move_on_map(heading)

    def engage(self, enemy_task_force):
        battle_rounds(self, enemy_task_force)

    def acted(self):
        for unit in self.units:
            if not unit.acted:
                return False
        return True


class ResourceSite(MapEvent):
    pass
