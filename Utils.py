import random

from Classes.Fleet import Fleet
from Events.TestEvents import a_ship_joins


def show_ship(ship):
    print('=========================')
    print('Ship ID:', ship.uid)
    print('Ship HP:', ship.hit_points, '/', ship.max_hit_points)
    for i in range(len(ship.weapons)):
        weapon = ship.weapons[i]
        print('+++++++++++++++++++++++++')
        print('Weapon:', i, 'Power:', weapon.power, 'Targets:', weapon.target)


def generate_fleet():
    fleet = Fleet()
    for _ in range(random.randint(1, 5)):
        fleet = a_ship_joins(fleet)
    fleet.flag_ship = random.choice(list(fleet.ships.keys()))
    return fleet
