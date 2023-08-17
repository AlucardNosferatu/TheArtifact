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


class Parasite(Buff):
    def __init__(self, effect_target, parasite):
        super().__init__(
            parasite['countdown'],
            effect_target,
            Parasite.t_func,
            Parasite.r_func,
            {
                'parasite': parasite,
                'new_damaged': self.damaged,
                'control': False
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
        if params['control']:
            if parasite['fleet_e'].leave(target.uid):
                parasite['fleet_p'].join(target)
                print('{} has taken control of {}!'.format(params['parasite']['ship_p'].name, target.name))
            else:
                if target.uid == parasite['fleet_e'].flag_ship:
                    print("Flag ship self-destructed when it's about to be controlled!!!")
                    target.hit_points = 0
        else:
            print('The executor was destroyed, boarding/salvaging has been aborted!!!')

    def decay(self):
        assert not self.expired
        assert self.triggered
        if not self.memorized_params['parasite']['ship_p'].is_destroyed():
            self.memorized_params['control'] = True
        super().decay()
        if not self.memorized_params['parasite']['ship_p'].is_destroyed():
            if not self.expired:
                print(
                    '{} will take control of {} in {} rounds!'.format(
                        self.memorized_params['parasite']['ship_p'].name,
                        self.effect_target.name,
                        self.decay_count
                    )
                )

    def damaged(self, amount):
        amount = max(1, round(0.5 * amount))
        type(self.memorized_params['parasite']['ship_p']).damaged(self.memorized_params['parasite']['ship_p'], amount)
        type(self.effect_target).damaged(self.effect_target, amount)
        print(
            '{} was involved while {} is being attacked!!!'.format(
                self.effect_target.name,
                self.memorized_params['parasite']['ship_p'].name
            )
        )
