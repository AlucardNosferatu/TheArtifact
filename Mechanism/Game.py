import threading
import time


class Game:
    engine_ptr = None
    routines = None
    loaded = None
    params = None
    eg_thread = None

    def __init__(self):
        self.loaded = False

    def load_engine(self, engine_ptr):
        self.engine_ptr = engine_ptr
        self.routines = {'w': self.engine_ptr.world_routine, 'u': self.engine_ptr.ui_routine}
        self.params = self.engine_ptr.params
        self.loaded = True

    def append_routine(self, func, r_type='w', multi_inst=False):
        if self.loaded:
            if not self.has_routine(func=func, r_type=r_type) or multi_inst:
                self.routines[r_type].append(func)

    def insert_routine(self, func, r_type='w', multi_inst=False):
        if self.loaded:
            if not self.has_routine(func=func, r_type=r_type) or multi_inst:
                self.routines[r_type].insert(0, func)

    def has_routine(self, func, r_type='w'):
        assert self.loaded
        return func in self.routines[r_type]

    def remove_routine(self, func, r_type='w', purge=True):
        if self.loaded:
            while self.has_routine(func=func, r_type=r_type):
                self.routines[r_type].remove(func)
                if not purge:
                    break

    def execute_game(self):
        for routine_func in self.engine_ptr.world_routine:
            spr_key, spr = routine_func(params=self.params, recent_input=self.engine_ptr.recent_input)
            if spr_key is not None:
                self.engine_ptr.renderer.world_draw[spr_key] = spr
        for routine_func in self.engine_ptr.ui_routine:
            spr_key, spr = routine_func(params=self.params, recent_input=self.engine_ptr.recent_input)
            if spr_key is not None:
                self.engine_ptr.renderer.ui_draw[spr_key] = spr
        time.sleep(0.99/self.engine_ptr.fps)

    def execute_game_loop(self):
        while True:
            self.execute_game()

    def ignite(self):
        self.eg_thread = threading.Thread(target=self.execute_game_loop)
        self.eg_thread.start()
