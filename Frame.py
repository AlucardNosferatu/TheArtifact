from math import sqrt


class Beam:
    start_point: list[float]
    end_point: list[float]
    attached_beam = None

    def __init__(self, sp: list[float], ep: list[float]):
        self.start_point = sp
        self.end_point = ep
        self.attached_beam: list[Beam | None] = [None, None]

    def attach(self, index, another_b, another_i):
        self.be_attached(index, another_b)
        another_b.be_attached(another_i, self)

    def be_attached(self, index, another_b):
        self.attached_beam[index] = another_b

    def detach(self, index):
        another_b: Beam = self.attached_beam[index]
        another_i = another_b.attached_beam.index(self)
        self.be_detached(index)
        another_b.be_detached(another_i)

    def be_detached(self, index):
        self.attached_beam[index] = None

    def find_nearest_attach_p(self, index, another_b):
        if index == 0:
            attach_p = self.start_point
        else:
            attach_p = self.end_point
        ab_sp = another_b.start_point
        ab_sp_dx = ab_sp[0] - attach_p[0]
        ab_sp_dy = ab_sp[1] - attach_p[1]
        ab_sp_dst = sqrt((ab_sp_dx ** 2) + (ab_sp_dy ** 2))
        ab_ep = another_b.end_point
        ab_ep_dx = ab_ep[0] - attach_p[0]
        ab_ep_dy = ab_ep[1] - attach_p[1]
        ab_ep_dst = sqrt((ab_ep_dx ** 2) + (ab_ep_dy ** 2))
        dst_list = [ab_sp_dst, ab_ep_dst]
        return dst_list.index(min(dst_list))

    def change_point(self, index, new_p):
        if index == 0:
            self.start_point = new_p
        else:
            self.end_point = new_p

    def snap_to_beam(self, index, another_b):
        another_i = self.find_nearest_attach_p(index, another_b)
        if another_i == 0:
            new_p = another_b.start_point
        else:
            new_p = another_b.end_point
        self.change_point(index, new_p)
        self.attach(index, another_b, another_i)


if __name__ == '__main__':
    b1 = Beam([-20, -20], [20, 20])
    b2 = Beam([60, -20], [40, 20])
    b2.snap_to_beam(1, b1)
    print('Done')
