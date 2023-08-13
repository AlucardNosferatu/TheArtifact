import os
import pickle
import random
from math import sqrt

from Battle.BattlePlan import clear_screen
from Classes.Fleet import Fleet
from Events.EventSystem import event_process, global_pools_dict
from Events.EventSystemDeprecated import events_chains, add_flags, del_flags
from Utils import a_ship_joins

clear = True


class Game:
    fleet = None
    score = None
    finished_chains = None
    flags = None
    killed = None
    battles = None
    map = None
    coordinate = None
    map_width = 512
    map_height = 512

    def __init__(self):
        # self.events_pool = events_pool_default
        self.events_pool = global_pools_dict['default']
        self.score = 0
        self.fleet = None
        self.finished_chains = []
        self.flags = []
        self.killed = 0
        self.battles = 0
        self.map = []
        row = []
        for _ in range(Game.map_width):
            row.append(None)
        for _ in range(Game.map_height):
            self.map.append(row.copy())
        self.coordinate = [int(0.5 * Game.map_width), int(0.5 * Game.map_height)]

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
                # self.random_event_deprecated()
                self.update_map()
                self.show_map()
                clear = False
                events = self.contact_events()
                while not self.is_game_over() and len(events) > 0:
                    event = random.choice(events)
                    location = event[1]
                    event_func = event[0]
                    self.random_event(event_func)
                    events.remove(event)
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
                print('~~~~~~~~~~~~~~~~~~~~~~~~')
                cmd = input('1.Hold Position\t2.Manage Fleet\t3.Move\t4.Save & Exit\t5.Exit\n')
                if cmd == '2':
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
                    full_speed = self.fleet.get_cruise_speed()
                    speed = max(1, round(full_speed * float(s_factor) / 100))
                    self.move_fleet(direction, speed)
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
        x, y = self.coordinate[0], self.coordinate[1]
        # noinspection PyTypeChecker
        self.map[y][x] = self
        dist = 1
        surround_locations = [
            [x + dist, y], [x - dist, y], [x, y + dist], [x, y - dist],
            [x - dist, y - dist], [x + dist, y + dist], [x - dist, y + dist], [x + dist, y - dist]
        ]
        surround_locations = [
            sl for sl in surround_locations if 0 <= sl[0] < len(self.map[0]) and 0 <= sl[1] < len(self.map)
        ]
        # for i in range(8):
        #     location = surround_locations[i]
        #     x_loc, y_loc = location[0], location[1]
        #     self.map[y_loc][x_loc] = None
        for i in range(2):
            location = random.choice(surround_locations)
            x_loc, y_loc = location[0], location[1]
            event = random.choice(self.events_pool['events'])
            self.map[y_loc][x_loc] = event()
            surround_locations.remove(location)

    def show_map(self):
        x, y = self.coordinate[0], self.coordinate[1]
        window_size_w = 15
        window_size_h = 10
        digit_w = len(str(self.map_width))
        digit_h = len(str(self.map_height))
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
                temp_str = loc_str
                while len(temp_str) < digit_w:
                    temp_str += loc_str
                print(temp_str, end='  ')
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
            if self.map[i][j] in self.events_pool['stealth'].keys():
                stealth_degree = self.events_pool['stealth'][self.map[i][j]]
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

    def random_event(self, event, specified_fleet=None):
        event_process(self, event, specified_fleet=specified_fleet)

    def random_event_deprecated(self):
        # select event form pool
        event = random.choice(self.events_pool)
        # execute that event
        self.fleet, change_score = event(self.fleet)
        # update flags by pool_flags
        self.score += change_score
        if event in add_flags.keys():
            for flag in add_flags[event]:
                if flag not in self.flags:
                    self.flags.append(flag)
        if event in del_flags.keys():
            for flag in del_flags[event]:
                if flag in self.flags:
                    self.flags.remove(flag)

        chains = list(events_chains.keys())
        priority_dict = {}
        [priority_dict.__setitem__(int(chain.split('#')[0]), chain) for chain in chains]
        for i in range(len(chains)):
            if i in priority_dict.keys():
                if priority_dict[i] not in self.finished_chains:
                    check_chain = events_chains[priority_dict[i]]
                    condition = check_chain['condition']
                    triggered = True
                    for flag in condition:
                        if flag not in self.flags:
                            triggered = False
                            break
                    if triggered:
                        self.events_pool = check_chain['events_pool']

    def display_score(self):
        print('Score:', self.score)

    def move_fleet(self, direction, speed):
        global clear
        x, y = self.coordinate[0], self.coordinate[1]
        self.map[y][x] = None
        dx, dy = int(direction.split(',')[0]), int(direction.split(',')[1])
        ds = max(1, round(sqrt(dx ** 2 + dy ** 2)))
        dx, dy = round(speed * dx / ds), round(speed * dy / ds)
        x_new, y_new = min(max(0, x + dx), self.map_width - 1), min(max(0, y + dy), self.map_height - 1)
        self.coordinate = [x_new, y_new]
        events = self.trail_events(x, y, dx, dy)
        if len(events) > 0:
            print('Something happened on the route to destination!')
        while len(events) > 0:
            event = events.pop(0)
            location = event[1]
            event_func = event[0]
            self.random_event(event_func)
            self.map[location[1]][location[0]] = None
            if self.is_game_over():
                return
        if self.map[y_new][x_new] is not None:
            print('Something happened as soon as our fleet arrived the destination!')
            event_func = self.map[y_new][x_new]
            self.random_event(event_func)
            self.map[y_new][x_new] = None
            if self.is_game_over():
                return
        # noinspection PyTypeChecker
        self.map[y_new][x_new] = self
        print('Move from {},{} to {},{} at speed:{}, direction:{}'.format(x, y, x_new, y_new, speed, direction))

    def trail_events(self, x0, y0, dx, dy, trigger_radius=2, specified_fleet=None):
        # todo: implement encounter logic
        k = dy / dx
        # (y - y0) = k * (x - x0)
        # 0 = k * x - y - k * x0 + y0
        a, b, c = k, -1, y0 - k * x0
        events = []
        for i in range(self.map_height):
            for j in range(self.map_width):
                d = self.p2l(a, b, c, i, j)
                if d < trigger_radius:
                    if self.map[i][j] is not None:
                        event = self.map[i][j]
                        location = [j, i]
                        if specified_fleet is None:
                            events.append([event, location])
                        else:
                            events.append([event, location, specified_fleet])
        return events

    @staticmethod
    def p2l(a, b, c, i, j):
        d = abs(a * j + b * i + c) / sqrt(a ** 2 + b ** 2)
        return d

    def save(self):
        old_game = vars(self)
        pickle.dump(old_game, open('save.pkl', 'wb'))


if __name__ == '__main__':
    g = Game()
    g.game_loop()
