import random

from Battle.BattleActions import hit
from Buffs.NegativeBuff import Parasite
from Classes.Weapon import SpecialWeapon


def one_on_one_kamikaze(acting_fleet, acting_ship, target_ship, target_fleet):
    _, _ = acting_fleet, target_fleet
    acting_ship.damaged(acting_ship.hit_points)
    old_hp = target_ship.hit_points
    target_ship.damaged(acting_ship.hit_points)
    print('{} crashed into {}!!!'.format(acting_ship.name, target_ship.name))
    print('Target was hit! HP:{}->{}'.format(old_hp, target_ship.hit_points))


def missed_kamikaze(acting_fleet, acting_ship, target_ship, target_fleet):
    _, _, _, _ = acting_fleet, acting_ship, target_ship, target_fleet
    print('Missed!')
    print('{} failed at getting close to {}!!!'.format(acting_ship.name, target_ship.name))


class Kamikaze(SpecialWeapon):

    def __init__(self, acting_ship, damage_function=None, miss_function=None, external_fcs=None):
        super().__init__(m=None)
        self.acting_ship = acting_ship
        if damage_function is None:
            damage_function = one_on_one_kamikaze
        self.damage_function = damage_function
        if miss_function is None:
            miss_function = missed_kamikaze
        self.miss_function = miss_function
        if external_fcs is None:
            self.basic_accuracy = acting_ship.fire_control_system
        else:
            self.basic_accuracy = external_fcs

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        # fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
        target_fleet = fleets_and_actions[fleets_and_actions[order[2]][2]][0]
        acting_fleet = fleets_and_actions[order[2]][0]
        ship_uid_list = list(target_fleet.ships.keys())
        if hasattr(self, 'target_excluded'):
            ship_uid_list = [ship_uid for ship_uid in ship_uid_list if ship_uid not in self.target_excluded]
            if len(ship_uid_list) <= 0:
                print('No valid targets! Action aborted!')
                return
        speeds = [target_fleet.ships[ship_uid].speed for ship_uid in ship_uid_list]
        slowest = min(speeds)
        slowest_count = speeds.count(slowest)
        slowest_count_indices = []
        prev_slowest_count_index = -1
        for _ in range(slowest_count):
            prev_slowest_count_index = speeds.index(slowest, prev_slowest_count_index + 1)
            slowest_count_indices.append(prev_slowest_count_index)
        unlucky_ship_index = random.choice(slowest_count_indices)
        unlucky_ship_uid = ship_uid_list[unlucky_ship_index]
        unlucky_ship = target_fleet.ships[unlucky_ship_uid]
        maneuver = acting_ship.maneuver
        maneuver_target = unlucky_ship.maneuver
        if hit(self.basic_accuracy, maneuver, maneuver_target):
            print('{} is approaching {}!!!'.format(acting_ship.name, unlucky_ship.name))
            self.damage_function(
                acting_fleet=acting_fleet, acting_ship=acting_ship, target_ship=unlucky_ship, target_fleet=target_fleet
            )
        else:
            print('{} evaded {}!!!'.format(unlucky_ship.name, acting_ship.name))
            self.miss_function(
                acting_fleet=acting_fleet, acting_ship=acting_ship, target_ship=unlucky_ship, target_fleet=target_fleet
            )


def ranged_explosion(acting_fleet, acting_ship, target_ship, target_fleet):
    _ = target_ship
    damaged_ships = [target_fleet.ships[ship_uid] for ship_uid in target_fleet.ships.keys()]
    damaged_ships = [ship for ship in damaged_ships if ship.speed < acting_ship.explosion_range]
    acting_ship.damaged(acting_ship.hit_points)
    print('{} exploded!!!'.format(acting_ship.name, target_ship.name))
    acting_fleet.leave(acting_ship.uid)
    for damaged_ship in damaged_ships:
        old_hp = damaged_ship.hit_points
        damaged_ship.damaged(acting_ship.hit_points)
        print('Target was hit! HP:{}->{}'.format(old_hp, damaged_ship.hit_points))


def miss_and_explode(acting_fleet, acting_ship, target_ship, target_fleet):
    _, _ = target_ship, target_fleet
    print('Missed!')
    acting_ship.damaged(acting_ship.hit_points)
    print('{} missed the target and it exploded after a while.'.format(acting_ship.name))
    acting_fleet.leave(acting_ship.uid)


class AllahAkbar(Kamikaze):
    def __init__(self, acting_ship, explosion_range, external_fcs=None):
        super().__init__(
            acting_ship=acting_ship, damage_function=ranged_explosion, miss_function=miss_and_explode,
            external_fcs=external_fcs
        )
        self.explosion_range = explosion_range
        setattr(acting_ship, 'explosion_range', self.explosion_range)


def give_parasite_buff(p_dict):
    target = p_dict['ship_e']
    for buff in target.buff_list:
        if type(buff) == Parasite:
            print('The target is already parasitized! Action abort!')
            return False
    p_buff = Parasite(effect_target=target, parasite=p_dict)
    p_buff.trigger()
    target.buff_list.append(p_buff)
    return True


def force_boarding_action(acting_fleet, acting_ship, target_ship, target_fleet):
    p_dict = {
        'countdown': 2,
        'type': 'internal',
        'fleet_p': acting_fleet,
        'ship_p': acting_ship,
        'fleet_e': target_fleet,
        'ship_e': target_ship
    }
    if give_parasite_buff(p_dict):
        print('{} is boarding {}!!!'.format(acting_ship.name, target_ship.name))


class Boarding(Kamikaze):
    def __init__(self, acting_ship):
        super().__init__(
            acting_ship=acting_ship, damage_function=force_boarding_action, miss_function=missed_kamikaze
        )
        self.target_excluded = []

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        # fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
        target_fleet = fleets_and_actions[fleets_and_actions[order[2]][2]][0]
        self.target_excluded.append(target_fleet.flag_ship)
        super().special_function(action, order, acting_ship, extra_params)


def salvage_with_hiigara_style(acting_fleet, acting_ship, target_ship, target_fleet):
    p_dict = {
        'countdown': 1,
        'type': 'external',
        'fleet_p': acting_fleet,
        'ship_p': acting_ship,
        'fleet_e': target_fleet,
        'ship_e': target_ship
    }
    if give_parasite_buff(p_dict):
        print('{} had docked on the surface of {}!!!'.format(acting_ship.name, target_ship.name))


class Salvage(Kamikaze):
    def __init__(self, acting_ship):
        super().__init__(
            acting_ship=acting_ship, damage_function=salvage_with_hiigara_style, miss_function=missed_kamikaze
        )
        self.target_excluded = []

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        # fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
        target_fleet = fleets_and_actions[fleets_and_actions[order[2]][2]][0]
        self.target_excluded.append(target_fleet.flag_ship)
        super().special_function(action, order, acting_ship, extra_params)
