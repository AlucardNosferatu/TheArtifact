from Weapons.Drone import Drone
from Weapons.Special import Kamikaze


def ranged_explosion(acting_fleet, acting_ship, target_ship, target_fleet):
    _ = target_ship
    damaged_ships = [target_fleet.ships[ship_uid] for ship_uid in target_fleet.ships.keys()]
    damaged_ships = [ship for ship in damaged_ships if ship.speed < acting_ship.explosion_range]
    acting_ship.damaged(acting_ship.hit_points)
    acting_fleet.leave(acting_ship.uid)
    for damaged_ship in damaged_ships:
        old_hp = damaged_ship.hit_points
        damaged_ship.damaged(acting_ship.hit_points)
        print('Target was hit! HP:{}->{}'.format(old_hp, damaged_ship.hit_points))


def miss_and_drop(acting_fleet, acting_ship, target_ship, target_fleet):
    _, _ = target_ship, target_fleet
    print('Missed!')
    acting_ship.damaged(acting_ship.hit_points)
    print('The projectile missed the target and it flew away.')
    acting_fleet.leave(acting_ship.uid)


class Missile(Drone):
    def __init__(self, explosion_range):
        super().__init__(spawner=False, mother_ship=None)
        setattr(self.drone_ship, 'explosion_range', explosion_range)
        self.drone_ship.install_weapon(Kamikaze(acting_ship=self.drone_ship, damage_function=ranged_explosion))
