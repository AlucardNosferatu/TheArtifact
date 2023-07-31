import uuid

from Classes.Weapon import Weapon


class Ship:
    Weapons = None
    HitPoints = None
    MaxWeapons = None
    MaxHitPoints = None
    UID = None

    def __init__(self, mh=None, mw=None, init_params=None):
        self.Weapons = []
        if init_params is None:
            self.UID = str(uuid.uuid4())
            self.MaxHitPoints = mh
            self.MaxWeapons = mw
            self.HitPoints = self.MaxHitPoints
        else:
            self.UID = init_params['UID']
            self.MaxHitPoints = init_params['MaxHP']
            self.MaxWeapons = init_params['MaxWeapons']
            self.HitPoints = init_params['HP']
            for weapon_param in init_params['Weapons']:
                self.Weapons.append(Weapon(init_params=weapon_param))

    def install_weapon(self, weapon):
        if len(self.Weapons) < self.MaxWeapons:
            self.Weapons.append(weapon)

    def uninstall_weapon(self, w_index):
        if w_index < self.MaxWeapons and w_index < len(self.Weapons):
            self.Weapons.pop(w_index)

    def save(self):
        ship_dict = {}
        ship_dict.__setitem__('UID', self.UID)
        ship_dict.__setitem__('MaxHP', self.MaxHitPoints)
        ship_dict.__setitem__('MaxWeapons', self.MaxWeapons)
        ship_dict.__setitem__('HP', self.HitPoints)
        ship_dict.__setitem__('Weapons', [weapon.save() for weapon in self.Weapons])
        return ship_dict

    def is_destroyed(self):
        return self.HitPoints <= 0
