import os
import pickle
import random

from Classes.Fleet import Fleet
from Classes.Ship import Ship
from Classes.Weapon import Weapon
from Events.TestEvents import a_ship_joins, a_ship_leaves, nothing_happened

events_list = [a_ship_joins, a_ship_leaves, nothing_happened]


class Game:
    Fleet = None

    def __init__(self):
        self.Score = 0

        self.Fleet = None

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

    def init_fleet(self):
        mh = random.randint(50, 101)
        mw = random.randint(5, 11)
        ship = Ship(mh=mh, mw=mw)
        p = random.randint(5, 15)
        t = random.randint(1, 10)
        ship.install_weapon(Weapon(p=p, t=t))
        self.Fleet = Fleet()
        self.Fleet.join(ship)
        self.Fleet.FlagShip = ship.UID

    def load_fleet(self):
        if os.path.exists('save.pkl'):
            save = pickle.load(open('save.pkl', 'rb'))
            self.Fleet = Fleet(init_params=save['Fleet'])
            self.Score = save['Score']
            return True
        else:
            print('No previously saved game.')
            return False

    def save_fleet(self):
        pickle.dump({'Fleet': self.Fleet.save(), 'Score': self.Score}, open('save.pkl', 'wb'))

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

    def show_status(self):
        for ship_uid in self.Fleet.Ships.keys():
            ship = self.Fleet.Ships[ship_uid]
            print('=========================')
            if ship_uid == self.Fleet.FlagShip:
                print('###Flag Ship###')
            print('Ship ID:', ship.UID)
            print('Ship HP:', ship.HitPoints, '/', ship.MaxHitPoints)
            for i in range(len(ship.Weapons)):
                weapon = ship.Weapons[i]
                print('+++++++++++++++++++++++++')
                print('Weapon:', i, 'Power:', weapon.Power, 'Targets:', weapon.Targets)

    def random_event(self, fleet):
        self.Fleet = fleet
        event = random.choice(events_list)
        fleet = event(fleet)
        # todo: add some events to make game interesting
        return fleet

    def is_game_over(self):
        return self.Fleet.Ships[self.Fleet.FlagShip].is_destroyed()

    def display_score(self):
        print('Score:', self.Score)


if __name__ == '__main__':
    g = Game()
    g.game_loop()
