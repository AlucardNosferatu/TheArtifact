import random

from Battle.BattleActions import hit
from Classes.Weapon import SpecialWeapon


def one_on_one_kamikaze(acting_fleet, acting_ship, target_ship, target_fleet):
    _, _ = acting_fleet, target_fleet
    acting_ship.damaged(acting_ship.hit_points)
    old_hp = target_ship.hit_points
    target_ship.damaged(acting_ship.hit_points)
    print('Target was hit! HP:{}->{}'.format(old_hp, target_ship.hit_points))


def missed_kamikaze(acting_fleet, acting_ship, target_ship, target_fleet):
    _, _, _, _ = acting_fleet, acting_ship, target_ship, target_fleet
    print('Missed!')


class Kamikaze(SpecialWeapon):

    def __init__(self, acting_ship, damage_function=None, miss_function=None):
        super().__init__(m=None)
        self.acting_ship = acting_ship
        if damage_function is None:
            damage_function = one_on_one_kamikaze
        self.damage_function = damage_function
        if miss_function is None:
            miss_function = missed_kamikaze
        self.miss_function = miss_function

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        # fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
        target_fleet = fleets_and_actions[fleets_and_actions[order[2]][2]][0]
        acting_fleet = fleets_and_actions[order[2]][0]
        ship_uid_list = list(target_fleet.ships.keys())
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
        basic_accuracy = acting_ship.fire_control_system
        maneuver = acting_ship.maneuver
        maneuver_target = unlucky_ship.maneuver
        if hit(basic_accuracy, maneuver, maneuver_target):
            self.damage_function(
                acting_fleet=acting_fleet, acting_ship=acting_ship, target_ship=unlucky_ship, target_fleet=target_fleet
            )
        else:
            self.miss_function(
                acting_fleet=acting_fleet, acting_ship=acting_ship, target_ship=unlucky_ship, target_fleet=target_fleet
            )
