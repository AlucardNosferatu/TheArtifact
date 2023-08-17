from Battle.BattleEvent import BattleEvent
from Classes.Fleet import Fleet
from Events.Area88 import Defection, Volunteers
from Utils import Nothing
from Weapons.Melee import AllahAkbar, Kamikaze
from Weapons.Drone import Missile
from main import move_on_map


def battle_only(event):
    return type(event) is BattleEvent


class StrategicMissile(Missile):
    def __init__(self, explosion_range, launcher, filter_event=None):
        super().__init__(explosion_range)
        self.launcher = launcher
        if filter_event is None:
            filter_event = battle_only
        self.filter_event = filter_event

    def strategic_function(self, game_obj, direction):
        w_index = self.launcher.weapons.index(self)
        self.launcher.uninstall_weapon(w_index)
        one_missile_fleet = Fleet()
        one_missile_fleet.join(self.drone_ship)
        move_on_map(
            game_obj=game_obj, direction=direction, speed=self.drone_ship.speed, move_go=False,
            filter_event=self.filter_event, specified_player_fleet=one_missile_fleet
        )


def volunteers_greeting(fleet_p: Fleet):
    print('A troop of volunteers contact your fleet via the probe.')
    print('They are willing to repair ships in your fleet, as long as you meet them.')
    return fleet_p, 0


def probe_task(event):
    if type(event) is Volunteers:
        setattr(event, 'next_e_func', event.event_function)
        event.event_function = volunteers_greeting
    return type(event) in [Defection, Nothing, BattleEvent, Volunteers]


class Probe(StrategicMissile):
    def __init__(self, launcher):
        super().__init__(explosion_range=0, launcher=launcher, filter_event=probe_task)
        weapons = self.drone_ship.weapons
        dynamite_indices = [i for i in range(len(weapons)) if type(weapons[i]) is AllahAkbar]
        # remove dynamites
        dynamite_indices.sort(reverse=True)
        for w_index in dynamite_indices:
            self.drone_ship.uninstall_weapon(w_index=w_index)
        self.drone_ship.install_weapon(Kamikaze(acting_ship=self.drone_ship))
