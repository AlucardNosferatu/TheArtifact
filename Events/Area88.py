import random

from Classes.Fleet import Fleet
from Classes.Ship import Ship
from Classes.Weapon import Weapon
from Utils import show_ship, generate_fleet


def rebel_attack(fleet):
    enemy_fleet = generate_fleet()
    _ = enemy_fleet
    while True:
        break
        # todo: design battle process
    return fleet


def new_mercenary(fleet: Fleet):
    mh = random.randint(50, 101)
    mw = random.randint(5, 11)
    ship = Ship(mh=mh, mw=mw)
    p = random.randint(5, 15)
    t = random.randint(1, 10)
    ship.install_weapon(Weapon(p=p, t=t))
    fleet.join(ship)
    print('New ship joined the fleet!')
    show_ship(ship)
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
