from Classes.Buff import Buff


class Stall(Buff):
    def __init__(self, effect_target):
        super().__init__(1, effect_target, Stall.t_func, Stall.r_func)

    @staticmethod
    def t_func(target, params: dict):
        amount = max(1, int(0.25 * target.maneuver))
        params['amount'] = amount
        target.maneuver -= amount

    @staticmethod
    def r_func(target, params: dict):
        amount = params['amount']
        target.maneuver += amount
