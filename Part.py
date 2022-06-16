import uuid
from Dicts import *


class Part:
    # 部件所属载机对象指针，用于数据交互
    v_ptr = None
    size = None
    # 组件类型名称，一类一个
    type_str: None | str = None
    # 组件对象名称，一个实例一个
    uid_str: None | str = None
    # 具有增益效果的相邻组件类型名称
    bonus_neighbor: None | list[str] = None
    # 被增益的有效相邻组件范围
    bonus_radius = 0
    # 容器或连接器
    # 容器允许该组件挂载一个小于载机尺寸级别的载具，con='cont'
    # 连接器允许该组件挂载一个与载机同尺寸级别的载具，con='conn'
    # 既不是容器也不是连接器，con=None
    con: None | str = None
    con_target = None
    # 组件重量
    mass: None | float = None
    hp = None

    armed = None
    max_range = None
    rof = None
    damage = None
    acc = None

    scavenger = None
    res_store = None
    res_cap = None
    collect_spd = None

    garrison = None
    garrison_firepower = None
    # 以列表的形式列出该组件特有功能统一传入载具对象
    function_list = None

    def set_v_ptr(self, vessel_ptr):
        self.v_ptr = vessel_ptr

    def set_engage_perf(self):
        self.armed = self.type_str in armed_list
        if self.armed:
            self.max_range = max_range[self.type_str]
            self.rof = rof[self.type_str]
            self.damage = damage[self.type_str]
            self.acc = acc[self.type_str]
        else:
            self.max_range = 0
            self.rof = 0
            self.damage = 0
            self.acc = 0

    def set_collect_perf(self):
        if self.type_str in scavenger_dict:
            self.scavenger = scavenger_dict[self.type_str]
            self.res_store = 0
            self.res_cap = scavenger_perf[self.type_str][0]
            self.collect_spd = scavenger_perf[self.type_str][1]
        else:
            self.scavenger = []
            self.res_store = 0
            self.res_cap = 0
            self.collect_spd = 0

    def set_occupy_perf(self):
        if self.type_str in initial_garrison:
            self.garrison = initial_garrison[self.type_str]
            self.garrison_firepower = garrison_firepower[self.type_str]
        else:
            self.garrison = 0
            self.garrison_firepower = 0

    def set_con_perf(self):
        if self.type_str in connector_list:
            self.con = 'conn'
        elif self.type_str in container_list:
            self.con = 'cont'
        else:
            self.con = None
        self.con_target = None

    def set_bonus_neighbor(self):
        if self.type_str in part_bonus_neighbor:
            self.bonus_neighbor = part_bonus_neighbor[self.type_str]
        else:
            self.bonus_neighbor = []
        if self.type_str in part_bonus_radius:
            self.bonus_radius = part_bonus_radius[self.type_str]
        else:
            self.bonus_radius = 0

    def __init__(self, size, type_str):
        self.size = size
        self.type_str = type_str
        self.hp = hp[self.type_str]
        self.mass = mass[self.type_str]
        self.uid_str = str(uuid.uuid4())
        self.set_bonus_neighbor()
        self.set_con_perf()
        self.set_engage_perf()
        self.set_collect_perf()
        self.set_occupy_perf()
        self.function_list = []

    def can_engage(self):
        if self.armed:
            return True
        elif self.con is not None and self.con_target is not None:
            if self.con_target.can_engage():
                return True
            else:
                return False

    def engage(self, enemy_tf):
        pass

    def can_collect(self, res_type):
        if res_type in self.scavenger:
            return True
        elif self.con is not None and self.con_target is not None:
            if self.con_target.can_collect(res_type):
                return True
            else:
                return False

    def collect(self, res_site):
        if self.type_str in scavenger_dict:
            if res_site.res_type in scavenger_dict[self.type_str]:
                if self.res_store + self.collect_spd <= self.res_cap:
                    res_site.output_res(self.collect_spd)
                    self.res_store += self.collect_spd

    def can_occupy(self):
        part_firepower = self.garrison * self.garrison_firepower
        if self.con is not None and self.con_target is not None:
            part_firepower += self.con_target.can_occupy()
        return part_firepower

    def occupy(self, cv_or_nc):
        if cv_or_nc.size == 'huge':
            print(self)
            # todo:City Occupation
        elif cv_or_nc.size == 'large':
            pass
            # todo:Boarding Action

    def neighbor_buff(self, n_count):
        pass

    def destroyed(self):
        index = self.v_ptr.p_list.index(self)
        self.v_ptr.uninstall_part(index)


class Building(Part):
    def __init__(self, type_str):
        super().__init__('huge', type_str)


class Room(Part):
    def __init__(self, type_str):
        super().__init__('large', type_str)


class Equipment(Part):
    def __init__(self, type_str):
        super().__init__('medium', type_str)


class Device(Part):
    def __init__(self, type_str):
        super().__init__('small', type_str)
