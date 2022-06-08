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
    location = [0.0, 0.0]
    speed = [0.0, 0.0]
    acc = [0.0, 0.0]
    ang = 0.0
    ang_speed = 0.0


class Input:
    throttle = 0
    pitch_sig = 0
    artifact_instance = None


class Artifact:
    ThisSpecs: None | Specs = None
    ThisStats: None | Stats = None
    ThisInput: None | Input = None

    def __init__(self, this_specs: Specs):
        self.ThisSpecs = this_specs
        self.ThisStats = Stats()
        self.ThisInput = Input()
