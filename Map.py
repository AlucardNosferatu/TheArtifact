import math
import random
import sys
import threading
import uuid

import pygame

from artifacts import Artifact
from interaction import surfaces_render_queue

img_dict_test = {}


class MapEvent:
    coordinate = None
    map_size = [2029, 1224]
    icon_id = None
    event_type = None
    icon_path = {
        'base': 'Img/base.png',
        'wood': 'Img/wood.png',
        'task_force': 'Img/task_force.png'
    }
    radiation_src = None
    time_passed_tasks = None

    def __init__(self, x, y, et: str):
        self.coordinate = [x, y]
        self.event_type = et
        self.set_icon_id(str(uuid.uuid4()))
        self.radiation_src = []
        self.time_passed_tasks = []

    def get_bearing(self, origin, use_radian=False):
        x_o, y_o = origin
        x, y = self.coordinate
        dy = y - y_o
        dx = x - x_o
        radian = math.atan2(dy, dx)
        if use_radian:
            return radian
        else:
            return radian * 180 / 3.14

    def get_heading(self, target, use_radian=False):
        x_o, y_o = self.coordinate
        x, y = target
        dy = y - y_o
        dx = x - x_o
        radian = math.atan2(dy, dx)
        if use_radian:
            return radian
        else:
            return radian * 180 / 3.14

    def get_distance(self, origin):
        x_o, y_o = origin
        x, y = self.coordinate
        dy = y - y_o
        dx = x - x_o
        dist = math.sqrt(dy ** 2 + dx ** 2)
        return dist

    def get_screen_pos(self, s_width=1024, s_height=768):
        x, y = self.coordinate
        x_map, y_map = MapEvent.map_size
        x_pix = round(x * s_width / x_map)
        y_pix = s_height - round(y * s_height / y_map)
        return x_pix, y_pix

    def set_coordinate(self, x, y):
        self.coordinate = [x, y]

    def set_icon_id(self, icon_id):
        self.icon_id = icon_id

    def get_icon_id(self):
        return self.icon_id


class Base(MapEvent):
    tech_tree = None
    hangar_cap = None
    hangar_basic = None
    warehouse_cap = None
    warehouse_basic = None
    hr_cap = None
    hr_basic = None
    buildings = None
    unlocked_parts = None
    designs = None
    is_able_to_build_miner = False

    def __init__(self, x, y):
        super().__init__(x, y, 'base')
        self.tech_tree = {
            'command_center': [],
            'warehouse': ['command_center']
        }
        self.is_able_to_build_miner = False
        self.hangar_cap = 4
        self.hangar_basic = []
        self.warehouse_cap = 100
        self.warehouse_basic = {
            'wood': 0,
            'concrete': 0,
            'ore': 0,
            'steel': 0,
            'ti': 0,
            'fuel': 0,
            'silicon': 0,
            'gun_p': 0,
            'barrel': 0,
            'e-device': 0
        }
        self.hr_cap = 100
        self.hr_basic = {
            'army': 0,
            'logistic_worker': 0,
            'pilot': 0,
            'engineer': 0,
            'scientist': 0
        }
        self.buildings = [None, None, None]
        self.unlocked_parts = {
            'chs': [],
            'eng': [],
            'wpn': [],
            'whd': [],
            'loc': [],
            'avi': []
        }
        self.designs = {}

    def next_building_slot(self):
        for i in range(len(self.buildings)):
            if self.buildings[i] is None:
                return i
        return -1

    def expand_building_slot(self):
        self.buildings.append(None)

    def add_resource(self, res_type: str, value: int):
        print('得到了', value, '个', res_type)
        self.warehouse_basic[res_type] += value
        if self.warehouse_basic[res_type] > self.warehouse_cap:
            print('仓库放不下，丢失', self.warehouse_basic[res_type] - self.warehouse_cap, '件', res_type)
            self.warehouse_basic[res_type] = self.warehouse_cap

    def consume_resource(self, res_type: str, value: int):
        print('消耗了', value, '个', res_type)
        self.warehouse_basic[res_type] -= value


