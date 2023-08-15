import random

from Battle.BattleEvent import battle_event, BattleEvent
from Classes.Event import Event
from Classes.Fleet import Fleet
from Utils import a_ship_joins, a_ship_leaves


def new_mercenary(fleet_p: Fleet):
    print('New ship joined the fleet!')
    fleet_p = a_ship_joins(fleet_p, show=True)
    return fleet_p, 0


class NewMercenary(Event):
    def __init__(self):
        super().__init__(new_mercenary)


def leaved_mercenary(fleet_p: Fleet):
    print('A ship left the fleet!')
    fleet_p = a_ship_leaves(fleet_p, show=True)
    return fleet_p, 0


class LeavedMercenary(Event):
    def __init__(self):
        super().__init__(leaved_mercenary)


def volunteers(fleet_p: Fleet):
    for ship_uid in fleet_p.ships.keys():
        fleet_p.ships[ship_uid].hit_points = fleet_p.ships[ship_uid].max_hit_points
    print('A troop of volunteers repaired all ships in your fleet.')
    return fleet_p, 0


class Volunteers(Event):
    def __init__(self):
        super().__init__(volunteers)


def defection(fleet_p, fleet_e=None):
    if fleet_e is None:
        fleet_e = Fleet()
        ship_uid = fleet_p.flag_ship
        if len(list(fleet_p.ships.keys())) > 1:
            while ship_uid == fleet_p.flag_ship:
                ship_uid = random.choice(list(fleet_p.ships.keys()))
            fleet_e.join(fleet_p.ships[ship_uid])
            fleet_e.flag_ship = ship_uid
            fleet_p.leave(ship_uid)
            print('A ship betrayed the fleet!')
            fleet_e.ships[ship_uid].show_ship()
        else:
            setattr(fleet_p, 'battle_result', 'win')
            print('You stopped a menacing disturbance on the flag ship.')
            return fleet_p, 0
    fleet_p, change_score = battle_event(fleet_p, fleet_e=fleet_e, clear_=False)
    return fleet_p, change_score


class Defection(BattleEvent):
    def __init__(self):
        super().__init__(customized_event=defection)
