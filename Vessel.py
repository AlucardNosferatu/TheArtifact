from Building import *


class Vessel:
    size = None
    # 设计为一维长数组，内容默认为None，当安装有组件后变为组件指针
    p_list: None | list[Part | None] = None
    # 组件容量，可以通过升级载具增大
    part_cap: None | int = None
    uid_str: None | str = None

    def __init__(self, size):
        self.size = size
        self.part_cap = 5
        self.uid_str = str(uuid.uuid4())
        self.p_list = []
        for i in range(self.part_cap):
            self.p_list.append(None)


class NomadCity(Vessel):
    def __init__(self):
        super().__init__('huge')


class CraftCarrier(Vessel):
    def __init__(self):
        super().__init__('large')


class Craft(Vessel):
    def __init__(self):
        super().__init__('medium')


class Drone(Vessel):
    def __init__(self):
        super().__init__('small')
