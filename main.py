import os
import pickle
import random

from Classes.Fleet import Fleet
from Classes.Ship import Ship
from Classes.Weapon import Weapon
from Events.Area88 import rebel_attack, new_mercenary, volunteer_engineers, defection
from Events.TestEvents import a_ship_joins, a_ship_leaves, nothing_happened
from Utils import show_ship

events_list = [a_ship_joins, a_ship_leaves, nothing_happened]
events_chains = {
    '0#Area 88': {'condition': ['a88'], 'events_list': [rebel_attack, new_mercenary, volunteer_engineers, defection]}
}
add_flags = {a_ship_joins: ['a88']}
del_flags = {a_ship_leaves: ['a88']}


class Game:
    Fleet = None
    Score = None
    finished_chains = None
    flags = None

    def __init__(self):
        self.Score = 0
        self.Fleet = None
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
                if not self.load_fleet():
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
            self.Fleet = self.random_event(self.Fleet)
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
                self.save_fleet()
                return
            else:
                raise ValueError()

    def init_fleet(self):
        mh = random.randint(50, 101)
        mw = random.randint(5, 11)
        ship = Ship(mh=mh, mw=mw)
        p = random.randint(5, 15)
        t = random.randint(1, 10)
        ship.install_weapon(Weapon(p=p, t=t))
        self.Fleet = Fleet()
        self.Fleet.join(ship)
        self.Fleet.flag_ship = ship.uid

    def load_fleet(self):
        if os.path.exists('save.pkl'):
            save = pickle.load(open('save.pkl', 'rb'))
            self.Fleet = Fleet(init_params=save['Fleet'])
            self.Score = save['Score']
            self.finished_chains = save['Finished']
            self.flags = save['Flags']
            return True
        else:
            print('No previously saved game.')
            return False

    def save_fleet(self):
        pickle.dump(
            {'Fleet': self.Fleet.save(), 'Score': self.Score, 'Finished': self.finished_chains, 'Flags': self.flags},
            open('save.pkl', 'wb')
        )

    def show_status(self):
        for ship_uid in self.Fleet.ships.keys():
            ship = self.Fleet.ships[ship_uid]
            print('=========================')
            if ship_uid == self.Fleet.flag_ship:
                print('###Flag Ship###')
            show_ship(ship)

    def random_event(self, fleet):
        chains = list(events_chains.keys())
        priority_dict = {}
        [priority_dict.__setitem__(int(chain.split('#')[0]), chain) for chain in chains]
        temp_list = None
        for i in range(len(chains)):
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
        return self.Fleet.ships[self.Fleet.flag_ship].is_destroyed()

    def display_score(self):
        print('Score:', self.Score)


if __name__ == '__main__':
    g = Game()
    g.game_loop()
