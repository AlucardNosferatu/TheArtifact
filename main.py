import os
import pickle
import random

from Classes.Fleet import Fleet
from Events.Area88 import new_mercenary, volunteer_engineers, defection
from Events.Battle import battle_event
from Events.TestEvents import nothing_happened
from Utils import show_ship, a_ship_joins, a_ship_leaves

events_list = [a_ship_joins, a_ship_leaves, nothing_happened]
events_chains = {
    '0#Area 88': {'condition': ['a88'], 'events_list': [battle_event, new_mercenary, volunteer_engineers, defection]}
}
add_flags = {a_ship_joins: ['a88']}
del_flags = {a_ship_leaves: ['a88']}


class Game:
    fleet = None
    score = None
    finished_chains = None
    flags = None

    def __init__(self):
        self.score = 0
        self.fleet = None
        self.finished_chains = []
        self.flags = []

    def game_loop(self):
        while True:
            cmd = ''
            while cmd not in ['1', '2', '3']:
                cmd = input('1.New Game\n2.Old Game\n3.Exit')
            if cmd == '1':
                self.init_fleet()
            elif cmd == '2':
                if not self.load():
                    continue
            elif cmd == '3':
                os.abort()
            else:
                raise ValueError()
            self.events_loop()

    def events_loop(self):
        while True:
            # random event
            print('~~~~~~~~~~~~~~~~~~~~~~~~')
            self.fleet = self.random_event(self.fleet)
            # check game over
            if self.is_game_over():
                self.display_score()
                return
            cmd = ''
            while cmd not in ['1', '3']:
                cmd = input('1.Continue\n2.Show Status\n3.Save & Exit')
                if cmd == '2':
                    self.show_status()
            if cmd == '1':
                continue
            elif cmd == '3':
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
        pickle.dump(old_game, open('save.pkl', 'wb'))

    def show_status(self):
        for ship_uid in self.fleet.ships.keys():
            ship = self.fleet.ships[ship_uid]
            print('=========================')
            if ship_uid == self.fleet.flag_ship:
                print('###Flag Ship###')
            show_ship(ship)

    def random_event(self, fleet):
        chains = list(events_chains.keys())
        priority_dict = {}
        [priority_dict.__setitem__(int(chain.split('#')[0]), chain) for chain in chains]
        temp_list = None
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
                        temp_list = check_chain['events_list']
        if temp_list is None:
            temp_list = events_list
        event = random.choice(temp_list)
        fleet = event(fleet)
        if event in add_flags.keys():
            for flag in add_flags[event]:
                if flag not in self.flags:
                    self.flags.append(flag)
        if event in del_flags.keys():
            for flag in del_flags[event]:
                if flag in self.flags:
                    self.flags.remove(flag)
        # todo: add some events to make game interesting
        return fleet

    def is_game_over(self):
        return self.fleet.ships[self.fleet.flag_ship].is_destroyed()

    def display_score(self):
        print('Score:', self.score)


if __name__ == '__main__':
    g = Game()
    g.game_loop()
