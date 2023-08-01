class Fleet:
    ships = None
    flag_ship = None

    def __init__(self):
        self.ships = {}
        self.flag_ship = None

    def join(self, ship):
        self.ships.__setitem__(ship.uid, ship)

    def leave(self, ship_uid):
        if ship_uid in self.ships.keys() and ship_uid != self.flag_ship:
            del self.ships[ship_uid]
