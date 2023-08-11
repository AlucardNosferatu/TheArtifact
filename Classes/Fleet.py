class Fleet:
    ships = {}
    flag_ship = None
    storage = None
    will_to_fight = None

    def __init__(self):
        self.ships = {}
        self.flag_ship = None
        self.storage = []
        self.will_to_fight = 0

    def join(self, ship):
        self.ships.__setitem__(ship.uid, ship)

    def leave(self, ship_uid):
        if ship_uid in self.ships.keys() and ship_uid != self.flag_ship:
            Fleet.ships.__setitem__(ship_uid, self.ships.pop(ship_uid))
            return True
        else:
            return False

    def reset_w2f(self):
        self.will_to_fight = 0
        for ship_uid in self.ships:
            if not self.ships[ship_uid].is_destroyed():
                self.will_to_fight += 1
