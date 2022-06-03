class Base:
    cost_dict = None
    tech_tree = None
    warehouse_cap = None
    warehouse_basic = None
    hr_cap = None
    hr_basic = None
    buildings = None

    def __init__(self):
        self.cost_dict = {
            'command_center': {'wood': 10, 'time': 0},
            'warehouse': {'wood': 10, 'time': 0},

        }
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


class Building:
    health_point = 0
    slot = 0
    refund = 0
    level = 0
    type_str = ''
    stat = ''
    base_ptr = None

    def __init__(self, hp, slot, lv, refund, ts, stat, b_ptr):
        self.level = lv
        self.health_point = hp
        self.slot = slot
        self.refund = refund
        self.type_str = ts
        self.stat = stat
        self.base_ptr = b_ptr


class ConstructionCrane(Building):
    progress_record = None

    def __init__(self, base_inst):
        super().__init__(2000, 0, 1, 0, 'construction_crane', 'normal', base_inst)
        self.progress_record = {}

    def query_cost(self, building_type):
        pass

    def build_new(self, slot, building_type):
        pass


class CommandCenter(Building):
    pass


if __name__ == '__main__':
    print('Done')
