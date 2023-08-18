from Buffs.NegativeBuff import TimedBomb, Jammed
from Classes.Weapon import SpecialWeapon
from Weapons.Drone import Drone, AntiRadarMissile


class Jammer(SpecialWeapon):
    def __init__(self, mass):
        super().__init__(mass)

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        target_fleet = fleets_and_actions[fleets_and_actions[order[2]][2]][0]

        unlucky_ship = AntiRadarMissile.pick_target(target_fleet)

        jammed = Jammed(effect_target=unlucky_ship)
        jammed.trigger()
        unlucky_ship.buff_list.append(jammed)


class AntiJammer(SpecialWeapon):
    def __init__(self, mass):
        super().__init__(mass)

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        acting_fleet = fleets_and_actions[order[2]][0]
        uid_list = list(acting_fleet.ships.keys())
        for ship_uid in uid_list:
            buff_count = len(acting_fleet.ships[ship_uid].buff_list)
            for index in range(buff_count):
                index = buff_count - index - 1
                if type(acting_fleet.ships[ship_uid].buff_list[index]) is Jammed:
                    buff = acting_fleet.ships[ship_uid].buff_list.pop(index)
                    while not buff.expired:
                        buff.decay()


class Dummy(Drone):
    def __init__(self, drone_life, fleet):
        super().__init__(spawner=True, mother_ship=None, init_weapon=False)
        self.drone_life = drone_life
        self.fleet = fleet
        self.init_drone()

    def special_function(self, action, order, acting_ship, extra_params):
        super().special_function(action, order, acting_ship, extra_params)
        self.init_drone()

    def init_drone(self):
        self.drone_ship.hit_points = 1
        self.drone_ship.armor = 0
        self.drone_ship.dummy = True
        tb = TimedBomb(effect_target=self.drone_ship, life=self.drone_life, fleet=self.fleet)
        tb.trigger()
        self.drone_ship.buff_list.append(tb)


class AntiDummy(SpecialWeapon):
    def __init__(self, mass):
        super().__init__(mass)

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        target_fleet = fleets_and_actions[fleets_and_actions[order[2]][2]][0]
        uid_list = list(target_fleet.ships.keys())
        for ship_uid in uid_list:
            target_ship = target_fleet.ships[ship_uid]
            if target_ship.dummy:
                target_ship.hit_points = 0
                target_fleet.leave(ship_uid)
                print('{} was revealed as a dummy, its signal is filtered now.'.format(target_ship.name))

