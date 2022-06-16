import uuid
from Dicts import *


class Part:
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
    # 组件重量
    mass: None | float = None

    def __init__(self, size, type_str):
        self.size = size
        self.type_str = type_str
        self.uid_str = str(uuid.uuid4())
        self.bonus_neighbor = part_bonus_neighbor[type_str]
        self.bonus_radius = part_bonus_radius[type_str]


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
