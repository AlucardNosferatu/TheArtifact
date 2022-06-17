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
        self.function_list.append(self.move_to_tac_pos)
        self.params_list.append(['dst_tac_pos'])

    def move_to_tac_pos(self, params):
        dst_tac_pos = params[0]
        return move_to_tac_pos(self, dst_tac_pos)


class CtrlSurface(Equipment):
    yaw_spd = None

    def __init__(self, yaw_spd):
        super().__init__('ctrl_surface')
        self.yaw_spd = yaw_spd
        self.function_list.append(self.embark)
        self.params_list.append(['target_index'])
        self.function_list.append(self.disembark)
        self.params_list.append([])

    def embark(self, params):
        target_index = params[0]
        target = self.v_ptr.belonged.confront.units[target_index]
        return embark(self, target)

    def disembark(self, params):
        return disembark(self)


class Drill(Equipment):
    def __init__(self):
        super().__init__('drill')
        self.function_list.append(self.attack)
        self.params_list.append(['target_index'])

    def attack(self, params):
        target_index = params[0]
        part_index = params[1]
        target = self.v_ptr.belonged.confront.units[target_index]
        return attack(self, target, part_index)


class TransformHinge(Equipment):
    def __init__(self):
        super().__init__('trans_hinge')

    def on_install(self):
        self.v_ptr.can_para.append('large')

    def on_uninstall(self):
        self.v_ptr.can_para.remove('large')


class SalvageMagnet(Equipment):
    def __init__(self):
        super().__init__('salvage_magnet')

    def on_install(self):
        self.v_ptr.can_para.append('large')
        self.v_ptr.can_para.append('medium')

    def on_uninstall(self):
        self.v_ptr.can_para.remove('large')
        self.v_ptr.can_para.remove('medium')
