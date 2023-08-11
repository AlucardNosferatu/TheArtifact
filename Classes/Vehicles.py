from Classes.Altitude import fixed_altitude
from Classes.Ship import Ship


class ACV(Ship):
    pass


class Plane(Ship):
    def __init__(self, mh, mw, ms, armor, fcs, man):
        super().__init__(mh, mw, ms, armor, fcs, man)
        self.take_off_speed = max(1, int(0.25 * self.max_speed))

    def take_off(self, local_altitude):
        if self.altitude == local_altitude['terrain']:
            while self.speed < self.take_off_speed:
                self.change_speed(amount=5)
            self.altitude = fixed_altitude['atmosphere'] - local_altitude['terrain']
        elif local_altitude['terrain'] < self.altitude <= fixed_altitude['atmosphere']:
            print('The ship is already airborne!')
        elif fixed_altitude['atmosphere'] < self.altitude:
            print('The ship is out of atmosphere!')
        else:
            print('The ship is subterranean!')
