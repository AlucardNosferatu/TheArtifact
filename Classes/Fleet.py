from Classes.Ship import Ship


class Fleet:
    ships = None
    flag_ship = None

    def __init__(self, init_params=None):
        self.ships = {}
        self.flag_ship = None
        if init_params is not None:
            self.flag_ship = init_params['FlagShip']
            ships = init_params['Ships']
            for ship_param in ships:
                ship = Ship(init_params=ship_param)
                self.ships.__setitem__(ship.uid, ship)

    def join(self, ship):
        self.ships.__setitem__(ship.uid, ship)

    def leave(self, ship_uid):
        if ship_uid in self.ships.keys() and ship_uid != self.flag_ship:
            del self.ships[ship_uid]

    def save(self):
        save_params = []
        for uid in self.ships:
            ship: Ship = self.ships[uid]
            save_params.append(ship.save())
        return {'Ships': save_params, 'FlagShip': self.flag_ship}
