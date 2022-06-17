from Part import *


class Stabilizer(Device):
    def __init__(self):
        super().__init__('stabilizer')


class Accelerator(Device):
    thrust = None

    def __init__(self, thrust):
        super().__init__('accelerator')
        self.thrust = thrust
        self.function_list.append(self.move_to_tac_pos)
        self.params_list.append(['dst_tac_pos'])

    def move_to_tac_pos(self, params):
        dst_tac_pos = params[0]
        return move_to_tac_pos(self, dst_tac_pos)


class Elevator(Device):
    lift = None

    def __init__(self, lift):
        super().__init__('elevator')
        self.lift = lift


class SteerMotor(Device):
    yaw_spd = None

    def __init__(self, yaw_spd):
        super().__init__('steer_motor')
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


class Harpoon(Device):
    def __init__(self):
        super().__init__('harpoon')

    def on_install(self):
        self.v_ptr.can_para.append('medium')

    def on_uninstall(self):
        self.v_ptr.can_para.remove('medium')


class HackerInterface(Device):
    def __init__(self):
        super().__init__('hacker_interface')

    def on_install(self):
        self.v_ptr.can_para.append('medium')
        self.v_ptr.can_para.append('small')

    def on_uninstall(self):
        self.v_ptr.can_para.remove('medium')
        self.v_ptr.can_para.remove('small')
