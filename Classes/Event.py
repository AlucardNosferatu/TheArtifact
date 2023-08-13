class Event:
    def __init__(self, e_func):
        self.event_function = e_func
        self.end = False

    def __call__(self, *args, **kwargs):
        fleet, score = self.event_function(*args, **kwargs)
        self.end = True
        return fleet, score
