import os
from math import sqrt

import pygame

from Engine.Core import Core
from Mechanism.Game import World

if __name__ == '__main__':
    core = Core()

    world = World(core=core, map_image='Assets/city.png')
    world.new_entity(ent_id='1#jet', image_path='Assets/F-5E.png', world_x=960, world_y=540)


    def cam_u(params, recent_input):
        _, _ = params, recent_input
        world.camera.move(d_y=-16)
        return None, None


    def cam_d(params, recent_input):
        _, _ = params, recent_input
        world.camera.move(d_y=16)
        return None, None


    def cam_l(params, recent_input):
        _, _ = params, recent_input
        world.camera.move(d_x=-16)
        return None, None


    def cam_r(params, recent_input):
        _, _ = params, recent_input
        world.camera.move(d_x=16)
        return None, None


    def jet_u(params, recent_input):
        _, _ = params, recent_input
        jet = world.get_entity(ent_id='1#jet')
        if jet is not None:
            jet.move(d_y=-16)
        return None, None


    def jet_d(params, recent_input):
        _, _ = params, recent_input
        jet = world.get_entity(ent_id='1#jet')
        if jet is not None:
            jet.move(d_y=16)
        return None, None


    def jet_l(params, recent_input):
        _, _ = params, recent_input
        jet = world.get_entity(ent_id='1#jet')
        if jet is not None:
            jet.move(d_x=-16)
        return None, None


    def jet_r(params, recent_input):
        _, _ = params, recent_input
        jet = world.get_entity(ent_id='1#jet')
        if jet is not None:
            jet.move(d_x=16)
        return None, None


    def jet_m(params, recent_input):
        _, _ = params, recent_input
        m_w_x, m_w_y = world.camera.mouse_world_pos()
        jet = world.get_entity(ent_id='1#jet')
        if jet is not None:
            d_w_x = m_w_x - jet.world_x
            d_w_y = m_w_y - jet.world_y
            dist = sqrt((d_w_x ** 2) + (d_w_y ** 2))
            spd = 16
            err = 2 * spd
            if dist > err:
                s_w_x = round(spd * d_w_x / dist)
                s_w_y = round(spd * d_w_y / dist)
                jet.move(d_x=s_w_x, d_y=s_w_y)
        return None, None


    world.new_stimulation(sti_id='btn_cam_u', sti_type='button', image_path='Assets/btn.png', x=640, y=8)
    world.new_stimulation(sti_id='btn_cam_d', sti_type='button', image_path='Assets/btn.png', x=640, y=712)
    world.new_stimulation(sti_id='btn_cam_l', sti_type='button', image_path='Assets/btn.png', x=8, y=360)
    world.new_stimulation(sti_id='btn_cam_r', sti_type='button', image_path='Assets/btn.png', x=1272, y=360)
    world.new_stimulation(sti_id='btn_jet_u', sti_type='button', image_path='Assets/btn.png', x=1212, y=612)
    world.new_stimulation(sti_id='btn_jet_d', sti_type='button', image_path='Assets/btn.png', x=1212, y=692)
    world.new_stimulation(sti_id='btn_jet_l', sti_type='button', image_path='Assets/btn.png', x=1172, y=652)
    world.new_stimulation(sti_id='btn_jet_r', sti_type='button', image_path='Assets/btn.png', x=1252, y=652)
    world.new_stimulation(sti_id='w', sti_type='keyboard', trigger_key=pygame.K_w)
    world.new_stimulation(sti_id='s', sti_type='keyboard', trigger_key=pygame.K_s)
    world.new_stimulation(sti_id='a', sti_type='keyboard', trigger_key=pygame.K_a)
    world.new_stimulation(sti_id='d', sti_type='keyboard', trigger_key=pygame.K_d)
    world.new_stimulation(sti_id='arrow_u', sti_type='keyboard', trigger_key=pygame.K_UP)
    world.new_stimulation(sti_id='arrow_d', sti_type='keyboard', trigger_key=pygame.K_DOWN)
    world.new_stimulation(sti_id='arrow_l', sti_type='keyboard', trigger_key=pygame.K_LEFT)
    world.new_stimulation(sti_id='arrow_r', sti_type='keyboard', trigger_key=pygame.K_RIGHT)
    world.new_stimulation(sti_id='mouse', sti_type='mouse', trigger_key=1, mouse_r_type='w')

    world.sti_add_callback(sti_id='btn_cam_u', callback=cam_u)
    world.sti_add_callback(sti_id='btn_cam_d', callback=cam_d)
    world.sti_add_callback(sti_id='btn_cam_l', callback=cam_l)
    world.sti_add_callback(sti_id='btn_cam_r', callback=cam_r)
    world.sti_add_callback(sti_id='w', callback=cam_u)
    world.sti_add_callback(sti_id='s', callback=cam_d)
    world.sti_add_callback(sti_id='a', callback=cam_l)
    world.sti_add_callback(sti_id='d', callback=cam_r)
    world.sti_add_callback(sti_id='btn_jet_u', callback=jet_u)
    world.sti_add_callback(sti_id='btn_jet_d', callback=jet_d)
    world.sti_add_callback(sti_id='btn_jet_l', callback=jet_l)
    world.sti_add_callback(sti_id='btn_jet_r', callback=jet_r)
    world.sti_add_callback(sti_id='arrow_u', callback=jet_u)
    world.sti_add_callback(sti_id='arrow_d', callback=jet_d)
    world.sti_add_callback(sti_id='arrow_l', callback=jet_l)
    world.sti_add_callback(sti_id='arrow_r', callback=jet_r)
    world.sti_add_callback(sti_id='mouse', callback=jet_m)

    world.start()
    os.abort()
