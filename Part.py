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
    # 容器或连接器
    # 容器允许该组件挂载一个小于载机尺寸级别的载具，con='cont'
    # 连接器允许该组件挂载一个与载机同尺寸级别的载具，con='conn'
    # 既不是容器也不是连接器，con=None
    con: None | str = None
    con_target = None
    # 组件重量
    mass: None | float = None
    hp = None

    # 以列表的形式列出该组件特有功能统一传入载具对象
    function_list = None

    def set_v_ptr(self, vessel_ptr):
        self.v_ptr = vessel_ptr

    def __init__(self, size, type_str):
        self.size = size
        self.type_str = type_str
        self.hp = hp[self.type_str]
        self.mass = mass[self.type_str]
        self.uid_str = str(uuid.uuid4())
        self.function_list = []

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
