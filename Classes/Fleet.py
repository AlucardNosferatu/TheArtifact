from Classes.Ship import Ship


class Fleet:
    Ships = None
    FlagShip = None

    def __init__(self, init_params=None):
        if init_params is None:
            self.Ships = {}
            self.FlagShip = None
        else:
            self.FlagShip = init_params['FlagShip']
            ships = init_params['Ships']
            for ship_param in ships:
                ship = Ship(init_params=ship_param)
                self.Ships.__setitem__(ship.UID, ship)

    def join(self, ship):
        self.Ships.__setitem__(ship.UID, ship)

    def leave(self, ship_uid):
        if ship_uid in self.Ships.keys() and ship_uid != self.FlagShip:
            del self.Ships[ship_uid]

    def save(self):
        save_params = []
        for uid in self.Ships:
            ship: Ship = self.Ships[uid]
            save_params.append(ship.save())
        return {'Ships': save_params, 'FlagShip': self.FlagShip}
