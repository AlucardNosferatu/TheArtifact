import os
import pickle
import random
from math import sqrt

import numpy as np

from Battle.BattlePlan import clear_screen
from Classes.Event import Event
from Classes.Fleet import Fleet
from Config import default_new_event_period, default_new_event_dist
from Events.EventSystem import global_pools_dict, update_score_and_flags, gather_triggered_pools
from Maps.Composer import compose_map
from Utils import a_ship_joins

clear = True


def move_on_map(game_obj, direction, speed, move_go=True, filter_event=None, specified_player_fleet=None):
    global clear
    dx, dy, x0, x_final, y0, y_final = get_ideal_dst_coordinate(game_obj, direction, speed)

    terrains = get_events_on_the_trail(game_obj, x0, y0, dx, dy, target='terrain')
    terrains = sort_events_on_the_trail(events=terrains, x0=x0, y0=y0)

    altitude = game_obj.fleet.ships[game_obj.fleet.flag_ship].altitude
    climbing = game_obj.fleet.ships[game_obj.fleet.flag_ship].maneuver
    x_final, y_final = get_reachable_dst_coordinate(terrains, x_final, y_final, altitude, climbing)
    dx, dy = x_final - x0, y_final - y0
    events = get_events_on_the_trail(game_obj, x0, y0, dx, dy, target='event')
    events = sort_events_on_the_trail(events=events, x0=x0, y0=y0)

    game_over = False
    game_over, x_final, y_final = play_events_on_the_trail(
        events, filter_event, game_obj, game_over, specified_player_fleet, x0, x_final, y0,
        y_final
    )

    if move_go and not game_over:
        game_obj.coordinate = [x_final, y_final]
        # noinspection PyTypeChecker
        game_obj.map[game_obj.coordinate[1]][game_obj.coordinate[0]] = game_obj
        current_altitude = game_obj.fleet.ships[game_obj.fleet.flag_ship].altitude
        dest_altitude = game_obj.terrain[y_final, x_final, :]
        if dest_altitude[2] <= current_altitude:
            game_obj.fleet.ships[game_obj.fleet.flag_ship].altitude = game_obj.terrain[y_final, x_final, 2]
        elif dest_altitude[1] <= current_altitude:
            if hasattr(game_obj.fleet.ships[game_obj.fleet.flag_ship], 'burrow'):
                game_obj.fleet.ships[game_obj.fleet.flag_ship].altitude = game_obj.terrain[y_final, x_final, 1]
            else:
                game_obj.fleet.ships[game_obj.fleet.flag_ship].altitude = game_obj.terrain[y_final, x_final, 2]
        elif dest_altitude[0] <= current_altitude:
            game_obj.fleet.ships[game_obj.fleet.flag_ship].altitude = game_obj.terrain[y_final, x_final, 0]
        else:
            if hasattr(game_obj.fleet.ships[game_obj.fleet.flag_ship], 'burrow'):
                game_obj.fleet.ships[game_obj.fleet.flag_ship].altitude = game_obj.terrain[y_final, x_final, 1]
            else:
                game_obj.fleet.ships[game_obj.fleet.flag_ship].altitude = game_obj.terrain[y_final, x_final, 0]
        print(
            'Move from {},{} to {},{} at speed:{}, altitude:{}, direction:{}'.format(
                x0, y0, x_final, y_final, speed, game_obj.fleet.ships[game_obj.fleet.flag_ship].altitude, direction
            )
        )


def get_ideal_dst_coordinate(game_obj, direction, speed):
    x, y = game_obj.coordinate[0], game_obj.coordinate[1]
    game_obj.map[y][x] = None
    dx, dy = int(direction.split(',')[0]), int(direction.split(',')[1])
    ds = max(1, round(sqrt(dx ** 2 + dy ** 2)))
    dx, dy = round(speed * dx / ds), round(speed * dy / ds)
    x_final = min(max(0, x + dx), game_obj.terrain.shape[1] - 1),
    y_final = min(max(0, y + dy), game_obj.terrain.shape[0] - 1)
    return dx, dy, x, x_final, y, y_final


