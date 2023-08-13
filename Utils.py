import random

from Classes.Event import Event
from Classes.Fleet import Fleet
from Classes.Ship import Ship


def generate_fleet(min_ships=1, max_ships=5):
    fleet = Fleet()
    for _ in range(random.randint(min_ships, max_ships)):
        fleet = a_ship_joins(fleet)
    fleet.flag_ship = random.choice(list(fleet.ships.keys()))
    return fleet


def a_ship_joins(fleet: Fleet, show=False):
    reunion = random.choice([True, False])
    if len(list(Fleet.ships.keys())) <= 0:
        reunion = False
    if reunion:
        print('A ship has rejoined the fleet!')
        ship_uid = random.choice(list(Fleet.ships.keys()))
        ship = Fleet.ships.pop(ship_uid)
    else:
        ship = Ship.spawn()
    fleet.join(ship)
    if show:
        ship.show_ship()
    return fleet


def a_ship_leaves(fleet: Fleet, show=False):
    ship_uid = random.choice(list(fleet.ships.keys()))
    if show:
        fleet.ships[ship_uid].show_ship()
    if not fleet.leave(ship_uid):
        print("But it's your flag ship, you managed to stop it from leaving")
    return fleet


def nothing(fleet: Fleet):
    print('Nothing happened!')
    return fleet, 0


class Nothing(Event):
    def __init__(self):
        super().__init__(nothing)
