class Weapon:
    Power = None
    Targets = None

    def __init__(self, p=None, t=None, init_params=None):
        if init_params is None:
            self.Power = p
            self.Targets = t
        else:
            self.Power = init_params['Power']
            self.Targets = init_params['Targets']

    def save(self):
        weapon_dict = {}
        weapon_dict.__setitem__('Power', self.Power)
        weapon_dict.__setitem__('Targets', self.Targets)
        return weapon_dict
