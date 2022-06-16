import math


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

    def __init__(self, x, y):
        super().__init__(x, y)
        self.units = []

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
        self.set_cruise_spd(min(spd))
        return True

    def can_engage(self):
        for unit in self.units:
            if unit.can_engage():
                return True
        return False

    def can_collect(self, res_type):
        for unit in self.units:
            if unit.can_collect(res_type):
                return True
        return False

    def can_occupy(self, enemy_firepower):
        tf_firepower = 0
        for unit in self.units:
            tf_firepower += unit.can_occupy()
        if tf_firepower > enemy_firepower:
            return True
        else:
            return False

    def move_on_map(self, heading):
        if self.can_move():
            super().move_on_map(heading)


class ResourceSite(MapEvent):
    pass
