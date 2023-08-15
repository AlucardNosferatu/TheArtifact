class Weapon:
    power = None
    target = None
    mass = None

    def __init__(self, p=None, t=None, m=None):
        self.power = p
        self.target = t
        if m is None and self.power is not None and self.target is not None:
            m = self.power * self.target
        self.mass = m


class SpecialWeapon(Weapon):
    def __init__(self, m):
        super().__init__(m=m)

    def special_function(self, action, order, acting_ship, extra_params):
        # fleets_and_actions = extra_params[0]
        # fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
        raise NotImplementedError('SpecialWeapon Class wont be called directly!')