def get_events_on_the_trail(game_obj, x0, y0, dx, dy, trigger_radius=2, target='event'):
    # todo: implement encounter logic
    events = []
    for i in range(game_obj.terrain.shape[0]):
        for j in range(game_obj.terrain.shape[1]):
            if dx != 0:
                d = game_obj.p2l(x0, y0, dx, dy, i, j)
            else:
                d = abs(j - x0)
            if d < trigger_radius:
                location = [j, i]
                event_distance = sqrt((location[0] - x0) ** 2 + (location[1] - y0) ** 2)
                event_direction = [(location[0] - x0), (location[1] - y0)]
                moving_direction = [dx, dy]
                same_direction = [moving_direction[i] * event_direction[i] for i in range(2)]
                same_direction = [factor for factor in same_direction if factor >= 0]
                if event_distance <= sqrt(dx ** 2 + dy ** 2) and len(same_direction) == 2:
                    if target == 'event':
                        if game_obj.map[i][j] is not None:
                            event = game_obj.map[i][j]
                            events.append([event, location])
                    elif target == 'terrain':
                        events.append([np.copy(game_obj.terrain[i, j, :]), location])
    return events


def sort_events_on_the_trail(events, x0, y0):
    def calc_dist(loc, x, y):
        x_loc, y_loc = loc[0], loc[1]
        return sqrt((y_loc - y) ** 2 + (x_loc - x) ** 2)

    new_events = []
    dist = [calc_dist(events[i][-1], x0, y0) for i in range(len(events))]
    locations = {}
    [locations.__setitem__(i, dist[i]) for i in range(len(events))]
    locations = sorted(locations.items(), key=lambda d: d[1])
    for location in locations:
        event = events[location[0]]
        new_events.append(event)
    return new_events


def get_reachable_dst_coordinate(terrains, x_final, y_final, altitude, climbing):
    for i in range(len(terrains)):
        if altitude >= terrains[i][0][2]:
            floor_start = terrains[i][0][2]
        elif altitude >= terrains[i][0][1]:
            x_final, y_final = terrains[i][1][0], terrains[i][1][1]
            break
        elif altitude >= terrains[i][0][0]:
            floor_start = terrains[i][0][0]
        else:
            x_final, y_final = terrains[i][1][0], terrains[i][1][1]
            break
        if i + 1 < len(terrains):
            layer = 0
            if terrains[i + 1][0][1] <= floor_start:
                layer = 2
            floor_end = terrains[i + 1][0][layer]
            h_diff = floor_end - floor_start
            if h_diff > climbing:
                if i + 3 < len(terrains):
                    e1 = terrains[i + 1][0][layer]
                    e2 = terrains[i + 2][0][layer]
                    e3 = terrains[i + 3][0][layer]
                    if e2 - floor_start <= climbing:
                        terrains[i + 1][0][layer] = e2
                        terrains[i + 2][0][layer] = e1
                    elif e3 - floor_start <= climbing:
                        terrains[i + 1][0][layer] = e3
                        terrains[i + 3][0][layer] = e1
                    else:
                        x_final, y_final = terrains[i][1][0], terrains[i][1][1]
                        break
                elif i + 2 < len(terrains):
                    e1 = terrains[i + 1][0]
                    e2 = terrains[i + 2][0]
                    if e2 - floor_start <= climbing:
                        terrains[i + 1][0] = e2
                        terrains[i + 2][0] = e1
                    else:
                        x_final, y_final = terrains[i][1][0], terrains[i][1][1]
                        break
                else:
                    x_final, y_final = terrains[i][1][0], terrains[i][1][1]
                    break
            else:
                continue
        else:
            x_final, y_final = terrains[i][1][0], terrains[i][1][1]
    return x_final, y_final


def play_events_on_the_trail(
        events, filter_event, game_obj, game_over, specified_player_fleet, x, x_final, y,
        y_final
):
    while len(events) > 0:
        event = events.pop(0)
        if filter_event is not None:
            if filter_event(event):
                pass
            else:
                continue
        location = event[-1]
        print('Something happened on the route to destination!')
        # noinspection PyTypeChecker
        event_func: Event = event[0]
        game_obj.random_event(event=event_func, specified_player_fleet=specified_player_fleet)
        if event_func.end:
            game_obj.map[location[1]][location[0]] = None
        else:
            x_final, y_final = get_evaded_location(game_obj, location, near_point=game_obj.coordinate)
            if x_final < 0 or y_final < 0:
                x_final, y_final = x, y
                print('The fleet was blocked by other events!')
            break
        if game_obj.is_game_over():
            game_over = True
            break
    return game_over, x_final, y_final


