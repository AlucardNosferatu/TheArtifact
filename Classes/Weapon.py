class Weapon:
    power = None
    target = None

    def __init__(self, p=None, t=None):
        self.power = p
        self.target = t


class SpecialWeapon(Weapon):
    def __init__(self):
        super().__init__()

    def special_function(self, action, order, acting_ship, extra_params):
        # fleets_and_actions = extra_params[0]
        # fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
        raise NotImplementedError('SpecialWeapon Class wont be called directly!')


