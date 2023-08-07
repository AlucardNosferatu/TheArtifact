import random
import uuid

from Battle.BattleOverride import OverrideActions
from Classes.Weapon import Weapon


class Ship:
    max_hit_points = None
    max_weapons = None
    speed = None
    # 0 for normal, 1 for not-escapable, 2 for fast escape
    escapable = None
    uid = None
    hit_points = None
    weapons = None
    name = None
    idle_speech = None
    names = {
        'Nautilus': 0, 'Red Noah': 0, 'Enterprise': 0, 'Dugong': 0, 'Area': 0, 'Nimbus': 0, 'Nebula': 0, 'Rainbow': 0
    }
    buff_list = None
    override_enabled = None
    override_actions = None

    def __init__(self, mh, mw, spd, armor, fcs, man, name=None):
        self.max_hit_points = mh
        self.max_weapons = mw
        self.speed = spd
        self.armor = armor
        self.fire_control_system = fcs
        self.maneuver = man
        self.escapable = 0
        self.buff_list = []
        self.uid = str(uuid.uuid4())
        self.hit_points = self.max_hit_points
        self.weapons: list[Weapon] = []
        if name is None:
            name = random.choice(list(Ship.names.keys()))
            Ship.names[name] += 1
            name += (' #' + str(Ship.names[name]))
        self.name = name
        self.idle_speech = ['Why should I waits for a better chance?']
        self.override_enabled = False
        self.override_actions = OverrideActions()

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

    def show_ship(self):
        print('=========================')
        print('■' + self.name, end='\t')
        # print('Ship ID:', ship.uid, end='\t')
        print(
            '■HP:', self.hit_points, '/', self.max_hit_points,
            '■Speed:', self.speed,
            '■Armor:', self.armor,
            '■FCS (Fire Control System):', self.fire_control_system,
            '■Maneuverability:', self.maneuver
        )
        print('++++++++Weapons++++++++')
        for i in range(len(self.weapons)):
            weapon = self.weapons[i]
            print('■Weapon ID:', i, '■Power:', weapon.power, '■Targets:', weapon.target)
        print('+++++++++Buffs+++++++++')
        if len(self.buff_list) <= 0:
            print('==No buff in this ship==')
        else:
            for i in range(len(self.buff_list)):
                buff = self.buff_list[i]
                print(
                    '■Buff ID:', i, '■Type:', type(buff), '■Triggered:', buff.triggered, '■Expired:', buff.expired,
                    '■Timeout:', buff.decay_count
                )


if __name__ == '__main__':
    pass
