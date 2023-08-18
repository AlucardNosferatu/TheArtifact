import random

from Battle.BattleActions import hit
from Classes.Fleet import Fleet
from Classes.Ship import Ship
from Classes.Weapon import SpecialWeapon
from Weapons.Melee import AllahAkbar


class Drone(SpecialWeapon):
    def __init__(self, spawner=False, mother_ship=None, init_weapon=True):
        self.init_weapon = init_weapon
        self.drone_ship = Ship.spawn(init_weapon=self.init_weapon)
        super().__init__(mass=self.drone_ship.get_mass())
        self.spawner = spawner
        if not self.spawner and mother_ship is not None:
            self.drone_ship.install_weapon(DroneReturn(mother_ship=mother_ship))
            setattr(self.drone_ship, 'reinstall_drone', self)

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        # fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
        fleet_a: Fleet = fleets_and_actions[order[2]][0]
        fleet_a.join(self.drone_ship)
        print('Drone/Missile:{} was released into combat!'.format(self.drone_ship.name))
        if not self.spawner:
            w_index = acting_ship.weapons.index(self)
            acting_ship.uninstall_weapon(w_index)
        else:
            self.drone_ship = Ship.spawn(init_weapon=self.init_weapon)


class DroneReturn(SpecialWeapon):
    def __init__(self, mother_ship):
        super().__init__(mass=None)
        self.mother_ship = mother_ship

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        # fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
        fleet_a: Fleet = fleets_and_actions[order[2]][0]
        fleet_a.leave(acting_ship.uid)
        # noinspection PyUnresolvedReferences
        self.mother_ship.install_weapon(acting_ship.reinstall_drone)
        print('Drone:{} return to its mothership:{}!'.format(acting_ship.name, self.mother_ship.name))


class Missile(Drone):
    def __init__(self, explosion_range, external_fcs=None):
        super().__init__(spawner=False, mother_ship=None, init_weapon=False)
        self.drone_ship.install_weapon(
            AllahAkbar(acting_ship=self.drone_ship, explosion_range=explosion_range, external_fcs=external_fcs))


class AntiRadarMissile(Missile):
    def __init__(self, explosion_range):
        super().__init__(explosion_range=explosion_range)
        for weapon in self.drone_ship.weapons:
            if type(weapon) is AllahAkbar:
                weapon.pick_target = self.pick_target
                weapon.judge_hit = self.judge_hit

    @staticmethod
    def pick_target(target_fleet, ship_uid_list=None):
        if ship_uid_list is None:
            ship_uid_list = list(target_fleet.ships.keys())
        fcs = [target_fleet.ships[ship_uid].fire_control_system for ship_uid in ship_uid_list]
        loudest = min(fcs)
        loudest_count = fcs.count(loudest)
        loudest_count_indices = []
        prev_loudest_count_index = -1
        for _ in range(loudest_count):
            prev_loudest_count_index = fcs.index(loudest, prev_loudest_count_index + 1)
            loudest_count_indices.append(prev_loudest_count_index)
        unlucky_ship_index = random.choice(loudest_count_indices)
        unlucky_ship_uid = ship_uid_list[unlucky_ship_index]
        unlucky_ship = target_fleet.ships[unlucky_ship_uid]
        return unlucky_ship

    @staticmethod
    def judge_hit(acting_ship, basic_accuracy, unlucky_ship):
        _ = basic_accuracy
        basic_accuracy = unlucky_ship.fire_control_system
        maneuver = acting_ship.maneuver
        maneuver_target = unlucky_ship.maneuver
        hit_target = hit(basic_accuracy, maneuver, maneuver_target)
        return hit_target


class Rocket(Missile):
    def __init__(self, explosion_range, acting_ship):
        super().__init__(explosion_range=explosion_range, external_fcs=acting_ship.fire_control_system)
