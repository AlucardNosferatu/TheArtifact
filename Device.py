from Part import *


class Stabilizer(Device):
    pass


class Accelerator(Device):
    pass


class Elevator(Device):
    pass


class SteerMotor(Device):
    pass


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
