import random
import uuid

from Classes.Weapon import Weapon


class Ship:
    max_hit_points = None
    max_weapons = None
    speed = None

    uid = None
    hit_points = None
    weapons = None
    name = None
    names = {
        'Nautilus': 0, 'Red Noah': 0, 'Enterprise': 0, 'Dugong': 0, 'Area': 0, 'Nimbus': 0, 'Nebula': 0, 'Rainbow': 0
    }
    buff_list = None

    def __init__(self, mh, mw, spd, armor, fcs, man, name=None):
        self.max_hit_points = mh
        self.max_weapons = mw
        self.speed = spd
        self.armor = armor
        self.fire_control_system = fcs
        self.maneuver = man
        self.buff_list = []
        self.uid = str(uuid.uuid4())
        self.hit_points = self.max_hit_points
        self.weapons: list[Weapon] = []
        if name is None:
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
        amount -= self.armor
        if amount < 0:
            amount = 0
        self.hit_points -= amount
        if self.hit_points < 0:
            self.hit_points = 0

    @staticmethod
    def spawn(mh=None, mw=None, spd=None, wp=None, wt=None, armor=None, fcs=None, man=None):
        if mh is None:
            mh = random.randint(50, 100)
        if mw is None:
            mw = random.randint(5, 10)
        if spd is None:
            spd = random.randint(5, 30)
        if wp is None:
            wp = random.randint(5, 20)
        if wt is None:
            wt = random.randint(7, 10)
        if armor is None:
            armor = random.randint(5, 10)
        if fcs is None:
            fcs = random.randint(10, 50)
        if man is None:
            man = random.randint(5, 10)
        ship = Ship(mh=mh, mw=mw, spd=spd, armor=armor, fcs=fcs, man=man)
        ship.install_weapon(Weapon(p=wp, t=wt))
        return ship


def show_ship(ship):
    print('=========================')
    print('■' + ship.name, end='\t')
    # print('Ship ID:', ship.uid, end='\t')
    print(
        '■HP:', ship.hit_points, '/', ship.max_hit_points,
        '■Speed:', ship.speed,
        '■Armor:', ship.armor,
        '■FCS (Fire Control System):', ship.fire_control_system,
        '■Maneuverability:', ship.maneuver
    )
    for i in range(len(ship.weapons)):
        weapon = ship.weapons[i]
        print('++++++++Weapons++++++++')
        print('■Weapon ID:', i, '■Power:', weapon.power, '■Targets:', weapon.target)
