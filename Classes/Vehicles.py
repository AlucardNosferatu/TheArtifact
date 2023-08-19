import random

from Classes.Altitude import fixed_altitude
from Classes.Ship import Ship
from Classes.Weapon import SpecialWeapon


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


class Combination(Ship):
    def __init__(self, ship_a: Ship, ship_b: Ship):
        mh = ship_a.max_hit_points + ship_b.max_hit_points
        mw = ship_a.max_weapons + ship_b.max_weapons
        ms = max(1, round((ship_a.max_speed + ship_b.max_speed) / 2))
        armor = max(1, round((ship_a.armor + ship_b.armor) / 2))
        fcs = max(ship_a.fire_control_system, ship_b.fire_control_system)
        total_force = ship_a.get_force() + ship_b.get_force()
        total_mass = ship_a.get_mass() + ship_b.get_mass()
        man = max(1, round(total_force / total_mass))
        super().__init__(mh, mw, ms, armor, fcs, man)
        self.ship_a = ship_a
        self.ship_b = ship_b
        self.belong_dict = {'ShipA': self.ship_a, 'ShipB': self.ship_b}
        self.hit_points = self.ship_a.hit_points + self.ship_b.hit_points
        [
            self.weapons.append(w) for w in self.ship_a.weapons + self.ship_b.weapons if type(w) is not Combine
        ]
        self.weapon_map = [
                              'ShipA' for w in self.ship_a.weapons if type(w) is not Combine
                          ] + [
                              'ShipB' for w in self.ship_b.weapons if type(w) is not Combine
                          ]
        self.name = '{}+{}'.format(self.ship_a.name, self.ship_b.name)
        self.idle_speech = self.ship_a.idle_speech + self.ship_b.idle_speech
        self.override_enabled = self.ship_a.override_enabled or self.ship_b.override_enabled
        self.override_actions = [self.ship_a.override_actions, self.ship_b.override_actions]
        if self.ship_a.override_actions is not None:
            self.override_actions = self.ship_a.override_actions
        elif self.ship_b.override_actions is not None:
            self.override_actions = self.ship_b.override_actions
        self.parts = self.ship_a.parts + self.ship_b.parts
        self.change_speed(amount=max(1, int(0.5 * self.max_speed)))

    def install_weapon(self, weapon, belong=None):
        super().install_weapon(weapon)
        if len(self.weapons) < self.max_weapons:
            self.weapon_map.append(belong)

    def uninstall_weapon(self, w_index):
        super().uninstall_weapon(w_index)
        if w_index < self.max_weapons and w_index < len(self.weapons):
            weapon = self.weapons.pop(w_index)
            belong = self.weapon_map.pop(w_index)
            if belong is not None:
                if weapon in self.belong_dict[belong].weapons:
                    w_index_ = self.belong_dict[belong].weapons.index(weapon)
                    force_ = self.belong_dict[belong].get_force()
                    self.belong_dict[belong].weapons.pop(w_index_)
                    mass_new_ = self.belong_dict[belong].get_mass()
                    self.belong_dict[belong].maneuver = max(1, round(force_ / mass_new_))

    def separate(self):
        assert len(self.weapons) == len(self.weapon_map)
        for i in range(len(self.weapons)):
            weapon = self.weapons[i]
            belong = self.weapon_map[i]
            if belong is not None:
                if weapon not in self.belong_dict[belong].weapons:
                    self.belong_dict[belong].weapons.append(weapon)
        hp_ratio_a = self.ship_a.max_hit_points / self.max_hit_points
        hp_ratio_b = 1 - hp_ratio_a
        self.ship_a.hit_points = round(self.hit_points * hp_ratio_a)
        self.ship_b.hit_points = round(self.hit_points * hp_ratio_b)
        return self.ship_a, self.ship_b