def get_evaded_location(game_obj, center, near_point=None):
    def check_location(sl, go):
        if 0 <= sl[0] < len(go.map[0]):
            if 0 <= sl[1] < len(go.map):
                if there_is_no_event(sl, go):
                    return True
        return False

    def there_is_no_event(sl, go):
        return go.map[sl[1]][sl[0]] is None

    dist = 2
    centers = [center]
    used = []
    surround_locations_ = []
    while len(surround_locations_) <= 0:
        if len(centers) > 0:
            location = centers.pop(0)
            if location not in used:
                used.append(location)
                surround_locations = [
                    [location[0] + dist, location[1]], [location[0] - dist, location[1]],
                    [location[0], location[1] + dist], [location[0], location[1] - dist],
                    [location[0] - dist, location[1] - dist], [location[0] + dist, location[1] + dist],
                    [location[0] - dist, location[1] + dist], [location[0] + dist, location[1] - dist]
                ]
                centers += [
                    surround_loc for surround_loc in surround_locations if not there_is_no_event(surround_loc, game_obj)
                ]
                surround_locations_ = [
                    surround_loc for surround_loc in surround_locations if check_location(surround_loc, game_obj)
                ]
        else:
            return -1, -1
    if near_point is None:
        evaded_location = random.choice(surround_locations_)
    else:
        x_s, y_s = near_point[0], near_point[1]
        dst = []
        for e_loc in surround_locations_:
            x_d, y_d = e_loc[0], e_loc[1]
            dst.append(sqrt((x_d - x_s) ** 2 + (y_d - y_s) ** 2))
        min_dst = min(dst)
        min_dst_index = dst.index(min_dst)
        evaded_location = surround_locations_[min_dst_index]
    x_final, y_final = evaded_location[0], evaded_location[1]
    return x_final, y_final


