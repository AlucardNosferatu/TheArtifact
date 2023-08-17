from Classes.Buff import Buff
from Classes.Ship import Ship


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


class Parasite(Buff):
    def __init__(self, effect_target, parasite):
        super().__init__(
            parasite['countdown'],
            effect_target,
            Parasite.t_func,
            Parasite.r_func,
            {
                'parasite': parasite,
                'new_damaged': self.damaged
            }
        )

    @staticmethod
    def t_func(target, params: dict):
        _ = target
        parasite = params['parasite']
        if parasite['type'] == 'internal':
            parasite['fleet_p'].leave(parasite['ship_p'].uid)
        elif parasite['type'] == 'external':
            params['old_damaged'] = parasite['ship_p'].damaged
            parasite['ship_p'].damaged = params['new_damaged']

    @staticmethod
    def r_func(target, params: dict):
        parasite = params['parasite']
        if parasite['type'] == 'internal':
            parasite['fleet_p'].join(parasite['ship_p'])
        elif parasite['type'] == 'external':
            parasite['ship_p'].damaged = params['old_damaged']
        parasite['fleet_e'].leave(target.uid)
        parasite['fleet_p'].join(target)

    def decay(self, deactivate=False):
        if deactivate or self.memorized_params['parasite']['ship_p'].is_destroyed():
            self.decay_count = 0
            self.expired = True
            print('Buff:', str(self), 'Expired!')
        else:
            super().decay()

    def damaged(self, amount):
        amount = max(1, round(0.5 * amount))
        Ship.damaged(self.memorized_params['parasite']['ship_p'], amount)
        Ship.damaged(self.effect_target, amount)
