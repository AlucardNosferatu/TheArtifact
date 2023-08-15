from Weapons.Missile import Missile


class StrategicMissile(Missile):
    def __init__(self, explosion_range, launcher):
        super().__init__(explosion_range)
        self.launcher = launcher

    def strategic_function(self, game_obj, direction, speed):
        w_index = self.launcher.weapons.index(self)
        self.launcher.uninstall_weapon(w_index)
        # todo: how about an universal version of move_fleet?


class Probe(StrategicMissile):
    # todo: use probe to trigger non-battle event
    pass
