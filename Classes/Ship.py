import random
import uuid

from Battle.BattleOverride import OverrideActions
from Buffs.NegativeBuff import Stall
from Classes.Altitude import default_altitude, fixed_altitude
from Classes.Weapon import Weapon


class Ship:
    max_hit_points = None
    max_weapons = None
    max_speed = None
    # 0 for normal, 1 for not-escapable, 2 for fast escape
    escapable = None
    uid = None
    hit_points = None
    weapons = None
    speed = None
    name = None
    idle_speech = None
    names = {
        'Nautilus': 0, 'Red Noah': 0, 'Enterprise': 0, 'Dugong': 0, 'Area': 0, 'Nimbus': 0, 'Nebula': 0, 'Rainbow': 0
    }
    buff_list = None
    override_enabled = None
    override_actions = None
    parts = None

    def __init__(self, mh, mw, ms, armor, fcs, man, name=None, local_altitude=default_altitude):
        self.max_hit_points = mh
        self.max_weapons = mw
        self.max_speed = ms
        self.armor = armor
        self.fire_control_system = fcs
        self.maneuver = man
        self.escapable = 0
        self.buff_list = []
        self.uid = str(uuid.uuid4())
        self.hit_points = self.max_hit_points
        self.weapons: list[Weapon] = []
        self.speed = 0
        self.altitude = local_altitude['terrain']
        if name is None:
            name = random.choice(list(Ship.names.keys()))
            Ship.names[name] += 1
            name += (' #' + str(Ship.names[name]))
        self.name = name
        self.idle_speech = ['Why should I waits for a better chance?']
        self.override_enabled = False
        self.override_actions = OverrideActions()
        self.parts = []

    def get_force(self, mass=None):
        if mass is None:
            mass = self.get_mass()
        return mass * self.maneuver

    def get_mass(self):
        return (self.hit_points * self.armor) + self.get_weapon_mass()

    def get_weapon_mass(self):
        mass = [weapon.mass for weapon in self.weapons if weapon.mass is not None]
        return sum(mass)

    def install_weapon(self, weapon):
        if len(self.weapons) < self.max_weapons:
            force = self.get_force()
            self.weapons.append(weapon)
            mass_new = self.get_mass()
            self.maneuver = max(1, round(force / mass_new))

    def uninstall_weapon(self, w_index):
        if w_index < self.max_weapons and w_index < len(self.weapons):
            force = self.get_force()
            self.weapons.pop(w_index)
            mass_new = self.get_mass()
            self.maneuver = max(1, round(force / mass_new))

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

    def change_speed(self, amount, allow_exceed=False):
        self.speed += amount
        if self.speed > self.max_speed:
            if allow_exceed:
                print('Over-Speed ({}>{}) is possible when engine is overloaded!'.format(self.speed, self.max_speed))
            else:
                print('Over-Speed ({}>{}) was prevented by Fly Control System.'.format(self.speed, self.max_speed))
                self.speed = self.max_speed
        elif self.speed < 0:
            self.speed = 0
        if self.speed < (0.125 * self.max_speed):
            print('Speed of {} is too low ({}<{}*12.5%), it is stalling!'.format(self.name, self.speed, self.max_speed))
            already_stall = False
            for buff in self.buff_list:
                if type(buff) is Stall:
                    if buff.triggered and not buff.expired:
                        already_stall = True
                        break
            if not already_stall:
                st = Stall(self)
                self.buff_list.append(st)
                st.trigger()
        else:
            for buff in self.buff_list:
                if type(buff) is Stall:
                    if buff.triggered and not buff.expired:
                        print('{} speed up, it has recovered from stalling.'.format(self.name))
                        while not buff.expired:
                            buff.decay()

    @staticmethod
    def spawn(mh=None, mw=None, ms=None, wp=None, wt=None, armor=None, fcs=None, man=None):
        if mh is None:
            mh = random.randint(50, 100)
        if mw is None:
            mw = random.randint(5, 10)
        if ms is None:
            ms = random.randint(5, 30)
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
        ship = Ship(mh=mh, mw=mw, ms=ms, armor=armor, fcs=fcs, man=man)
        ship.install_weapon(Weapon(p=wp, t=wt))
        ship.change_speed(amount=max(1, int(0.5 * ship.max_speed)))
        ship.altitude = (fixed_altitude['atmosphere'] + default_altitude['terrain']) / 2
        return ship

    def show_ship(self):
        # print('=========================')
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
            print('■Weapon ID:', i, '■Type:', type(weapon), '■Power:', weapon.power, '■Targets:', weapon.target)
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
