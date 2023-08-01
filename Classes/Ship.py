import random
import uuid

from Classes.Weapon import Weapon


class Ship:
    weapons = None
    hit_points = None
    max_weapons = None
    max_hit_points = None
    speed = None
    uid = None
    name = None
    names = {
        'Nautilus': 0, 'Red Noah': 0, 'Enterprise': 0, 'Dugong': 0, 'Area': 0, 'Nimbus': 0, 'Nebula': 0, 'Rainbow': 0
    }

    def __init__(self, mh=None, mw=None, spd=None):
        self.weapons: list[Weapon] = []
        self.uid = str(uuid.uuid4())
        self.max_hit_points = mh
        self.max_weapons = mw
        self.hit_points = self.max_hit_points
        self.speed = spd
        name = random.choice(list(Ship.names.keys()))
        Ship.names[name] += 1
        name += (' #' + str(Ship.names[name]))
        self.name = name

    def install_weapon(self, weapon):
        if len(self.weapons) < self.max_weapons:
            self.weapons.append(weapon)

    def uninstall_weapon(self, w_index):
        if w_index < self.max_weapons and w_index < len(self.weapons):
            self.weapons.pop(w_index)

    def is_destroyed(self):
        return self.hit_points <= 0

    def repair(self, amount):
        self.hit_points += amount
        if self.hit_points > self.max_hit_points:
            self.hit_points = self.max_hit_points

    def damaged(self, amount):
        self.hit_points -= amount
        if self.hit_points < 0:
            self.hit_points = 0
