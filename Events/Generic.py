from Classes.Event import Event
from Classes.Fleet import Fleet


def unlock_override(fleet_p: Fleet):
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('Flagship is able to be Override-Control now!')
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    f_ship = fleet_p.ships[fleet_p.flag_ship]
    f_ship.override_enabled = True
    return fleet_p, 0


class UnlockOverride(Event):
    def __init__(self):
        super().__init__(unlock_override)
