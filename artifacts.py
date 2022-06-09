class Specs:
    health_points = None
    bare_weight = None
    fuel_capacity = None
    thrust = None
    consumption = None
    maneuver = None
    drag = None
    special_functions = None

    def __init__(self, params):
        self.health_points = params['health_points']
        self.bare_weight = params['bare_weight']
        self.fuel_capacity = params['fuel_capacity']
        self.thrust = params['thrust']
        self.consumption = params['consumption']
        self.maneuver = params['maneuver']
        self.drag = params['drag']
        self.special_functions = params['special_functions']


class Stats:
    total_mass = None
    fuel_stored = None
    speed = None
    acc = None

    def __init__(self, bare_weight):
        self.total_mass = bare_weight
        self.fuel_stored = 0
        self.speed = 0
        self.acc = 0


class Input:
    throttle = None
    yaw_sig = None

    def __init__(self):
        self.throttle = 0
        self.yaw_sig = 0


class Artifact:
    ThisSpecs: None | Specs = None
    ThisStats: None | Stats = None
    ThisInput: None | Input = None

    def __init__(self, this_specs: Specs):
        self.ThisSpecs = this_specs
        self.ThisStats = Stats(bare_weight=self.ThisSpecs.bare_weight)
        self.ThisInput = Input()
