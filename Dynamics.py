import math


class Artifact:
    ThisSpecs = None
    ThisStats = None
    ThisInput = None

    def __init__(self):
        self.ThisInput = Input(art_inst=self)
        self.ThisStats = Stats()
        self.ThisSpecs = Specs()

    def update_stats(self, drag, gravity):
        self.ThisStats.update_loc()

        pit = self.ThisInput.pitch_sig
        maa = self.ThisSpecs.max_ang_acc
        mas = self.ThisSpecs.max_ang_spd
        self.ThisStats.update_ang(pit_sig=pit, max_ang_acc=maa, max_ang_spd=mas, drag=drag)

        thr = self.ThisInput.throttle
        ma = self.ThisSpecs.max_acc
        ms = self.ThisSpecs.max_spd
        self.ThisStats.update_spd(throttle=thr, max_acc=ma, max_spd=ms, drag=drag, gravity=gravity)


class Specs:
    max_acc = 9
    max_spd = 12
    max_ang_acc = 2
    max_ang_spd = 4

    def __init__(self):
        self.max_acc = 3
        self.max_spd = 12
        self.max_ang_acc = 3
        self.max_ang_spd = 5


class Stats:
    location = [0.0, 0.0]
    speed = [0.0, 0.0]
    acc = [0.0, 0.0]
    ang = 0.0
    ang_speed = 0.0

    def __init__(self):
        self.location = [0.0, 0.0]
        self.speed = [0.0, 0.0]
        self.acc = [0.0, 0.0]
        self.ang = 0.0
        self.ang_speed = 0.0

    def update_ang(self, pit_sig, max_ang_acc, max_ang_spd, drag):
        self.ang_speed += pit_sig * max_ang_acc
        if self.ang_speed > 1:
            self.ang_speed -= math.sqrt(0.5 * drag)
        elif self.ang_speed < -1:
            self.ang_speed += math.sqrt(0.5 * drag)
        if self.ang_speed > max_ang_spd:
            self.ang_speed = max_ang_spd
        elif -self.ang_speed > max_ang_spd:
            self.ang_speed = -max_ang_spd

        self.ang += self.ang_speed

    def update_spd(self, throttle, max_acc, max_spd, drag, gravity):
        self.acc = throttle * max_acc
        self.acc -= drag
        if self.acc > max_acc:
            self.acc = max_acc
        elif self.acc < 0:
            self.acc = 0.0

        dv_x = self.acc * math.cos(self.ang * 3.14 / 180)
        dv_y = self.acc * -math.sin(self.ang * 3.14 / 180)
        print(self.acc, math.cos(self.ang * 3.14 / 180), math.sin(self.ang * 3.14 / 180))
        if self.location[1] > 0:
            dv_y -= gravity
        self.speed[0] += dv_x
        self.speed[1] += dv_y
        spd_mag = math.sqrt(self.speed[0] ** 2 + self.speed[1] ** 2)
        if spd_mag > max_spd:
            ratio = max_spd / spd_mag
            self.speed[0] *= ratio
            self.speed[1] *= ratio

    def update_loc(self):
        self.location[0] += self.speed[0]
        self.location[1] += self.speed[1]
        print('speed', self.speed)
        if self.location[1] < 0:
            self.location[1] = 0
        if self.location[0] < 0:
            self.location[0] = 0
        elif self.location[0] > 1023:
            self.location[0] = 1023


class Input:
    throttle = 0
    pitch_sig = 0
    artifact_instance = None

    def __init__(self, art_inst: Artifact):
        self.throttle = 0.0
        self.pitch_sig = 0.0
        self.artifact_instance = art_inst

    def pitch_up(self):
        self.pitch_sig += 0.01
        if self.pitch_sig > 1:
            self.pitch_sig = 1

    def pitch_down(self):
        self.pitch_sig -= 0.01
        if self.pitch_sig < -1:
            self.pitch_sig = -1

    def pitch_neutral(self):
        self.pitch_sig = 0

    def throttle_up(self):
        self.throttle += 0.01
        if self.throttle > 1:
            self.throttle = 1

    def throttle_down(self):
        self.throttle -= 0.01
        if self.throttle < 0:
            self.throttle = 0
