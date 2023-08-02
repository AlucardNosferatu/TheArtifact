import random

from Classes.Fleet import Fleet
from Events.Battle import battle_event
from Utils import show_ship, a_ship_joins, a_ship_leaves


def new_mercenary(fleet: Fleet):
    print('New ship joined the fleet!')
    fleet = a_ship_joins(fleet, show=True)
    return fleet, 0


def leaved_mercenary(fleet: Fleet):
    print('A ship left the fleet!')
    fleet = a_ship_leaves(fleet, show=True)
    return fleet, 0


def volunteer_engineers(fleet: Fleet):
    for ship_uid in fleet.ships.keys():
        fleet.ships[ship_uid].hit_points = fleet.ships[ship_uid].max_hit_points
    print('A troop of volunteers repaired all ships in your fleet.')
    return fleet, 0


def defection(fleet):
    enemy_fleet = Fleet()
    ship_uid = fleet.flag_ship
    if len(list(fleet.ships.keys())) > 1:
        while ship_uid == fleet.flag_ship:
            ship_uid = random.choice(list(fleet.ships.keys()))
        enemy_fleet.join(fleet.ships[ship_uid])
        enemy_fleet.flag_ship = ship_uid
        fleet.leave(ship_uid)
        print('A ship betrayed the fleet!')
        show_ship(enemy_fleet.ships[ship_uid])
        fleet, change_score = battle_event(fleet, enemy_fleet=enemy_fleet)
        return fleet, change_score
    print('You stopped a menacing disturbance on the flag ship.')
    return fleet, 0
