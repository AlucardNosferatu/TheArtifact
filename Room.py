from Part import *


class Hangar(Room):
    pass


class LiftEngine(Room):
    lift = None

    def __init__(self, lift):
        super().__init__('lift_engine')
        self.lift = lift


class Propulsion(Room):
    thrust = None

    def __init__(self, thrust):
        super().__init__('propulsion')
        self.thrust = thrust
        self.function_list.append(self.move_to_tac_pos)
        self.params_list.append(['dst_tac_pos'])

    def move_to_tac_pos(self, params):
        dst_tac_pos = params[0]
        return move_to_tac_pos(self, dst_tac_pos)
