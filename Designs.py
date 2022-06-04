class Part:
    health_points = 0
    build_cost = None

    def __init__(self, hp, bc):
        self.health_points = hp
        self.build_cost = bc


class Chassis(Part):
    slot_count = None
    bare_weight_modifier = 0

    def __init__(self, slot_count, bwm, hp, bc):
        super().__init__(hp, bc)
        del_list = []
        for usage in slot_count:
            if slot_count[usage][0] == slot_count[usage][1] == slot_count[usage][2] == 0:
                del_list.append(usage)
        for del_usage in del_list:
            del slot_count[del_usage]
        self.slot_count = slot_count
        self.bare_weight_modifier = bwm


class Engine(Part):
    max_thrust = 0
    fuel_consumption = 0

    def __init__(self, hp, bc):
        super().__init__(hp, bc)


class Weapon(Part):
    fire_rate = 0
    accuracy = 0
    effective_range = 0
    warhead_in_use = None

    def __init__(self, rof, acc, e_range, hp, bc):
        super().__init__(hp, bc)
        self.fire_rate = rof
        self.accuracy = acc
        self.effective_range = e_range

    def load_warhead(self, wh):
        self.warhead_in_use = wh


class Warhead(Weapon):
    damage = 0
    damage_type = 0
    cluster_warhead = None
    speed = 0
    ang_speed = 0

    def __init__(self, cw, damage, dt, spd, ang_spd, hp, bc):
        super().__init__(-1, -1, -1, hp, bc)
        self.speed = spd
        self.ang_speed = ang_spd
        self.cluster_warhead = cw
        self.damage = damage
        self.damage_type = dt


class Locomotive(Part):
    maneuverability = 0
    drag = 0

    def __init__(self, hp, bc):
        super().__init__(hp, bc)


class Avionics(Part):
    main_function = None
    sub_function = None

    def __init__(self, hp, bc, func1, func2=None):
        super().__init__(hp, bc)
        self.main_function = func1
        self.sub_function = func2

    def main_f(self, args):
        self.main_function(args)

    def sub_f(self, args):
        if self.sub_function is not None:
            self.sub_function(args)
        else:
            print('错误！该设备无次要功能！')


class Design:
    chassis_in_use = None
    slots = None
    part_class_dict = {'eng': Engine, 'wpn': Weapon, 'loc': Locomotive, 'avi': Avionics}

    def __init__(self, chassis: Chassis):

        self.slots = {}
        self.chassis_in_use = chassis
        for slot_usage in self.chassis_in_use.slot_count:
            usage_size_list = []
            self.slots.__setitem__(slot_usage, usage_size_list)
            # 0 for small, 1 for med, 2 for large
            for i in range(3):
                self.slots[slot_usage].append([None] * self.chassis_in_use.slot_count[slot_usage][i])


if __name__ == '__main__':
    slot_c = {'eng': [3, 2, 1], 'wpn': [0, 0, 0], 'loc': [2, 1, 0]}
    ch = Chassis(slot_c, 1.0, {'wood': 10}, 100)
    design_1 = Design(ch)
