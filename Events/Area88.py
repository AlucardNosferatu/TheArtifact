import random

from Classes.Fleet import Fleet
from Utils import show_ship, a_ship_joins


def new_mercenary(fleet: Fleet):
    print('New ship joined the fleet!')
    fleet = a_ship_joins(fleet, show=True)
    return fleet


def volunteer_engineers(fleet: Fleet):
    for ship_uid in fleet.ships.keys():
        fleet.ships[ship_uid].hit_points = fleet.ships[ship_uid].max_hit_points
    print('A troop of volunteers repaired all ships in your fleet.')


def defection(fleet):
    fleet_hostile = Fleet()
    ship_uid = fleet.flag_ship
    if len(list(fleet.ships.keys())) > 1:
        while ship_uid == fleet.flag_ship:
            ship_uid = random.choice(list(fleet.ships.keys()))
        fleet_hostile.join(fleet.ships[ship_uid])
        fleet.leave(ship_uid)
        print('A ship betrayed the fleet!')
        show_ship(fleet_hostile.ships[ship_uid])
        while True:
            break
            # todo: design battle process
        return fleet
    print('You stopped a menacing disturbance on the flag ship.')
    return fleet
