from Classes.Fleet import Fleet
from Classes.Ship import Ship
from Classes.Weapon import SpecialWeapon
from Weapons.Melee import AllahAkbar


class Drone(SpecialWeapon):
    def __init__(self, spawner=False, mother_ship=None, init_weapon=True):
        self.drone_ship = Ship.spawn(init_weapon=init_weapon)
        super().__init__(m=self.drone_ship.get_mass())
        self.spawner = spawner
        if not self.spawner and mother_ship is not None:
            self.drone_ship.install_weapon(DroneReturn(mother_ship=mother_ship))
            setattr(self.drone_ship, 'reinstall_drone', self)

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        # fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
        fleet_a: Fleet = fleets_and_actions[order[2]][0]
        fleet_a.join(self.drone_ship)
        print('Drone/Missile:{} was released into combat!'.format(self.drone_ship.name))
        if not self.spawner:
            w_index = acting_ship.weapons.index(self)
            acting_ship.uninstall_weapon(w_index)


class DroneReturn(SpecialWeapon):
    def __init__(self, mother_ship):
        super().__init__(m=None)
        self.mother_ship = mother_ship

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        # fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
        fleet_a: Fleet = fleets_and_actions[order[2]][0]
        fleet_a.leave(acting_ship.uid)
        # noinspection PyUnresolvedReferences
        self.mother_ship.install_weapon(acting_ship.reinstall_drone)
        print('Drone:{} return to its mothership:{}!'.format(acting_ship.name, self.mother_ship.name))


class Missile(Drone):
    def __init__(self, explosion_range, external_fcs=None):
        super().__init__(spawner=False, mother_ship=None, init_weapon=False)
        self.drone_ship.install_weapon(
            AllahAkbar(acting_ship=self.drone_ship, explosion_range=explosion_range, external_fcs=external_fcs))


class Rocket(Missile):
    def __init__(self, explosion_range, acting_ship):
        super().__init__(explosion_range=explosion_range, external_fcs=acting_ship.fire_control_system)
