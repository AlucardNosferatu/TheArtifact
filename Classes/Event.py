from Config import default_event_life


class Event:
    def __init__(self, e_func, life=None):
        self.event_function = e_func
        self.end = False
        if life is None:
            life = default_event_life
        self.life = life
        self.lived = 1

    def __call__(self, *args, **kwargs):
        fleet, score = self.event_function(*args, **kwargs)
        if hasattr(self, 'next_e_func'):
            self.event_function = self.next_e_func
            delattr(self, 'next_e_func')
        else:
            self.end = True
        return fleet, score

    def aging_and_checking_life(self):
        if self.lived >= self.life:
            return True
        else:
            self.lived += 1
            return False

    @staticmethod
    def clear_timeout_event(game_obj):
        count = 0
        for i in range(len(game_obj.map)):
            for j in range(len(game_obj.map[i])):
                if game_obj.map[i][j] is not None:
                    if type(game_obj.map[i][j]) is not None and game_obj.map[i][j] != game_obj:
                        if game_obj.map[i][j].aging_and_checking_life():
                            game_obj.map[i][j] = None
                            count += 1
        print('{} events disappeared!'.format(count))


class City(Event):
    def aging_and_checking_life(self):
        return False
