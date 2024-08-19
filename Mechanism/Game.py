import random

import pygame.image
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP

pos_x = 640
pos_y = 360
ang = 0.0
mag_x = 100.0
mag_y = 100.0
flip = [False, False]

surface = pygame.image.load('Assets/F-5E.png')
active = False


class Game:
    engine_ptr = None

    def load_routine(self):
        self.engine_ptr.routine.append(update_game_logic)


def update_game_logic(params, recent_input):
    global pos_x, pos_y, ang, active, flip, mag_x, mag_y
    # 这里应根据游戏逻辑处理参数和输入，返回draw_dict
    # 示例draw_dict为一个包含待绘制内容的字典
    for event in recent_input:
        e = event[0]
        timestamp = event[1]
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            active = True
        elif e.type == MOUSEBUTTONUP and e.button == 1:
            active = False
        if active:
            pos_x += random.randint(-10, 10)
            pos_y += random.randint(-10, 10)
            ang += float(random.randint(-10, 10))
            mag_x += float(random.randint(-10, 10))
            mag_y += float(random.randint(-10, 10))
            if random.choice([True, False]):
                flip[0] = not flip[0]
            else:
                flip[1] = not flip[1]
    return '图形ID', (surface, (pos_x, pos_y), active, ang, (mag_x, mag_y), flip)
