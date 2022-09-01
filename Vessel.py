from Box2D import b2FixtureDef, b2PolygonShape

from Part import Part
from Physics import world

center_meter = [32, 32]


def grid2meter(grid):
    meter_x = grid[0] * 4 + center_meter[0]
    meter_y = grid[1] * 4 + center_meter[1]
    return meter_x, meter_y


class Vessel:
    parts_matrix: list[list[Part | None]]
    bodies_matrix = list[list[Part | None]]

    def __init__(self, pm):
        self.parts_matrix = pm

    def form_cluster(self):
        for i in range(len(self.parts_matrix)):
            parts_row = self.parts_matrix[i]
            for j in range(len(parts_row)):
                if parts_row[j] is not None:
                    p = parts_row[j]
                    pos_meter = grid2meter(parts_row[j].location)
                    fixture = b2FixtureDef(shape=b2PolygonShape(box=(4, 4)), density=p.density)
                    world.CreateDynamicBody(position=pos_meter, angle=0, fixtures=fixture)


if __name__ == '__main__':
    v = Vessel(None)
