from Classes.Event import Event
from Classes.Fleet import Fleet


def unlock_override(fleet: Fleet):
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('Flagship is able to be Override-Control now!')
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    f_ship = fleet.ships[fleet.flag_ship]
    f_ship.override_enabled = True
    return fleet, 0


class UnlockOverride(Event):
    def __init__(self):
        super().__init__(unlock_override)
