from math import sqrt

import pygame

from Engine.Core import Core
from Mechanism.Game import Game
from Mechanism.UI import Button, Camera, EntitySprite, KeyboardButton, Mouse

if __name__ == '__main__':
    game = Game()
    core = Core(game_obj=game)

    cam = Camera(screen=core.renderer.screen)
    cam.world_x = 960
    cam.world_y = 540
    city = EntitySprite(name='city', image_path='Assets/city.png', cam=cam, world_x=960, world_y=540, game=game)
    city.scale_x = 200.0
    city.scale_y = 200.0
    city.check_visibility = False
    jet = EntitySprite(name='jet', image_path='Assets/F-5E.png', cam=cam, world_x=960, world_y=540, game=game)


    def btn_up(params, recent_input):
        _, _ = params, recent_input
        print('up')
        cam.world_y -= 16
        return None, None


    def btn_down(params, recent_input):
        _, _ = params, recent_input
        print('down')
        cam.world_y += 16
        return None, None


    def btn_left(params, recent_input):
        _, _ = params, recent_input
        print('left')
        cam.world_x -= 16
        return None, None


    def btn_right(params, recent_input):
        _, _ = params, recent_input
        print('right')
        cam.world_x += 16
        return None, None


    def btn_jet_up(params, recent_input):
        _, _ = params, recent_input
        print('jet_up')
        jet.world_y -= 16
        return None, None


    def btn_jet_down(params, recent_input):
        _, _ = params, recent_input
        print('jet_down')
        jet.world_y += 16
        return None, None


    def btn_jet_left(params, recent_input):
        _, _ = params, recent_input
        print('jet_left')
        jet.world_x -= 16
        return None, None


    def btn_jet_right(params, recent_input):
        _, _ = params, recent_input
        print('jet_right')
        jet.world_x += 16
        return None, None


    def mouse_click(params, recent_input):
        _, _ = params, recent_input
        (mx, my) = pygame.mouse.get_pos()
        m_w_x = mx - round(cam.w / 2) + cam.world_x
        m_w_y = my - round(cam.h / 2) + cam.world_y
        d_w_x = m_w_x - jet.world_x
        d_w_y = m_w_y - jet.world_y
        dist = sqrt((d_w_x ** 2) + (d_w_y ** 2))
        spd = 16
        err = 2 * spd
        if dist > err:
            s_w_x = round(spd * d_w_x / dist)
            s_w_y = round(spd * d_w_y / dist)
            jet.world_x += s_w_x
            jet.world_y += s_w_y
        return None, None


    up = Button(name='up', image_path='Assets/btn.png', x=640, y=8, game=game)
    down = Button(name='down', image_path='Assets/btn.png', x=640, y=712, game=game)
    left = Button(name='left', image_path='Assets/btn.png', x=8, y=360, game=game)
    right = Button(name='right', image_path='Assets/btn.png', x=1272, y=360, game=game)

    jet_up = Button(name='jet_up', image_path='Assets/btn.png', x=1212, y=612, game=game)
    jet_down = Button(name='jet_down', image_path='Assets/btn.png', x=1212, y=692, game=game)
    jet_left = Button(name='jet_left', image_path='Assets/btn.png', x=1172, y=652, game=game)
    jet_right = Button(name='jet_right', image_path='Assets/btn.png', x=1252, y=652, game=game)

    jet_up.scale_x = 50.0
    jet_up.scale_y = 50.0
    jet_down.scale_x = 50.0
    jet_down.scale_y = 50.0
    jet_left.scale_x = 50.0
    jet_left.scale_y = 50.0
    jet_right.scale_x = 50.0
    jet_right.scale_y = 50.0

    w = KeyboardButton(name='w', game=game, trigger_key=pygame.K_w)
    s = KeyboardButton(name='s', game=game, trigger_key=pygame.K_s)
    a = KeyboardButton(name='a', game=game, trigger_key=pygame.K_a)
    d = KeyboardButton(name='d', game=game, trigger_key=pygame.K_d)

    arrow_up = KeyboardButton(name='arrow_up', game=game, trigger_key=pygame.K_UP)
    arrow_down = KeyboardButton(name='arrow_down', game=game, trigger_key=pygame.K_DOWN)
    arrow_left = KeyboardButton(name='arrow_left', game=game, trigger_key=pygame.K_LEFT)
    arrow_right = KeyboardButton(name='arrow_right', game=game, trigger_key=pygame.K_RIGHT)

    mouse_cursor = Mouse(name='mouse_cursor', game=game, trigger_key=1)

    up.reg_callback(callback=btn_up)
    down.reg_callback(callback=btn_down)
    left.reg_callback(callback=btn_left)
    right.reg_callback(callback=btn_right)

    w.reg_callback(callback=btn_up)
    s.reg_callback(callback=btn_down)
    a.reg_callback(callback=btn_left)
    d.reg_callback(callback=btn_right)

    jet_up.reg_callback(callback=btn_jet_up)
    jet_down.reg_callback(callback=btn_jet_down)
    jet_left.reg_callback(callback=btn_jet_left)
    jet_right.reg_callback(callback=btn_jet_right)

    arrow_up.reg_callback(callback=btn_jet_up)
    arrow_down.reg_callback(callback=btn_jet_down)
    arrow_left.reg_callback(callback=btn_jet_left)
    arrow_right.reg_callback(callback=btn_jet_right)

    mouse_cursor.reg_callback(callback=mouse_click)

    core.engine_run()
