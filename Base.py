import uuid


class Base:
    tech_tree = None
    warehouse_cap = None
    warehouse_basic = None
    hr_cap = None
    hr_basic = None
    buildings = None
    time_passed_tasks = None

    def __init__(self):
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
    level = 0
    type_str = ''
    stat = ''
    base_ptr = None

    def __init__(self, hp, slot, lv, ts, stat, b_ptr: Base):
        self.level = lv
        self.health_point = hp
        self.slot = slot
        self.type_str = ts
        self.stat = stat
        self.base_ptr = b_ptr


class ConstructionCrane(Building):
    progress_record = {}
    cost_dict = None
    class_dict = None

    def __init__(self, slot, base_inst):
        super().__init__(2000, slot, 1, 'construction_crane', 'normal', base_inst)
        self.progress_record = {}
        self.cost_dict = {
            'command_center': {'wood': 10, 'time': 0},
            'warehouse': {'wood': 10, 'time': 0},

        }
        self.class_dict = {
            'command_center': CommandCenter
        }

    def query_cost(self, building_type):
        print(self.cost_dict[building_type])

    def build_new(self, slot, building_type):
        if building_type not in self.class_dict:
            print('不可建造或建筑类型代码错误！')
        else:
            if 0 <= slot < len(self.base_ptr.buildings):
                if self.base_ptr.buildings[slot] is not None:
                    print('这个位置有建筑了！')
                else:
                    new_b_id = str(uuid.uuid4())
                    self.base_ptr.buildings[slot] = new_b_id
                    self.progress_record.__setitem__(new_b_id, self.class_dict[building_type]())

            else:
                print('基地里没有空地可供建造新建筑')


class CommandCenter(Building):
    def __init__(self, slot, b_ptr: Base):
        super().__init__(2000, slot, 1, 'command_center', 'normal', b_ptr)


if __name__ == '__main__':
    print('Done')
