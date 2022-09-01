direction = {
    0: 2,
    2: 0,
    1: 3,
    3: 1
}


class Part:
    density: float
    connected = None
    connectors = None
    rotation: int
    neighbors = None
    location: [int, int]
    can_rotate: bool

    # 0123
    # 0123-上左下右,0-2,2-0,1-3,3-1
    def __init__(self, d: float, loc: [int, int], con_types: list[str], n, can_r=True):
        self.can_rotate = can_r
        self.density = d
        self.location = loc
        self.rotation = 0
        self.connected: list[Part | None] = [None, None, None, None]
        self.connectors: list[str | None] = con_types
        # con_types = ['struct', 'pipe', 'pass', 'pylon',None]
        self.neighbors: list[Part | None] = n
        self.connect_nearby()

    def connect_nearby(self):
        for i in range(4):
            if self.neighbors[i] is not None:
                n_ct = self.neighbors[i].connectors[direction[i]]
                if n_ct is not None and n_ct == self.connectors[i]:
                    self.connected[i] = self.neighbors[i]
                    self.neighbors[i].be_connected(self, direction[i])
                else:
                    self.connected[i] = None
                    self.neighbors[i].be_disconnected(direction[i])

    def be_connected(self, another_p, side):
        self.connected[side] = another_p

    def be_disconnected(self, side):
        self.connected[side] = None

    def rotate(self):
        if self.can_rotate:
            self.rotation += 1
            self.rotation %= 4
            self.connected: list[Part | None] = [None, None, None, None]
            self.connectors.insert(0, self.connectors.pop(-1))
            self.connect_nearby()


if __name__ == '__main__':
    cockpit = Part(d=0.5, loc=[0, 0], con_types=[None, 'pass', 'struct', None], n=[None, None, None, None])
    dorm = Part(d=0.5, loc=[-1, 0], con_types=[None, 'pass', 'struct', 'pass'], n=[None, None, None, cockpit])
    dorm.rotate()
    dorm.rotate()
    dorm.rotate()
    dorm.rotate()
    print('Done')
