import math
import sys

import pygame


class MapEvent:
    coordinate = None
    map_size = [2029, 1224]
    icon_id = None

    def __init__(self, x, y):
        self.coordinate = [x, y]

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
    warehouse_cap = None
    warehouse_basic = None
    hr_cap = None
    hr_basic = None
    buildings = None
    time_passed_tasks = None
    unlocked_parts = None
    loaded_designs = None

    def __init__(self, x, y):
        super().__init__(x, y)
        self.tech_tree = {
            'command_center': [],
            'warehouse': ['command_center']
        }
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
        self.time_passed_tasks = []
        self.unlocked_parts = {
            'chs': [],
            'eng': [],
            'wpn': [],
            'whd': [],
            'loc': [],
            'avi': []
        }
        self.loaded_designs = {}

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
        super().__init__(x, y)
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


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("The Artifact")
    NewBase = Base(1014, 612)
    NewBase_icon = pygame.image.load('mark.png')
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
        new_rect = NewBase_icon.get_rect()
        new_rect.center = tuple(NewBase.get_screen_pos())
        screen.blit(NewBase_icon, new_rect)
        pygame.display.update()
