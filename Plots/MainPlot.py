from Classes.Fleet import Fleet


def unlock_override(fleet: Fleet):
    f_ship = fleet.ships[fleet.flag_ship]
    f_ship.override_enabled = True
    return fleet, 0
