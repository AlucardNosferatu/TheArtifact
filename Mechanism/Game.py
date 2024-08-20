class Game:
    engine_ptr = None
    routines = None
    loaded = None

    def __init__(self):
        self.loaded = False

    def load_engine(self, engine_ptr):
        self.engine_ptr = engine_ptr
        self.routines = {'w': self.engine_ptr.world_routine, 'u': self.engine_ptr.ui_routine}
        self.loaded = True

    def load_routine(self, func, r_type='w', multi_inst=False):
        if self.loaded:
            if not self.has_routine(func=func, r_type=r_type) or multi_inst:
                self.routines[r_type].append(func)

    def has_routine(self, func, r_type='w'):
        assert self.loaded
        return func in self.routines[r_type]

    def remove_routine(self, func, r_type='w'):
        if self.loaded:
            while self.has_routine(func=func, r_type=r_type):
                self.routines[r_type].remove(func)
