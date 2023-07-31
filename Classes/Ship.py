import uuid

from Classes.Weapon import Weapon


class Ship:
    weapons = None
    hit_points = None
    max_weapons = None
    max_hit_points = None
    uid = None

    def __init__(self, mh=None, mw=None, init_params=None):
        self.weapons = []
        if init_params is None:
            self.uid = str(uuid.uuid4())
            self.max_hit_points = mh
            self.max_weapons = mw
            self.hit_points = self.max_hit_points
        else:
            self.uid = init_params['UID']
            self.max_hit_points = init_params['MaxHP']
            self.max_weapons = init_params['MaxWeapons']
            self.hit_points = init_params['HP']
            for weapon_param in init_params['Weapons']:
                self.weapons.append(Weapon(init_params=weapon_param))

    def install_weapon(self, weapon):
        if len(self.weapons) < self.max_weapons:
            self.weapons.append(weapon)

    def uninstall_weapon(self, w_index):
        if w_index < self.max_weapons and w_index < len(self.weapons):
            self.weapons.pop(w_index)

    def save(self):
        ship_dict = {}
        ship_dict.__setitem__('UID', self.uid)
        ship_dict.__setitem__('MaxHP', self.max_hit_points)
        ship_dict.__setitem__('MaxWeapons', self.max_weapons)
        ship_dict.__setitem__('HP', self.hit_points)
        ship_dict.__setitem__('Weapons', [weapon.save() for weapon in self.weapons])
        return ship_dict

    def is_destroyed(self):
        return self.hit_points <= 0