class Game:
    fleet = None
    score = None
    finished_chains = None
    flags = None
    killed = None
    battles = None
    map = None
    coordinate = None
    events_pool = None
    new_event_countdown = None
    new_event_period = None
    terrain = None

    def __init__(self):
        self.reset_attributes()

    def reset_attributes(self):
        self.events_pool = global_pools_dict['default']
        self.score = 0
        self.fleet = None
        self.finished_chains = []
        self.flags = []
        self.killed = 0
        self.battles = 0
        self.load_terrain_map()
        self.init_event_map()

    def load_terrain_map(self):
        # todo: implement loading terrain
        # for debug
        terrain = compose_map()
        self.terrain = terrain.astype(np.int16)

    def init_event_map(self):
        w = self.terrain.shape[1]
        h = self.terrain.shape[0]
        self.map = []
        row = []
        for _ in range(w):
            row.append(None)
        for _ in range(h):
            self.map.append(row.copy())
        self.coordinate = [int(0.5 * w), int(0.5 * h)]
        self.new_event_period = default_new_event_period
        self.new_event_countdown = len(self.new_event_period)

    def game_loop(self):
        global clear
        while True:
            cmd = ''
            while cmd not in ['1', '2', '3']:
                clear = clear_screen(clear)
                print('~~~~~~~~~~~~~~~~~~~~~~~~')
                cmd = input('1.New Game\t2.Old Game\t3.Exit\n')
            if cmd == '1':
                print('~~~~~~~~~~~~~~~~~~~~~~~~')
                print('=======New Game=======')
                self.reset_attributes()
                self.init_fleet()
                clear = False
            elif cmd == '2':
                print('~~~~~~~~~~~~~~~~~~~~~~~~')
                print('=======Old Game=======')
                clear = False
                if not self.load():
                    continue
            elif cmd == '3':
                os.abort()
            else:
                raise ValueError()
            self.events_loop()

    def init_fleet(self):
        self.fleet = Fleet()
        self.fleet = a_ship_joins(self.fleet, show=True)
        self.fleet.flag_ship = list(self.fleet.ships.keys())[0]
        x, y = self.coordinate[0], self.coordinate[1]
        self.fleet.ships[self.fleet.flag_ship].altitude = self.terrain[y, x, -1]

    def load(self):
        if os.path.exists('save.pkl'):
            old_game = pickle.load(open('save.pkl', 'rb'))
            for key in old_game.keys():
                setattr(self, key, old_game[key])
            return True
        else:
            print('No previously saved game.')
            return False

    def events_loop(self):
        global clear
        while True:
            # random event
            clear = clear_screen(clear)
            if not self.is_game_over():
                print('~~~~~~~~~~~~~~~~~~~~~~~~')
                self.update_map()
                events = self.contact_events()
                while not self.is_game_over() and len(events) > 0:
                    event = random.choice(events)
                    location = event[1]
                    event_func = event[0]
                    print('Something happened at:{}'.format(location))
                    self.random_event(event=event_func)
                    events.remove(event)
                    if event_func.end:
                        self.map[location[1]][location[0]] = None
            # check game over
            if self.is_game_over():
                clear = clear_screen(clear)
                print('=======Game Over=======')
                self.display_score()
                return
            clear = False
            cmd = ''
            while cmd not in ['1', '4', '5']:
                clear = clear_screen(clear)
                self.show_event_map()
                print('======================================')
                self.show_terrain_map()
                cmd = input('1.Hold Position\t2.Manage Fleet\t3.Move\t4.Save & Exit\t5.Exit\n')
                if cmd == '2':
                    # todo: extend fleet management
                    self.fleet.show_fleet_status()
                    clear = False
                elif cmd == '3':
                    cmd = ''
                    while cmd not in [str(index) for index in list(range(-10, 11))] + ['B']:
                        cmd = input('Input X-factor of direction from -10-10, [B] for back.')
                    if cmd == 'B':
                        continue
                    else:
                        x_factor = cmd
                    cmd = ''
                    while cmd not in [str(index) for index in list(range(-10, 11))] + ['B']:
                        cmd = input('Input Y-factor of direction from -10-10, [B] for back.')
                    if cmd == 'B':
                        continue
                    else:
                        y_factor = cmd
                    cmd = ''
                    while cmd not in [str(index) for index in list(range(10, 110, 10))] + ['B']:
                        cmd = input(
                            'Input Speed percentage level [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]%, [B] for back.'
                        )
                    if cmd == 'B':
                        continue
                    else:
                        s_factor = cmd
                    direction = '{},{}'.format(x_factor, y_factor)
                    clear = clear_screen(clear)
                    full_speed = self.fleet.get_cruise_speed()
                    speed = max(1, round(full_speed * float(s_factor) / 100))
                    move_on_map(self, direction, speed, move_go=True)
                    cmd = '1'
                    clear = False
            if cmd == '1':
                continue
            elif cmd in ['4', '5']:
                if cmd == '4':
                    self.save()
                return
            else:
                raise ValueError()

    def is_game_over(self):
        return self.fleet.ships[self.fleet.flag_ship].is_destroyed()

    def update_map(self):
        # todo: implement map update
        Event.clear_timeout_event(self)
        x, y = self.coordinate[0], self.coordinate[1]
        # noinspection PyTypeChecker
        self.map[y][x] = self
        dist = default_new_event_dist
        surround_locations = [
            [x + dist, y], [x - dist, y], [x, y + dist], [x, y - dist],
            [x - dist, y - dist], [x + dist, y + dist], [x - dist, y + dist], [x + dist, y - dist]
        ]
        surround_locations = [
            sl for sl in surround_locations if 0 <= sl[0] < len(self.map[0]) and 0 <= sl[1] < len(self.map)
        ]
        if self.new_event_countdown >= 0:
            self.new_event_countdown -= 1
        else:
            self.new_event_countdown = len(self.new_event_period) - 1
        print('{} events appeared!'.format(self.new_event_period[self.new_event_countdown]))
        for i in range(self.new_event_period[self.new_event_countdown]):
            location = random.choice(surround_locations)
            event = random.choice(self.events_pool['events'])
            x_loc, y_loc = location[0], location[1]
            if self.map[y_loc][x_loc] is not None:
                x_loc, y_loc = get_evaded_location(self, location)
            if x_loc >= 0 and y_loc >= 0:
                self.map[y_loc][x_loc] = event()
            surround_locations.remove(location)

    def show_event_map(self):
        x, y = self.coordinate[0], self.coordinate[1]
        window_size_w = 15
        window_size_h = 10
        digit_w = len(str(self.terrain.shape[1]))
        digit_h = len(str(self.terrain.shape[0]))
        print(r'Y\X', end='  ')
        for j in range(max(0, x - window_size_w), min(len(self.map[0]), x + window_size_w + 1)):
            j_str = str(j)
            while len(j_str) < digit_w:
                j_str = '0' + j_str
            print(j_str, end='  ')
        print()
        for i in range(max(0, y - window_size_h), min(len(self.map), y + window_size_h + 1)):
            i_str = str(i)
            while len(i_str) < digit_h:
                i_str = '0' + i_str
            print(i_str, end='  ')
            for j in range(max(0, x - window_size_w), min(len(self.map[i]), x + window_size_w + 1)):
                x, y = self.coordinate[0], self.coordinate[1]
                distance = sqrt((j - x) ** 2 + (i - y) ** 2)
                if not self.in_detect_range(distance):
                    loc_str = 'X'
                elif not self.in_burn_through(distance):
                    loc_str = '_'
                else:
                    loc_str = '.'
                if self.map[i][j] == self:
                    loc_str = '@'
                elif self.map[i][j] is not None:
                    if self.detected(i, j, distance):
                        loc_str = '!'
                    # for debug
                    # elif self.in_detect_range(distance):
                    #     loc_str = '#'
                temp_str = loc_str
                while len(temp_str) < digit_w:
                    temp_str += loc_str
                print(temp_str, end='  ')
            print()

    def show_terrain_map(self):
        x, y = self.coordinate[0], self.coordinate[1]
        window_size_w = 5
        window_size_h = 10
        digit_w = len(str(self.terrain.shape[1]))
        digit_h = len(str(self.terrain.shape[0]))
        label = r'Y\X'
        while len(label) < digit_h:
            label = ' ' + label
        print(label, end='  ')
        for j in range(max(0, x - window_size_w), min(len(self.map[0]), x + window_size_w + 1)):
            j_str = str(j)
            while len(j_str) < max(digit_w, 11):
                j_str = '0' + j_str
            print(j_str, end='  ')
        print()
        for i in range(max(0, y - window_size_h), min(len(self.map), y + window_size_h + 1)):
            i_str = str(i)
            while len(i_str) < max(digit_h, len(label)):
                i_str = '0' + i_str
            print(i_str, end='  ')
            for j in range(max(0, x - window_size_w), min(len(self.map[i]), x + window_size_w + 1)):
                x, y = self.coordinate[0], self.coordinate[1]
                if x == j and y == i:
                    print('@@@/@@@/@@@', end='  ')
                else:
                    terrain = self.terrain[i, j, :]
                    temp_str = [terrain[0], terrain[1], terrain[2]]
                    temp_str = [str(element) for element in temp_str]
                    for k in range(3):
                        while len(list(temp_str[k])) < 3:
                            temp_str[k] = '0' + temp_str[k]
                    print('/'.join(temp_str), end='  ')
            print()

    def in_detect_range(self, distance):
        detect_range, _ = self.fleet.get_radar_range()
        return distance < detect_range

    def in_burn_through(self, distance):
        _, burn_through_range = self.fleet.get_radar_range()
        return distance < burn_through_range

    def detected(self, i, j, distance):
        if self.in_burn_through(distance):
            return True
        elif self.in_detect_range(distance):
            if type(self.map[i][j]) in self.events_pool['stealth'].keys():
                stealth_degree = self.events_pool['stealth'][type(self.map[i][j])]
                if type(stealth_degree) is list:
                    stealth_degree = random.randint(stealth_degree[0], stealth_degree[1])
                anti_stealth_degree = self.fleet.get_anti_stealth()
                if stealth_degree > anti_stealth_degree:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False

    def contact_events(self):
        x, y = self.coordinate[0], self.coordinate[1]
        dist = 1
        surround_locations = [
            [x + dist, y], [x - dist, y], [x, y + dist], [x, y - dist],
            [x - dist, y - dist], [x + dist, y + dist], [x - dist, y + dist], [x + dist, y - dist]
        ]
        surround_locations = [
            sl for sl in surround_locations if 0 <= sl[0] < len(self.map[0]) and 0 <= sl[1] < len(self.map)
        ]
        events = [[self.map[sl[1]][sl[0]], sl] for sl in surround_locations if self.map[sl[1]][sl[0]] is not None]
        return events

    def random_event(self, event, specified_player_fleet=None):
        # select an event in current event_pool
        # event = random.choice(game_obj.events_pool['events'])
        # the code above will be used in update_map
        # execute that event
        if specified_player_fleet is None:
            self.fleet, change_score = event(fleet_p=self.fleet)
        else:
            _, change_score = event(fleet_p=specified_player_fleet)
        # update flags by pool_flags
        update_score_and_flags(change_score, event, self)
        # check pools jumper with flags
        triggered_pools = gather_triggered_pools(self)
        if len(triggered_pools) > 0:
            next_pool = random.choice(triggered_pools)
            print('Event pool is switching to:', next_pool)
            new_events_pool = global_pools_dict[next_pool]
            self.events_pool = new_events_pool

    def display_score(self):
        print('Score:', self.score)

    @staticmethod
    def p2l(x0, y0, dx, dy, i, j):
        assert dx != 0
        k = dy / dx
        # (y - y0) = k * (x - x0)
        # 0 = k * x - y - k * x0 + y0
        a, b, c = k, -1, y0 - k * x0
        d = abs(a * j + b * i + c) / sqrt(a ** 2 + b ** 2)
        return d

    def save(self):
        old_game = vars(self)
        pickle.dump(old_game, open('save.pkl', 'wb'))


if __name__ == '__main__':
    g = Game()
    g.game_loop()
