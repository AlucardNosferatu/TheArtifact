from Part import *


class Wing(Equipment):
    lift = None

    def __init__(self, lift):
        super().__init__('wing')
        self.lift = lift


class Thruster(Equipment):
    thrust = None

    def __init__(self, thrust):
        super().__init__('thruster')
        self.thrust = thrust


class CtrlSurface(Equipment):
    yaw_spd = None

    def __init__(self, yaw_spd):
        super().__init__('ctrl_surface')
        self.yaw_spd = yaw_spd


class Drill(Equipment):
    def __init__(self):
        super().__init__('drill')
        self.function_list.append(self.attack)
        self.params_list.append(['target_index'])

    def attack(self, params):
        target_index = params[0]
        part_index = params[1]
        target = self.v_ptr.belonged.confront.units[target_index]
        attack(self, target, part_index)


class TransformHinge(Equipment):
    def __init__(self):
        super().__init__('trans_hinge')
        self.function_list.append(self.raise_parasite_countdown)
        self.params_list.append([])

    # noinspection PyUnusedLocal
    def raise_parasite_countdown(self, params):
        raise_parasite_countdown(self)

    def on_install(self):
        self.v_ptr.can_para.append('large')

    def on_uninstall(self):
        self.v_ptr.can_para.remove('large')


class SalvageMagnet(Equipment):
    def __init__(self):
        super().__init__('salvage_magnet')
        self.function_list.append(self.raise_parasite_countdown)
        self.params_list.append([])

    # noinspection PyUnusedLocal
    def raise_parasite_countdown(self, params):
        raise_parasite_countdown(self)

    def on_install(self):
        self.v_ptr.can_para.append('large')
        self.v_ptr.can_para.append('medium')

    def on_uninstall(self):
        self.v_ptr.can_para.remove('large')
        self.v_ptr.can_para.remove('medium')
