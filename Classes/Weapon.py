class Weapon:
    power = None
    target = None

    def __init__(self, p=None, t=None, init_params=None):
        if init_params is None:
            self.power = p
            self.target = t
        else:
            self.power = init_params['Power']
            self.target = init_params['Targets']

    def save(self):
        weapon_dict = {}
        weapon_dict.__setitem__('Power', self.power)
        weapon_dict.__setitem__('Targets', self.target)
        return weapon_dict
