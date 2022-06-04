class Design:
    pass


class Part:
    hp = 0
    cost = 0


class Chassis(Part):
    engines_slot = None
    weapons_slot = None
    locomotive_slot = None

    def __init__(self, sma_eng, med_eng, lar_eng, sma_wpn, med_wpn, lar_wpn, sma_loc, med_loc, lar_loc):
        self.engines_slot = {'small': sma_eng, 'medium': med_eng, 'large': lar_eng}
        self.weapons_slot = {'small': sma_wpn, 'medium': med_wpn, 'large': lar_wpn}
        self.locomotive_slot = {'small': sma_loc, 'medium': med_loc, 'large': lar_loc}


class Weapon(Part):
    fire_rate = 0
    accuracy = 0
    effective_range = 0
    warhead_in_use = None

    def __init__(self, rof, acc, e_range):
        self.fire_rate = rof
        self.accuracy = acc
        self.effective_range = e_range

    def load_warhead(self, wh):
        self.warhead_in_use = wh


class Warhead(Weapon):
    damage = 0
    damage_type = 0
    cluster_warhead = None
    speed = 0
    ang_speed = 0

    def __init__(self, cw, damage, dt, spd, ang_spd):
        super().__init__(-1, -1, -1)
        self.speed = spd
        self.ang_speed = ang_spd
        self.cluster_warhead = cw
        self.damage = damage
        self.damage_type = dt