class ResourceSite(MapEvent):
    site_name = {
        'wood': '森林',
        'ore': '矿井',
        'steel': '炼钢厂',
        'silicon': '晶圆厂',
        'fuel': '炼油厂'
    }
    stats_modifier_dict = {
        'occupied': 1.5,
        'tech_support': 1.5,
        'damaged': 0.75,
        'disabled': 0.5,
        'depleted': 0.25
    }
    stats = None
    efficiency = 1
    resource_type = None
    resource_amount = None
    resource_left = None

    def __init__(self, x, y, rt, ra):
        super().__init__(x, y, rt)
        self.stats = []
        self.efficiency = 1
        self.resource_type = rt
        self.resource_amount = ra
        self.resource_left = self.resource_amount

    def update_efficiency(self):
        self.efficiency = 1
        if self.resource_left / self.resource_amount <= 0.3:
            self.stats.append('depleted')
        self.stats = list(set(self.stats))
        for stat in self.stats:
            self.efficiency *= ResourceSite.stats_modifier_dict[stat]


class TaskForce(MapEvent):
    units = None
    concurrency = None
    dst = None
    heading = None

    def __init__(self, x, y):
        super().__init__(x, y, 'task_force')
        self.units = []
        self.concurrency = True
        self.dst = [x, y]
        self.heading = random.random() * random.choice([-180, 180])

    def assemble_new_unit(self, unit: Artifact):
        self.units.append(unit)

    def get_total_cpt(self):
        tc = 0
        for unit in self.units:
            unit: Artifact
            tc += unit.ThisSpecs.consumption
        tc *= 0.5
        return tc

    def get_total_fuel(self):
        tf = 0
        for unit in self.units:
            unit: Artifact
            tf += unit.ThisStats.fuel_stored
        return tf

    def consume_after_time(self, time):
        # 1440min=1day
        if len(self.units) > 0:
            f = self.get_total_fuel()
            tc = self.get_total_cpt()
            tc *= time
            f -= tc
            f /= len(self.units)
            for unit in self.units:
                unit.ThisStats.fuel_stored = f

    def move_order(self, x, y):
        self.dst = [x, y]
        if self not in self.time_passed_tasks:
            self.time_passed_tasks.append(self)

    def get_tf_speed(self):
        c_speed = -1
        for unit in self.units:
            unit: Artifact
            u_speed = unit.ThisStats.speed
            if c_speed == -1 or c_speed > u_speed:
                c_speed = u_speed
        return c_speed

    def tomorrow_by_min(self):
        if self.dst[0] != self.coordinate[0] or self.dst[1] != self.coordinate[1]:
            # todo: interact nearby MapEvent
            # region move order
            speed = self.get_tf_speed()
            self.heading = self.get_heading(self.dst)
            dx_min = speed * math.cos(self.heading * 3.14 / 180)
            dy_min = speed * math.sin(self.heading * 3.14 / 180)
            self.coordinate[0] += dx_min
            self.coordinate[1] += dy_min
            # endregion


def pygame_refresh_test():
    global img_dict_test
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("The Artifact")
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 卸载所有模块
                pygame.quit()
                # 终止程序，确保退出程序
                sys.exit()
        clock.tick(60)
        screen.fill('white')
        for img_id in img_dict_test:
            img_obj: pygame.Surface = img_dict_test[img_id][0]
            img_rect: pygame.Rect = img_dict_test[img_id][1]
            screen.blit(img_obj, img_rect)
        pygame.display.update()


if __name__ == '__main__':
    tf1 = TaskForce(1, 1)
    tf2 = TaskForce(2027, 1222)
    # todo:assemble 2 TFs
    concurrent_objs = [tf1, tf2]

    render_queue = []
    pygame_thread = threading.Thread(target=pygame_refresh_test)
    pygame_thread.start()
    while True:
        if not pygame_thread.is_alive():
            print()
        tf1.move_order(random.randint(0, 2028), random.randint(0, 1223))
        tf2.move_order(random.randint(0, 2028), random.randint(0, 1223))
        for i in range(1440):
            for obj in concurrent_objs:
                obj.tomorrow_by_min()

                render_queue, img_dict_test = surfaces_render_queue(render_queue, img_dict_test)