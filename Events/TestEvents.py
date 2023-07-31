import random

from Classes.Fleet import Fleet
from Classes.Ship import Ship
from Classes.Weapon import Weapon


def a_ship_joins(fleet: Fleet):
    mh = random.randint(50, 101)
    mw = random.randint(5, 11)
    ship = Ship(mh=mh, mw=mw)
    p = random.randint(5, 15)
    t = random.randint(1, 10)
    ship.install_weapon(Weapon(p=p, t=t))
    fleet.join(ship)
    print('New ship joined the fleet!')
    return fleet


def a_ship_leaves(fleet: Fleet):
    ship_uid = random.choice(list(fleet.ships.keys()))
    fleet.leave(ship_uid)
    print('A ship left the fleet!')
    return fleet


def nothing_happened(fleet: Fleet):
    print('Nothing happened!')
    return fleet
