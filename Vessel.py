from math import sqrt

from Box2D import b2FixtureDef, b2PolygonShape, b2Body, b2Joint, b2Vec2

from Part import Part
from Physics import world, init_loop, pygame_loop, body_init, body_test, loop_test, test_2, key_w_test, key_a_test, \
    key_d_test

center_meter = [32, 32]


def di2mi(direct_index, row, col):
    if direct_index == 0:
        return row - 1, col
    elif direct_index == 1:
        return row, col - 1
    elif direct_index == 2:
        return row + 1, col
    elif direct_index == 3:
        return row, col + 1
    else:
        raise ValueError('Error: wrong direction index.')


def grid2meter(grid):
    meter_x = grid[0] * 4 + center_meter[0]
    meter_y = grid[1] * 4 + center_meter[1]
    return meter_x, meter_y


class Vessel:
    parts_matrix: list[list[Part | None]]
    bodies_matrix: list[list[b2Body | None]]
    joint_cluster: list[b2Joint]
    crew_map: list[list[int]]
    pos2index: dict
    index2pos: list[str]

    # Adjacent Matrix of Accessible Parts
    def __init__(self, pm: list):
        self.crew_map = []
        self.pos2index = {}
        self.index2pos = []
        self.parts_matrix = pm
        self.bodies_matrix = []
        self.joint_cluster = []
        parts_to_itself = []
        for i in range(len(self.parts_matrix)):
            row_list = []
            for j in range(len(self.parts_matrix[i])):
                row_list.append(None)
                if self.parts_matrix[i][j] is not None and 'pass' in self.parts_matrix[i][j].connectors:
                    self.pos2index.__setitem__(str(i) + '_' + str(j), len(parts_to_itself))
                    self.index2pos.append(str(i) + '_' + str(j))
                    parts_to_itself.append(0)
            self.bodies_matrix.append(row_list)
        for i in range(len(parts_to_itself)):
            self.crew_map.append(parts_to_itself.copy())

    def form_graph(self):
        for i in range(len(self.index2pos)):
            if self.index2pos[i] is not None:
                r, c = [int(c_str) for c_str in self.index2pos[i].split('_')]
                p_inst = self.parts_matrix[r][c]
                for j in range(4):
                    if p_inst.connected[j] is not None and p_inst.connectors[j] is 'pass':
                        t_r, t_c = di2mi(j, r, c)
                        t_i = self.pos2index[str(t_r) + '_' + str(t_c)]
                        self.crew_map[i][t_i] = 1
                        self.crew_map[t_i][i] = 1
        # todo

    def form_cluster(self):
        for i in range(len(self.parts_matrix)):
            parts_row = self.parts_matrix[i]
            for j in range(len(parts_row)):
                if parts_row[j] is not None:
                    p = parts_row[j]
                    pos_meter = grid2meter(parts_row[j].location)
                    fixture = b2FixtureDef(shape=b2PolygonShape(box=(1.75, 1.75)), density=p.density)
                    dynamic_body = world.CreateDynamicBody(position=pos_meter, angle=0, fixtures=fixture)
                    self.bodies_matrix[i][j] = dynamic_body
        for i in range(len(self.parts_matrix)):
            parts_row = self.parts_matrix[i]
            for j in range(len(parts_row)):
                if parts_row[j] is not None:
                    p = parts_row[j]
                    for k in range(4):
                        if k == 0 or k == 1:
                            pass
                        else:
                            if p.connected[k] is not None:
                                db1 = self.bodies_matrix[i][j]
                                i2, j2 = di2mi(k, i, j)
                                db2 = self.bodies_matrix[i2][j2]
                                anchor = (db1.worldCenter + db2.worldCenter) / 2
                                joint = world.CreateRevoluteJoint(
                                    bodyA=db1,
                                    bodyB=db2,
                                    anchor=anchor,
                                    collideConnected=True
                                )
                                self.joint_cluster.append(joint)

    def check_joints(self):
        kill_list = []
        for i in range(len(self.joint_cluster)):
            force = self.joint_cluster[i].GetReactionForce(10)
            if force.length > 1000:
                print(force.length, 'break joint')
                kill_list.append(i)
        kill_list.sort(reverse=True)
        for killed_j in kill_list:
            world.DestroyJoint(self.joint_cluster.pop(killed_j))

    def test_up(self):
        force = b2Vec2(0, 500)
        for i in range(len(self.bodies_matrix)):
            for j in range(len(self.bodies_matrix[i])):
                if self.bodies_matrix[i][j] is not None:
                    target_body = self.bodies_matrix[i][j]
                    target_body.ApplyForce(force, target_body.worldCenter, True)

    def test_left(self):
        force = b2Vec2(-500, 0)
        for i in range(len(self.bodies_matrix)):
            for j in range(len(self.bodies_matrix[i])):
                if self.bodies_matrix[i][j] is not None:
                    target_body = self.bodies_matrix[i][j]
                    target_body.ApplyForce(force, target_body.worldCenter, True)

    def test_right(self):
        force = b2Vec2(500, 0)
        for i in range(len(self.bodies_matrix)):
            for j in range(len(self.bodies_matrix[i])):
                if self.bodies_matrix[i][j] is not None:
                    target_body = self.bodies_matrix[i][j]
                    target_body.ApplyForce(force, target_body.worldCenter, True)


if __name__ == '__main__':
    cockpit = Part(d=0.5, loc=[0, 0], con_types=[None, 'pass', 'struct', None], n=[None, None, None, None])
    dorm = Part(d=0.5, loc=[-1, 0], con_types=[None, 'pass', 'struct', 'pass'], n=[None, None, None, cockpit])
    lg1 = Part(d=0.5, loc=[0, -1], con_types=['struct', 'struct', None, 'struct'], n=[cockpit, None, None, None])
    lg2 = Part(d=0.5, loc=[-1, -1], con_types=['struct', 'struct', None, 'struct'], n=[dorm, None, None, lg1])
    corridor = Part(d=0.5, loc=[-2, 0], con_types=['pass', 'pass', 'pass', 'pass'], n=[None, None, None, dorm])
    part_m = [[dorm, cockpit], [lg2, lg1]]
    v = Vessel(part_m)
    v.form_graph()
    body_init.append(v.form_cluster)
    body_test.append(test_2)
    loop_test.append(v.check_joints)
    key_w_test.append(v.test_up)
    key_a_test.append(v.test_left)
    key_d_test.append(v.test_right)
    init_loop()
    pygame_loop()
