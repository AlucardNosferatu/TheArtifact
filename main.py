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
    map_width = 1024
    map_height = 1024

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

    def update_map(self):
        # todo: implement map update
        x, y = self.coordinate[0], self.coordinate[1]
        # noinspection PyTypeChecker
        self.map[y][x] = self
        surround_locations = [
            [x + 2, y], [x - 2, y], [x, y + 2], [x, y - 2],
            [x - 2, y - 2], [x + 2, y + 2], [x - 2, y + 2], [x + 2, y - 2]
        ]
        surround_locations = [
            sl for sl in surround_locations if 0 <= sl[0] < len(self.map[0]) and 0 <= sl[1] < len(self.map)
        ]
        for i in range(8):
            location = surround_locations[i]
            x_loc, y_loc = location[0], location[1]
            self.map[y_loc][x_loc] = None
        for i in range(2):
            location = surround_locations[i]
            x_loc, y_loc = location[0], location[1]
            event = random.choice(self.events_pool['events'])
            self.map[y_loc][x_loc] = event

    def show_map(self):
        x, y = self.coordinate[0], self.coordinate[1]
        for i in range(max(0, y - 10), min(len(self.map), y + 11)):
            for j in range(max(0, x - 10), min(len(self.map[i]), x + 11)):
                if self.map[i][j] is None:
                    print('_', end='  ')
                else:
                    if self.map[i][j] == self:
                        print('@', end='  ')
                    else:
                        print('!', end='  ')
            print()

    def contact_events(self):
        x, y = self.coordinate[0], self.coordinate[1]
        surround_locations = [
            [x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1],
            [x - 1, y - 1], [x + 1, y + 1], [x - 1, y + 1], [x + 1, y - 1]
        ]
        surround_locations = [
            sl for sl in surround_locations if 0 <= sl[0] < len(self.map[0]) and 0 <= sl[1] < len(self.map)
        ]
        events = [[self.map[sl[1]][sl[0]], sl] for sl in surround_locations if self.map[sl[1]][sl[0]] is not None]
        return events

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
                print('~~~~~~~~~~~~~~~~~~~~~~~~')
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
                if cmd == '3':
                    self.save()
                return
            else:
                raise ValueError()

    def move_fleet(self, direction, speed):
        global clear
        x, y = self.coordinate[0], self.coordinate[1]
        self.map[y][x] = None
        dx, dy = int(direction.split(',')[0]), int(direction.split(',')[1])
        ds = max(1, round(sqrt(dx ** 2 + dy ** 2)))
        dx, dy = round(speed * dx / ds), round(speed * dy / ds)
        x_new, y_new = min(max(0, x + dx), self.map_width - 1), min(max(0, y + dy), self.map_height - 1)
        self.coordinate = [x_new, y_new]
        if self.map[y_new][x_new] is not None:
            # todo: extend encounter logic
            print('Something happened as soon as our fleet arrived the destination!')
            event_func = self.map[y_new][x_new]
            self.random_event(event_func)
            if self.is_game_over():
                return
        # noinspection PyTypeChecker
        self.map[y_new][x_new] = self
        print('Move from {},{} to {},{} at speed:{}, direction:{}'.format(x, y, x_new, y_new, speed, direction))

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

    def save(self):
        old_game = vars(self)
        pickle.dump(old_game, open('save.pkl', 'wb'))

    def random_event(self, event):
        event_process(self, event)

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

    def is_game_over(self):
        return self.fleet.ships[self.fleet.flag_ship].is_destroyed()

    def display_score(self):
        print('Score:', self.score)


if __name__ == '__main__':
    g = Game()
    g.game_loop()
