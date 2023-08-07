import os
import pickle
import random

from Classes.Fleet import Fleet
from Events.EventSystem import event_process, global_pools_dict
from Events.EventSystemDeprecated import events_chains, add_flags, del_flags
from Utils import a_ship_joins
from Battle.BattlePlan import show_status, clear_screen

clear = True


class Game:
    fleet = None
    score = None
    finished_chains = None
    flags = None

    def __init__(self):
        # self.events_pool = events_pool_default
        self.events_pool = global_pools_dict['default']
        self.score = 0
        self.fleet = None
        self.finished_chains = []
        self.flags = []

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

    def events_loop(self):
        global clear
        while True:
            # random event
            clear = clear_screen(clear)
            print('~~~~~~~~~~~~~~~~~~~~~~~~')
            # self.random_event_deprecated()
            self.random_event()
            # check game over
            if self.is_game_over():
                clear = clear_screen(clear)
                print('=======Game Over=======')
                self.display_score()
                return
            clear = False
            cmd = ''
            while cmd not in ['1', '3', '4']:
                clear = clear_screen(clear)
                print('~~~~~~~~~~~~~~~~~~~~~~~~')
                cmd = input('1.Continue\t2.Show Status\t3.Save & Exit\t4.Exit\n')
                if cmd == '2':
                    show_status(self.fleet)
                    clear = False
            if cmd == '1':
                continue
            elif cmd in ['3', '4']:
                if cmd == '3':
                    self.save()
                return
            else:
                raise ValueError()

    def init_fleet(self):
        self.fleet = Fleet()
        self.fleet = a_ship_joins(self.fleet, show=True)
        self.fleet.flag_ship = list(self.fleet.ships.keys())[0]

    def load(self):
        if os.path.exists('save.pkl'):
            old_game = pickle.load(open('save.pkl', 'rb'))
            self.score = old_game['score']
            self.fleet = old_game['fleet']
            self.finished_chains = old_game['finished_chains']
            self.flags = old_game['flags']
            self.events_pool = old_game['events_pool']
            return True
        else:
            print('No previously saved game.')
            return False

    def save(self):
        old_game = {}
        old_game.__setitem__('score', self.score)
        old_game.__setitem__('fleet', self.fleet)
        old_game.__setitem__('finished_chains', self.finished_chains)
        old_game.__setitem__('flags', self.flags)
        old_game.__setitem__('events_pool', self.events_pool)
        pickle.dump(old_game, open('save.pkl', 'wb'))

    def random_event(self):
        event_process(self)

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
