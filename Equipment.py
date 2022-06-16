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



