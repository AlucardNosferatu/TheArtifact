import time
from math import sqrt

import pygame

from Mechanism.Agent import Agent, Nature, Player
from Mechanism.Event import Event


def cam_u(params, recent_input):
    _ = recent_input
    world = params['world']
    world.get_camera().move(d_y=-16)
    return None, None


def cam_d(params, recent_input):
    _ = recent_input
    world = params['world']
    world.get_camera().move(d_y=16)
    return None, None


def cam_l(params, recent_input):
    _ = recent_input
    world = params['world']
    world.get_camera().move(d_x=-16)
    return None, None


def cam_r(params, recent_input):
    _ = recent_input
    world = params['world']
    world.get_camera().move(d_x=16)
    return None, None


def jet_u(params, recent_input):
    _ = recent_input
    player = params['agents']['player']
    jet = player.obtain_ent_inst(type_name='jet', i=player.ent_inst['jet'][0])
    if jet is not None:
        jet.move(d_y=-16)
    return None, None


def jet_d(params, recent_input):
    _ = recent_input
    player = params['agents']['player']
    jet = player.obtain_ent_inst(type_name='jet', i=player.ent_inst['jet'][0])
    if jet is not None:
        jet.move(d_y=16)
    return None, None


def jet_l(params, recent_input):
    _ = recent_input
    player = params['agents']['player']
    jet = player.obtain_ent_inst(type_name='jet', i=player.ent_inst['jet'][0])
    if jet is not None:
        jet.move(d_x=-16)
    return None, None


def jet_r(params, recent_input):
    _ = recent_input
    player = params['agents']['player']
    jet = player.obtain_ent_inst(type_name='jet', i=player.ent_inst['jet'][0])
    if jet is not None:
        jet.move(d_x=16)
    return None, None


def jet_m(params, recent_input):
    _ = recent_input
    world = params['world']
    m_w_x, m_w_y = world.get_camera().mouse_world_pos()
    player = params['agents']['player']
    jet = player.obtain_ent_inst(type_name='jet', i=player.ent_inst['jet'][0])
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


def jet_f(params, recent_input):
    _ = recent_input
    world = params['world']
    player = params['agents']['player']
    type_name = 'bullet'
    jet = player.obtain_ent_inst(type_name='jet', i=player.ent_inst['jet'][0])
    i = player.create_ent_inst(type_name=type_name, world_x=jet.world_x, world_y=jet.world_y - 64)
    event = Event(radius=32, trigger_ent_type=['target'], trigger_function=reach_target, world=player.world)
    player.bind_ent_events(type_name=type_name, i=i, events=[event])
    world.core.append_routine(func=bullet_f, r_type='w')
    return None, None


def bullet_f(params, recent_input):
    _ = recent_input
    player = params['agents']['player']
    type_name = 'bullet'
    for i in player.ent_inst[type_name]:
        bullet = player.obtain_ent_inst(type_name=type_name, i=i)
        bullet.move(d_y=-8)
        if not hasattr(bullet, 'ttl'):
            bullet.__setattr__('ttl', 64)
        bullet.ttl -= 1
        if bullet.ttl < 0:
            player.remove_ent_inst(type_name=type_name, i=i)
    return None, None


def reach_target(trigger_ent, triggered_ent, world):
    _, _ = trigger_ent, world
    nature: Agent = trigger_ent.belong_agent
    player: Agent = triggered_ent.belong_agent
    ent_id_dict = Agent.dec_ent_id(ent_id=trigger_ent.ent_id)
    nature.remove_ent_inst(type_name=ent_id_dict['type_name'], i=ent_id_dict['i'])
    ent_id_dict = Agent.dec_ent_id(ent_id=triggered_ent.ent_id)
    player.remove_ent_inst(type_name=ent_id_dict['type_name'], i=ent_id_dict['i'])


def world_changing(world):
    nature = init_nature(world)

    player = init_player(world)

    player.create_ent_inst(type_name='jet', world_x=960, world_y=540)
    nature.create_ent_inst(type_name='target', world_x=560, world_y=540)
    nature.create_ent_inst(type_name='target', world_x=1360, world_y=540)
    nature.create_ent_inst(type_name='target', world_x=960, world_y=940)
    nature.create_ent_inst(type_name='target', world_x=960, world_y=140)

    agent_routines(world)


def init_nature(world):
    nature = Nature(world=world)
    nature.update_ent_type(render_order=1, image_path='Assets/target.png', type_name='target')
    return nature


def init_player(world):
    def fps_int():
        return int(world.core.clock.get_fps())

    player = Player(world=world)
    player.update_ent_type(render_order=1, image_path='Assets/F-5E.png', type_name='jet')
    player.update_ent_type(render_order=1, image_path='Assets/bullet.png', type_name='bullet')
    player.add_sti(sti_id='btn_cam_u', sti_type='button', image_path='Assets/btn.png', x=640, y=8, callback=cam_u)
    player.add_sti(sti_id='btn_cam_d', sti_type='button', image_path='Assets/btn.png', x=640, y=712, callback=cam_d)
    player.add_sti(sti_id='btn_cam_l', sti_type='button', image_path='Assets/btn.png', x=8, y=360, callback=cam_l)
    player.add_sti(sti_id='btn_cam_r', sti_type='button', image_path='Assets/btn.png', x=1272, y=360, callback=cam_r)
    player.add_sti(sti_id='btn_jet_u', sti_type='button', image_path='Assets/btn.png', x=1212, y=612, callback=jet_u)
    player.add_sti(sti_id='btn_jet_d', sti_type='button', image_path='Assets/btn.png', x=1212, y=692, callback=jet_d)
    player.add_sti(sti_id='btn_jet_l', sti_type='button', image_path='Assets/btn.png', x=1172, y=652, callback=jet_l)
    player.add_sti(sti_id='btn_jet_r', sti_type='button', image_path='Assets/btn.png', x=1252, y=652, callback=jet_r)
    player.add_sti(sti_id='w', sti_type='keyboard', trigger_key=pygame.K_w, callback=cam_u)
    player.add_sti(sti_id='s', sti_type='keyboard', trigger_key=pygame.K_s, callback=cam_d)
    player.add_sti(sti_id='a', sti_type='keyboard', trigger_key=pygame.K_a, callback=cam_l)
    player.add_sti(sti_id='d', sti_type='keyboard', trigger_key=pygame.K_d, callback=cam_r)
    player.add_sti(sti_id='arrow_u', sti_type='keyboard', trigger_key=pygame.K_UP, callback=jet_u)
    player.add_sti(sti_id='arrow_d', sti_type='keyboard', trigger_key=pygame.K_DOWN, callback=jet_d)
    player.add_sti(sti_id='arrow_l', sti_type='keyboard', trigger_key=pygame.K_LEFT, callback=jet_l)
    player.add_sti(sti_id='arrow_r', sti_type='keyboard', trigger_key=pygame.K_RIGHT, callback=jet_r)
    player.add_sti(sti_id='space', sti_type='keyboard', trigger_key=pygame.K_SPACE, callback=jet_f)
    player.add_sti(sti_id='mouse', sti_type='mouse', trigger_key=1, mouse_r_type='w', callback=jet_m)
    player.add_sti(sti_id='fps', sti_type='text', text=fps_int, x=32, y=32)
    return player


def agent_routines(world):
    while True:
        for key in world.core.params['agents'].keys():
            agent = world.core.params['agents'][key]
            agent.routine_check_events()
            time.sleep(0.01)
