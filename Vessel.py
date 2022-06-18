import random

from AI import generate_f_param
from Part import *


class Vessel:
    size = None
    # 设计为一维长数组，内容默认为None，当安装有组件后变为组件指针
    p_list = None
    p_list_dis = None
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
    tactic_ang = None

    wh_basic = None
    wh_cap = None
    ap_basic = None
    ap_cap = None
    guard_force = None

    def __init__(self, size, x=None, y=None):
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
        self.p_list_dis = []
        for i in range(self.p_cap):
            self.p_list.append(None)
            self.p_list_dis.append(None)

        self.para_target = None
        self.can_para = {
            'huge': [],
            'large': [],
            'medium': ['huge'],
            'small': ['huge', 'large']
        }[self.size]

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
        if self.size == 'huge':
            assert x is not None
            assert y is not None
            self.guard_force = TaskForce(x, y)
            self.guard_force.add_unit(self)
            self.wh_basic = {
                'wood': 0,
                'steel': 0
            }
            self.ap_basic = []
            self.ap_cap = 4
            for i in range(self.ap_cap):
                self.ap_basic.append(None)
            self.belonged = self.guard_force
        else:
            self.guard_force = None
            self.wh_basic = None
            self.ap_basic = None
            self.ap_cap = None
            self.belonged = None

    def can_move(self):
        if self.lift > self.mass and self.thrust > 0 and self.yaw_spd > 0:
            return True
        else:
            return False

    def install_part(self, part, index):
        if 0 <= index < self.p_cap and self.p_list_dis[index] is None:
            if part.size == self.size:
                part.set_v_ptr(self)
                self.p_list_dis[index] = part
                print(part.type_str, '已安装在', index, '号槽位。')
                return True
            else:
                print('零件尺寸与载具尺寸不匹配！')
                return False
        else:
            print('槽位编号错误！')
            return False

    def uninstall_part(self, index):
        if 0 <= index < self.p_cap and self.p_list_dis[index] is not None:
            self.p_list_dis: list[None | Part]
            part = self.p_list_dis[index]
            part.set_v_ptr(None)
            self.p_list_dis[index] = None
            print(part.type_str, '从', index, '号槽位拆除完毕。')
            return True
        else:
            print('槽位编号错误！')
            return False

    def enable_part(self, index):
        if 0 <= index < self.p_cap and self.p_list_dis[index] is not None:
            self.p_list: list[Part | None]

            part = self.p_list_dis[index]
            self.p_list[index] = part
            self.p_list_dis[index] = None

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
            print(index, '号槽位的部件', part.type_str, '已激活！')
            return True
        else:
            print('槽位编号错误！')
            return False

    def disable_part(self, index):
        if 0 <= index < self.p_cap and self.p_list[index] is not None:
            self.p_list: list[Part | None]

            self.p_list[index].on_uninstall()

            part = self.p_list[index]
            self.p_list_dis[index] = part
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
            print(index, '号槽位的部件', part.type_str, '已失效！')
            return True
        else:
            print('槽位编号错误！')
            return False

    def use_part(self, index, ai=False):
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
            try:
                self.acted = selected_part.function_list[f_index[0]](f_index[1:])
            except Exception as e:
                print(e)
                self.acted = False
        else:
            print('该载具这个回合已经行动过了。')


if __name__ == '__main__':
    print('Done')
