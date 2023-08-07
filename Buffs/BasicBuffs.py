from Classes.Buff import Buff


class Evade(Buff):
    def __init__(self, effect_target, amount):
        super().__init__(1, effect_target, Evade.t_func, Evade.r_func, {'amount': amount})

    @staticmethod
    def t_func(target, params: dict):
        amount = params['amount']
        target.maneuver += amount

    @staticmethod
    def r_func(target, params: dict):
        amount = params['amount']
        target.maneuver -= amount
        if target.maneuver <= 0:
            target.maneuver = 0


class Defend(Buff):
    def __init__(self, effect_target, amount):
        super().__init__(1, effect_target, Defend.t_func, Defend.r_func, {'amount': amount})

    @staticmethod
    def t_func(target, params: dict):
        amount = params['amount']
        target.armor += amount

    @staticmethod
    def r_func(target, params: dict):
        amount = params['amount']
        target.armor -= amount
        if target.armor <= 0:
            target.armor = 0
