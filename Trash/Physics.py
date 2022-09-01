from math import sqrt


class PhyElement:
    mass: float
    mesh: list[float]
    # [x1,y1,x2,y2,...]
    uid: str
    center: list[float]
    # [x,y]
    radius: float

    # Circumscribed Circle
    def calc_dist(self, coordinate):
        dx = self.center[0] - coordinate[0]
        dy = self.center[1] - coordinate[1]
        return sqrt((dx ** 2) + (dy ** 2))


class PhyPool:
    ElementDict: dict[str, PhyElement]
    CollisionDict: dict[str, list[str]]

    def __init__(self):
        self.ElementDict = {}

    def add_element(self, new_e: PhyElement):
        if new_e.uid not in self.ElementDict:
            self.ElementDict.__setitem__(new_e.uid, new_e)

    def remove_element(self, uid):
        if uid in self.ElementDict:
            return self.ElementDict.pop(uid)
        else:
            return None

    def collision_analysis(self):
        self.CollisionDict.clear()
        for key in self.ElementDict:
            pe = self.ElementDict[key]
            for key2 in self.ElementDict:
                if key2 != key:
                    pe2 = self.ElementDict[key2]
                    dist = pe.calc_dist(pe2.center)
                    if dist <= pe.radius:
                        if key not in self.CollisionDict:
                            self.CollisionDict.__setitem__(key, [])
                        self.CollisionDict[key].append(key2)

    def update(self):
        # collision_analysis
        # static_force_analysis
        # movement_update
        # velocity_update
        pass
