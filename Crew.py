import uuid

import numpy as np

from Part import Part
from Vessel import Vessel


def choose_min(node_cost, close_list):
    node_cost = np.array(node_cost)  # 将node_cost从list转换成array
    open_list = list(set(node_cost[:, 0].tolist()) - set(close_list))  # 建立一个open_list放入没有被遍历的点
    final_list = []
    for i in open_list:
        final_list.append(node_cost[int(i)].tolist())
    final_list = np.array(final_list)  # final_list转换成array，才可以利用np.where找最小值
    node_min_cost = final_list[np.where(final_list[:, 1] == final_list[:, 1].min())][0][0]  # 将node_cost最小的点的节点名给node0
    return int(node_min_cost)


def count_cost(mapping_list, node_cost, close_list, start_node, node_count):
    for i in range(0, node_count):
        if mapping_list[start_node][i] + node_cost[start_node][1] < node_cost[i][1]:
            node_cost[i][2] = start_node
            node_cost[i][1] = mapping_list[start_node][i] + node_cost[start_node][1]
    close_list.append(start_node)
    return [node_cost, close_list]


class Crew:
    name: str
    uid: str
    health: float
    loc: list[int]
    dead: bool
    ship: Vessel
    current_route: list[int]
    walk_spd: float
    mov_proc: float

    def __init__(self, crew_name, ship):
        self.health = 100
        self.uid = str(uuid.uuid4())
        self.name = crew_name
        self.dead = False
        self.loc = [0, 0]
        self.ship = ship
        self.current_route = []
        self.walk_spd = 10.0
        self.mov_proc = 0.0

    def spawn_at(self, x: int, y: int):
        if self.ship.parts_matrix[x][y] is not None:
            self.loc[0] = x
            self.loc[1] = y
            print(self.name, 'is at', self.loc)

    def work_here(self):
        x = self.loc[0]
        y = self.loc[1]
        if self.ship.parts_matrix[x][y] is not None:
            self.ship.parts_matrix[x][y].func()

    def goto_order(self, x, y):
        self.current_route.clear()
        node_count = len(self.ship.crew_map)
        node_cost: list[list[int | float]] = [[np.inf for i in range(0, 3)] for i in range(node_count)]
        for i in range(node_count):
            node_cost[i][0] = i
        node0 = self.ship.pos2index[str(self.loc[0]) + '_' + str(self.loc[1])]
        crew_pos = node0
        close_list = []
        for i in range(node_count):
            if self.ship.crew_map[crew_pos][i] < node_cost[i][1]:
                node_cost[i][2] = crew_pos
                node_cost[i][1] = self.ship.crew_map[crew_pos][i]
        close_list.append(crew_pos)
        node1 = self.ship.pos2index[str(x) + '_' + str(y)]
        target_pos = node1
        while target_pos not in close_list:
            node0 = choose_min(node_cost, close_list)  # 找node_cost最小的节点
            node_cost, close_list = count_cost(self.ship.crew_map, node_cost, close_list, node0, node_count)  # 计算邻节点
        self.current_route.append(node1)
        print("最短的路径代价为:", node_cost[node1][1])
        while crew_pos not in self.current_route:
            node1 = node_cost[node1][2]
            self.current_route.append(node1)
        print("最短路径为：", self.current_route)

    def what_now(self):
        if len(self.current_route) > 0:
            if self.mov_proc < 100.0:
                self.mov_proc += self.walk_spd
            else:
                self.mov_proc = 0.0
                r, c = [int(c_str) for c_str in self.ship.index2pos[self.current_route.pop(-1)].split('_')]
                self.spawn_at(r, c)
        else:
            self.work_here()


if __name__ == '__main__':
    dorm11 = Part(d=0.5, loc=[-1, 1], con_types=['pass', 'pass', 'pass', 'pass'], n=[None, None, None, None])
    dorm12 = Part(d=0.5, loc=[0, 1], con_types=['pass', 'pass', 'pass', 'pass'], n=[None, dorm11, None, None])
    dorm13 = Part(d=0.5, loc=[1, 1], con_types=['pass', 'pass', 'pass', 'pass'], n=[None, dorm12, None, None])
    dorm21 = Part(d=0.5, loc=[-1, 0], con_types=['pass', 'pass', 'pass', 'pass'], n=[dorm11, None, None, None])
    dorm22 = Part(d=0.5, loc=[0, 0], con_types=['pass', 'pass', 'pass', 'pass'], n=[dorm12, dorm21, None, None])
    dorm23 = Part(d=0.5, loc=[1, 0], con_types=['pass', 'pass', 'pass', 'pass'], n=[dorm13, dorm22, None, None])
    dorm31 = Part(d=0.5, loc=[-1, -1], con_types=['pass', 'pass', 'pass', 'pass'], n=[dorm21, None, None, None])
    dorm32 = Part(d=0.5, loc=[0, -1], con_types=['pass', 'pass', 'pass', 'pass'], n=[dorm22, dorm31, None, None])
    dorm33 = Part(d=0.5, loc=[1, -1], con_types=['pass', 'pass', 'pass', 'pass'], n=[dorm23, dorm32, None, None])
    part_m = [
        [dorm11, dorm12, dorm13],
        [dorm21, dorm22, dorm23],
        [dorm31, dorm32, dorm33]
    ]
    v = Vessel(part_m)
    v.form_cluster()
    v.form_graph()
    crew1 = Crew('Linhaobo', v)
    crew1.spawn_at(0, 0)
    crew1.goto_order(2, 2)

