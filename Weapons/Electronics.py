from Buffs.NegativeBuff import TimedBomb, Jammed, Hijacked
from Classes.Weapon import SpecialWeapon
from Weapons.Drone import Drone, AntiRadarMissile, DroneReturn


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


class RadarJammer(SpecialWeapon):
    def __init__(self, mass):
        super().__init__(mass)

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        target_fleet = fleets_and_actions[fleets_and_actions[order[2]][2]][0]

        unlucky_ship = AntiRadarMissile.pick_target(target_fleet=target_fleet)

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


class DroneHijacker(SpecialWeapon):
    def __init__(self, mass):
        super().__init__(mass)

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        target_fleet = fleets_and_actions[fleets_and_actions[order[2]][2]][0]
        acting_fleet = fleets_and_actions[order[2]][0]
        ship_uid_list = list(target_fleet.ships.keys())
        ship_uid_list = [ship_uid for ship_uid in ship_uid_list if self.hackable(target_fleet.ships[ship_uid])]
        if len(ship_uid_list) <= 0:
            print('No hackable drones! Action aborted!')
            return
        unlucky_ship = AntiRadarMissile.pick_target(target_fleet=target_fleet, ship_uid_list=ship_uid_list)
        hijacked = Hijacked(effect_target=unlucky_ship, fleet_from=target_fleet, fleet_to=acting_fleet)
        hijacked.trigger()
        unlucky_ship.buff_list.append(hijacked)

    @staticmethod
    def hackable(ship):
        for weapon in ship.weapons:
            if type(weapon) is DroneReturn:
                return True
        return False


class AntiHijacker(SpecialWeapon):
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
                if type(acting_fleet.ships[ship_uid].buff_list[index]) is Hijacked:
                    buff = acting_fleet.ships[ship_uid].buff_list.pop(index)
                    while not buff.expired:
                        buff.decay()


class MissileGuider(SpecialWeapon):
    def __init__(self, mass):
        super().__init__(mass)

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        target_fleet = fleets_and_actions[fleets_and_actions[order[2]][2]][0]
        ship_uid_list = list(target_fleet.ships.keys())
        ship_uid_list = [
            ship_uid for ship_uid in ship_uid_list if self.use_guider(target_fleet.ships[ship_uid])
        ]
        if len(ship_uid_list) <= 0:
            print('No guided missile! Action aborted!')
            return
        unlucky_ship = AntiRadarMissile.pick_target(target_fleet=target_fleet)
        for weapon in unlucky_ship.weapons:
            if hasattr(weapon, 'external_fcs') and weapon.external_fcs is not None:
                weapon.external_fcs = round(1.5 * weapon.external_fcs)

    @staticmethod
    def use_guider(ship):
        for weapon in ship.weapons:
            if hasattr(weapon, 'external_fcs') and weapon.external_fcs is not None:
                return True
        return False


class AntiGuider(SpecialWeapon):
    def __init__(self, mass):
        super().__init__(mass)

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        target_fleet = fleets_and_actions[fleets_and_actions[order[2]][2]][0]
        ship_uid_list = list(target_fleet.ships.keys())
        ship_uid_list = [
            ship_uid for ship_uid in ship_uid_list if MissileGuider.use_guider(target_fleet.ships[ship_uid])
        ]
        if len(ship_uid_list) <= 0:
            print('No guided missile! Action aborted!')
            return
        unlucky_ship = AntiRadarMissile.pick_target(target_fleet=target_fleet)
        for weapon in unlucky_ship.weapons:
            if hasattr(weapon, 'external_fcs') and weapon.external_fcs is not None:
                weapon.external_fcs = round(0.5 * weapon.external_fcs)
