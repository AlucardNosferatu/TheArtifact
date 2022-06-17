import random

from AI import generate_f_param
from Part import *
from MapEvent import MapEvent


class Vessel:
    size = None
    # 设计为一维长数组，内容默认为None，当安装有组件后变为组件指针
    p_list = None
    # 组件容量，可以通过升级载具增大
    p_cap: None | int = None
    uid_str: None | str = None

    hp = None
    mass = None
    armor = None
    lift = None
    thrust = None
    yaw_spd = None
    fuel_have = None
    fuel_cap = None

    para_target = None
    can_para = None
    para_cd = None
    para_to = None
    belonged = None
    para_in = None

    acted = None
    tactic_pos = None

    def __init__(self, size):
        self.hp = 0
        self.mass = 0
        self.armor = 0
        self.lift = 0
        self.thrust = 0
        self.yaw_spd = 0
        self.fuel_cap = 0
        self.fuel_have = 0

        self.size = size
        self.p_cap = 5
        self.uid_str = str(uuid.uuid4())
        self.p_list = []
        for i in range(self.p_cap):
            self.p_list.append(None)

        self.para_target = None
        self.can_para = {
            'huge': [],
            'large': [],
            'medium': ['huge'],
            'small': ['huge', 'large']
        }[self.size]

        self.belonged = None
        self.para_cd = 0
        self.para_to = {
            'huge': 100,
            'large': 50,
            'medium': 25,
            'small': 12
        }[self.size]
        self.para_in = []
        self.acted = False
        self.tactic_pos = 0

    def can_move(self):
        if self.lift > self.mass and self.thrust > 0 and self.yaw_spd > 0:
            return True
        else:
            return False

    def install_part(self, part, index):
        if None in self.p_list and self.p_list[index] is None:
            self.p_list[index] = part
            self.p_list: list[Part]
            self.p_list[index].set_v_ptr(self)

            if hasattr(part, 'hp'):
                self.hp += part.hp
            if hasattr(part, 'mass'):
                self.mass += part.mass
            total_armor = 0
            for p in self.p_list:
                if hasattr(p, 'armor'):
                    total_armor += p.armor
            self.p_list: list[None]
            eff_p_count = len(self.p_list) - self.p_list.count(None)
            self.armor = total_armor / eff_p_count
            if hasattr(part, 'lift'):
                self.lift += part.lift
            if hasattr(part, 'thrust'):
                self.thrust += part.thrust
            if hasattr(part, 'yaw_spd'):
                self.yaw_spd += part.yaw_spd
            if hasattr(part, 'fuel_cap'):
                self.fuel_cap += part.fuel_cap
            self.p_list: list[Part]
            self.p_list[index].on_install()

    def uninstall_part(self, index):
        if 0 <= index < self.p_cap and self.p_list[index] is not None:
            self.p_list: list[Part]
            self.p_list[index].on_uninstall()
            part = self.p_list[index]
            self.p_list: list[None]
            self.p_list[index] = None
            if hasattr(part, 'hp'):
                self.hp -= part.hp
            if hasattr(part, 'mass'):
                self.mass -= part.mass
            total_armor = 0
            for p in self.p_list:
                if hasattr(p, 'armor'):
                    total_armor += p.armor
            eff_p_count = len(self.p_list) - self.p_list.count(None)
            self.armor = total_armor / eff_p_count
            if hasattr(part, 'lift'):
                self.lift -= part.lift
            if hasattr(part, 'thrust'):
                self.thrust -= part.thrust
            if hasattr(part, 'yaw_spd'):
                self.yaw_spd -= part.yaw_spd
            if hasattr(part, 'fuel_cap'):
                self.fuel_cap -= part.fuel_cap
                if self.fuel_have > self.fuel_cap:
                    self.fuel_have = self.fuel_cap

    def select_part(self, index, ai=False):
        if not self.acted:
            if index >= len(self.p_list) or index < 0:
                return
            selected_part: Part | None = self.p_list[index]
            if selected_part is None:
                return
            for index, func in enumerate(selected_part.function_list):
                print(index, func)
                print(index, selected_part.params_list[index])
            if not ai:
                f_index = input()
                f_index = f_index.split('-')
                f_index = [eval(item) for item in f_index]
            else:
                f_index = [random.randint(0, len(selected_part.function_list) - 1)]
                for param in selected_part.params_list[f_index[0]]:
                    f_index.append(generate_f_param(param))
            self.acted = selected_part.function_list[f_index[0]](f_index[1:])
        else:
            print('该载具这个回合已经行动过了。')


class NomadCity(Vessel, MapEvent):
    wh_basic = None
    wh_cap = None
    ap_basic = None
    ap_cap = None

    def __init__(self, x, y):
        super().__init__(size='huge')
        self.set_coordinate(x, y)
        self.wh_basic = {
            'wood': 0,
            'steel': 0
        }
        self.ap_basic = []
        self.ap_cap = 4
        for i in range(self.ap_cap):
            self.ap_basic.append(None)

    def move_on_map(self, heading):
        if self.can_move():
            super().move_on_map(heading)


class CraftCarrier(Vessel):
    def __init__(self):
        super().__init__('large')


class Craft(Vessel):
    def __init__(self):
        super().__init__('medium')


class Drone(Vessel):
    def __init__(self):
        super().__init__('small')


if __name__ == '__main__':
    print('Done')
