import os
import random

from Classes.Fleet import Fleet
from Classes.Ship import Ship
from Classes.Weapon import Weapon


def show_ship(ship):
    print('=========================')
    print('Ship Name:', ship.name, end='\t')
    print('Ship ID:', ship.uid, end='\t')
    print('Ship HP:', ship.hit_points, '/', ship.max_hit_points)
    for i in range(len(ship.weapons)):
        weapon = ship.weapons[i]
        print('+++++++++++++++++++++++++')
        print('Weapon:', i, 'Power:', weapon.power, 'Targets:', weapon.target)


def generate_fleet(min_ships=1, max_ships=5):
    fleet = Fleet()
    for _ in range(random.randint(min_ships, max_ships)):
        fleet = a_ship_joins(fleet)
    fleet.flag_ship = random.choice(list(fleet.ships.keys()))
    return fleet


def a_ship_joins(fleet: Fleet, show=False):
    mh = random.randint(50, 100)
    mw = random.randint(5, 10)
    spd = random.randint(7, 10)
    ship = Ship(mh=mh, mw=mw, spd=spd)
    p = random.randint(5, 15)
    t = random.randint(7, 10)
    ship.install_weapon(Weapon(p=p, t=t))
    fleet.join(ship)
    if show:
        show_ship(ship)
    return fleet


def a_ship_leaves(fleet: Fleet, show=False):
    ship_uid = random.choice(list(fleet.ships.keys()))
    if show:
        show_ship(fleet.ships[ship_uid])
    if not fleet.leave(ship_uid):
        print("But it's your flag ship, you managed to stop it from leaving")
    return fleet


def nothing_happened(fleet: Fleet):
    print('Nothing happened!')
    return fleet, 0


def show_status(fleet):
    os.system('cls' if os.name == 'nt' else "printf '\033c'")
    for ship_uid in fleet.ships.keys():
        ship = fleet.ships[ship_uid]
        print('=========================')
        if ship_uid == fleet.flag_ship:
            print('###Flag Ship###')
        else:
            print('---Normal Ship---')
        show_ship(ship)
