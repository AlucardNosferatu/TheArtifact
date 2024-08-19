class Game:
    engine_ptr = None

    def load_routine(self, func):
        self.engine_ptr.routine.append(func)