class Transformation(Ship):
    def __init__(self, ship_a: Ship, ship_b: Ship):
        mh = max(1, round((ship_a.max_hit_points + ship_b.max_hit_points) / 2))
        armor = max(1, round((ship_a.armor + ship_b.armor) / 2))
        fcs = max(1, round((ship_a.fire_control_system + ship_b.fire_control_system) / 2))
        super().__init__(
            mh, ship_a.max_weapons, ship_a.max_speed, armor, fcs, ship_a.maneuver
        )
        self.mode_a = ship_a
        self.mode_b = ship_b
        self.mode = 'ShipB'
        self.mode_dict = {'ShipA': [self.mode_a, 'ShipB'], 'ShipB': [self.mode_b, 'ShipA']}
        target_mode = self.mode_dict[self.mode][1]
        self.sync_status(mode=target_mode, method='to')

    def sync_status(self, mode, method):
        mode_ship: Ship = self.mode_dict[mode][0]
        if method == 'from':
            mode_ship.weapons = self.weapons
        elif method == 'to':
            self.weapons = mode_ship.weapons
            self.max_speed = mode_ship.max_speed
            self.maneuver = mode_ship.maneuver

    def transform(self):
        self.sync_status(mode=self.mode, method='from')
        target_mode = self.mode_dict[self.mode][1]
        self.sync_status(mode=target_mode, method='to')

    def get_weapon_mass(self):
        mass = super().get_weapon_mass()
        mass += self.mode_dict[self.mode_dict[self.mode][1]][0].get_weapon_mass()
        return mass


class Transform(SpecialWeapon):
    def __init__(self):
        super().__init__(mass=None)

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        # fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
        acting_ship.transform()
        print('{} transformed!'.format(acting_ship.name))
        print('After Transformation, the ballistic computer needs to be reinitialized.')
        print('All followed attack actions in this round will be replaced by evade actions!')
        actions = fleets_and_actions[order[2]][1]
        actions = actions[acting_ship.uid]
        for action_ in actions:
            if action_[0] == 'attack':
                action_.clear()
                action_.append('evade')
                action_.append(13)


class Combine(SpecialWeapon):
    def __init__(self):
        super().__init__(mass=None)

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        # fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
        fleet_a = fleets_and_actions[order[2]][0]
        u_list = list(fleet_a.ships.keys())
        u_list = [
            u for u in u_list if self.combinable(fleet_a.ships[u]) and u != fleet_a.flag_ship and u != acting_ship.uid
        ]
        if len(u_list) <= 0:
            print('No other ship can be combined! Action aborted!')
            return
        lucky_ship = self.pick_target(target_fleet=fleet_a, ship_uid_list=u_list)
        if fleet_a.leave(acting_ship.uid):
            if fleet_a.leave(lucky_ship.uid):
                combined_ship = Combination(ship_a=acting_ship, ship_b=lucky_ship)
                combined_ship.install_weapon(weapon=Separate())
                fleet_a.join(combined_ship)
                print('{} and {} combined!'.format(acting_ship.name, lucky_ship.name))
                print('After Combination, the action execution system needs to be reinitialized.')
                print('All followed actions in this round will not be executed!')
            else:
                print('{} cannot leave fleet, action aborted!'.format(lucky_ship.name))
        else:
            print('{} cannot leave fleet, action aborted!'.format(acting_ship.name))

    @staticmethod
    def pick_target(target_fleet, ship_uid_list=None):
        if ship_uid_list is None:
            ship_uid_list = list(target_fleet.ships.keys())
        hp = [target_fleet.ships[ship_uid].hit_points for ship_uid in ship_uid_list]
        weakest = min(hp)
        weakest_count = hp.count(weakest)
        weakest_count_indices = []
        prev_weakest_count_index = -1
        for _ in range(weakest_count):
            prev_weakest_count_index = hp.index(weakest, prev_weakest_count_index + 1)
            weakest_count_indices.append(prev_weakest_count_index)
        lucky_ship_index = random.choice(weakest_count_indices)
        lucky_ship_uid = ship_uid_list[lucky_ship_index]
        lucky_ship = target_fleet.ships[lucky_ship_uid]
        return lucky_ship

    @staticmethod
    def combinable(ship):
        for weapon in ship.weapons:
            if type(weapon) is Combine:
                return True
        return False


class Separate(SpecialWeapon):
    def __init__(self):
        super().__init__(mass=None)

    def special_function(self, action, order, acting_ship, extra_params):
        fleets_and_actions = extra_params[0]
        # fleets_and_actions = {'FleetA': [fleet_a, actions_a, 'FleetB'], 'FleetB': [fleet_b, actions_b, 'FleetA']}
        acting_fleet = fleets_and_actions[order[2]][0]
        ship_a, ship_b = acting_ship.separate()
        if acting_fleet.leave(acting_ship.uid):
            acting_fleet.join(ship_a)
            acting_fleet.join(ship_b)
            print('{} and {} are separated!'.format(ship_a.name, ship_b.name))
            print('After Separation, the action execution system needs to be reinitialized.')
            print('All followed actions in this round will not be executed!')
        else:
            print('{} cannot leave fleet, action aborted!'.format(acting_ship.name))


if __name__ == '__main__':
    print('Done')
