from Part import *
from MapEvent import MapEvent


class Vessel:
    size = None
    # 设计为一维长数组，内容默认为None，当安装有组件后变为组件指针
    p_list: None | list[Part | None] = None
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

    def can_move(self):
        if self.lift > self.mass and self.thrust > 0 and self.yaw_spd > 0:
            return True
        else:
            return False

    def can_engage(self):
        for part in self.p_list:
            if part is not None:
                if part.can_engage():
                    return True
        return False

    def can_collect(self, res_type):
        for part in self.p_list:
            if part is not None:
                if part.can_collect(res_type):
                    return True
        return False

    def can_occupy(self, enemy_firepower=None):
        vessel_firepower = 0
        for part in self.p_list:
            if part is not None:
                vessel_firepower += part.can_occupy()
        if enemy_firepower is None:
            return vessel_firepower
        else:
            return vessel_firepower > enemy_firepower

    def install_part(self, part, index):
        if None in self.p_list:
            if self.p_list[index] is None:
                self.p_list[index] = part
                self.p_list[index].set_v_ptr(self)
                # todo:bonus_neighbor
                if hasattr(part, 'hp'):
                    self.hp += part.hp
                if hasattr(part, 'mass'):
                    self.mass += part.mass
                total_armor = 0
                for p in self.p_list:
                    if hasattr(p, 'armor'):
                        total_armor += p.armor
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
                # todo:attr_update, include armor fuel_cap etc.

    def uninstall_part(self, index):
        if 0 <= index < self.p_cap and self.p_list[index] is not None:
            part = self.p_list[index]
            self.p_list[index] = None
            # todo:bonus_neighbor
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
            # todo:attr_update, include armor fuel_cap etc.


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

    def select_building(self, index):
        if index >= len(self.p_list) or index < 0:
            return
        selected_building: Building | None = self.p_list[index]
        if selected_building is None:
            return
        for index, func in enumerate(selected_building.function_list):
            print(index, func)
        # todo

    def move_on_map(self, heading):
        if self.can_move():
            super().move_on_map(heading)


class CraftCarrier(Vessel):
    def __init__(self):
        super().__init__('large')

    def select_room(self, index):
        if index >= len(self.p_list) or index < 0:
            return
        selected_room: Room | None = self.p_list[index]
        if selected_room is None:
            return
        for index, func in enumerate(selected_room.function_list):
            print(index, func)
        # todo


class Craft(Vessel):
    def __init__(self):
        super().__init__('medium')


class Drone(Vessel):
    def __init__(self):
        super().__init__('small')


if __name__ == '__main__':
    nc = NomadCity(0, 0)
    print('Done')
