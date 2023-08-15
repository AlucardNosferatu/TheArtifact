from Weapons.Drone import Drone
from Weapons.Melee import AllahAkbar


class Missile(Drone):
    def __init__(self, explosion_range, external_fcs=None):
        super().__init__(spawner=False, mother_ship=None, init_weapon=False)
        self.drone_ship.install_weapon(
            AllahAkbar(acting_ship=self.drone_ship, explosion_range=explosion_range, external_fcs=external_fcs))


class Rocket(Missile):
    def __init__(self, explosion_range, acting_ship):
        super().__init__(explosion_range=explosion_range, external_fcs=acting_ship.fire_control_system)
