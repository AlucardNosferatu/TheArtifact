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
    armed = None
    scavenger = None
    extra_personnel = None

    def set_v_ptr(self, vessel_ptr):
        self.v_ptr = vessel_ptr

    def __init__(self, size, type_str):

        self.size = size
        self.type_str = type_str
        self.uid_str = str(uuid.uuid4())
        if type_str in part_bonus_neighbor:
            self.bonus_neighbor = part_bonus_neighbor[type_str]
        else:
            self.bonus_neighbor = []
        if type_str in part_bonus_radius:
            self.bonus_radius = part_bonus_radius[type_str]
        else:
            self.bonus_radius = 0
        if type_str in connector_list:
            self.con = 'conn'
        elif type_str in container_list:
            self.con = 'cont'
        else:
            self.con = None
        self.con_target = None
        self.armed = type_str in armed_list
        if type_str in scavenger_dict:
            self.scavenger = scavenger_dict[type_str]
        else:
            self.scavenger = []
        if type_str in initial_personnel:
            self.extra_personnel = initial_personnel[type_str]
        else:
            self.extra_personnel = 0

    def can_engage(self):
        if self.armed:
            return True
        elif self.con is not None and self.con_target is not None:
            if self.con_target.can_engage():
                return True
            else:
                return False

    def can_collect(self, res_type):
        if res_type in self.scavenger:
            return True
        elif self.con is not None and self.con_target is not None:
            if self.con_target.can_collect(res_type):
                return True
            else:
                return False

    def can_occupy(self, req_personnel):
        if self.extra_personnel >= req_personnel:
            return True
        elif self.con is not None and self.con_target is not None:
            if self.con_target.can_occupy(req_personnel):
                return True
            else:
                return False

    def neighbor_buff(self, n_count):
        pass


class Building(Part):
    # 以列表的形式列出该建筑所有功能统一传入城市对象
    function_list = None

    def __init__(self, type_str):
        super().__init__('huge', type_str)
        self.function_list = []


class Room(Part):
    # 以列表的形式列出该舱室所有功能统一传入航母对象
    function_list = None

    def __init__(self, type_str):
        super().__init__('large', type_str)
        self.function_list = []


class Equipment(Part):
    def __init__(self, type_str):
        super().__init__('medium', type_str)


class Device(Part):
    def __init__(self, type_str):
        super().__init__('small', type_str)
