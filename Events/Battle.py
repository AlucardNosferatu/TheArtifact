import random

from Classes.Fleet import Fleet
from Events.TestEvents import a_ship_joins


def generate_fleet():
    fleet = Fleet()
    for _ in range(random.randint(1, 5)):
        fleet = a_ship_joins(fleet)
    fleet.FlagShip = random.choice(list(fleet.Ships.keys()))
    return fleet


def battle_event(fleet):
    enemy_fleet = generate_fleet()
    while True:
        break
        # todo: design battle process
    return fleet
