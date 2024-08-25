import time
from math import sqrt

import pygame

from Mechanism.Agent import Agent, Nature, Player
from Mechanism.Entity import Entity
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
        spd = 16
        err = 2 * spd
        fly_toward(tracker=jet, dest_x=m_w_x, dest_y=m_w_y, spd=spd, err=err)
    return None, None


def fly_toward(tracker, dest_x, dest_y, spd, err):
    d_w_x = dest_x - tracker.world_x
    d_w_y = dest_y - tracker.world_y
    dist = sqrt((d_w_x ** 2) + (d_w_y ** 2))
    if dist > err:
        s_w_x = round(spd * d_w_x / dist)
        s_w_y = round(spd * d_w_y / dist)
        tracker.move(d_x=s_w_x, d_y=s_w_y)


def jet_f_b(params, recent_input):
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


def jet_f_m(params, recent_input):
    _ = recent_input
    world = params['world']
    player = params['agents']['player']
    type_name = 'missile'
    jet = player.obtain_ent_inst(type_name='jet', i=player.ent_inst['jet'][0])
    i = player.create_ent_inst(type_name=type_name, world_x=jet.world_x, world_y=jet.world_y - 64)
    event = Event(radius=32, trigger_ent_type=['target'], trigger_function=reach_target, world=player.world)
    player.bind_ent_events(type_name=type_name, i=i, events=[event])
    world.core.append_routine(func=missile_f, r_type='w')
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


def missile_t(missile, nature):
    type_name = 'target'
    target_t = None
    dist_min = 999999
    for i in nature.ent_inst[type_name]:
        target = nature.obtain_ent_inst(type_name=type_name, i=i)
        dist = Entity.distance_between(ent1=target, ent2=missile)
        if dist < dist_min:
            dist_min = dist
            target_t = target
    if target_t is None:
        missile.move(d_y=-8)
    else:
        fly_toward(tracker=missile, dest_x=target_t.world_x, dest_y=target_t.world_y, spd=8, err=16)


def missile_f(params, recent_input):
    _ = recent_input
    player = params['agents']['player']
    nature = params['agents']['nature']
    type_name = 'missile'
    for i in player.ent_inst[type_name]:
        missile = player.obtain_ent_inst(type_name=type_name, i=i)
        missile_t(missile=missile, nature=nature)
        if not hasattr(missile, 'ttl'):
            missile.__setattr__('ttl', 64)
        missile.ttl -= 1
        if missile.ttl < 0:
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


def spawn_targets(world, trc, trc_max):
    nature = world.core.params['agents']['nature']
    xy_pairs = [[560, 540], [1360, 540], [960, 940], [960, 140]]
    for i in range(len(xy_pairs)):
        xy_pair = xy_pairs[i]
        x = xy_pair[0]
        y = xy_pair[1]
        destroyed = True
        ent_list = list(world.entities.values()).copy()
        for ent in ent_list:
            if ent.world_x == x and ent.world_y == y:
                destroyed = False
                break
        if destroyed:
            trc[i] -= 1
        else:
            trc[i] = trc_max
        if trc[i] < 0:
            trc[i] = trc_max
            nature.create_ent_inst(type_name='target', world_x=x, world_y=y)


def init_nature(world):
    nature = Nature(world=world)
    nature.update_ent_type(render_order=1, image_path='#target', type_name='target')
    return nature


def init_player(world):
    def fps_int():
        return int(world.core.clock.get_fps())

    player = Player(world=world)
    player.update_ent_type(render_order=1, image_path='#jet', type_name='jet')
    player.update_ent_type(render_order=1, image_path='#bullet', type_name='bullet')
    player.update_ent_type(render_order=1, image_path='#missile', type_name='missile')
    player.add_sti(sti_id='btn_cam_u', sti_type='button', image_path='#button', x=640, y=8, callback=cam_u)
    player.add_sti(sti_id='btn_cam_d', sti_type='button', image_path='#button', x=640, y=712, callback=cam_d)
    player.add_sti(sti_id='btn_cam_l', sti_type='button', image_path='#button', x=8, y=360, callback=cam_l)
    player.add_sti(sti_id='btn_cam_r', sti_type='button', image_path='#button', x=1272, y=360, callback=cam_r)
    player.add_sti(sti_id='btn_jet_u', sti_type='button', image_path='#button', x=1212, y=612, callback=jet_u)
    player.add_sti(sti_id='btn_jet_d', sti_type='button', image_path='#button', x=1212, y=692, callback=jet_d)
    player.add_sti(sti_id='btn_jet_l', sti_type='button', image_path='#button', x=1172, y=652, callback=jet_l)
    player.add_sti(sti_id='btn_jet_r', sti_type='button', image_path='#button', x=1252, y=652, callback=jet_r)
    player.add_sti(sti_id='w', sti_type='keyboard', trigger_key=pygame.K_w, callback=cam_u)
    player.add_sti(sti_id='s', sti_type='keyboard', trigger_key=pygame.K_s, callback=cam_d)
    player.add_sti(sti_id='a', sti_type='keyboard', trigger_key=pygame.K_a, callback=cam_l)
    player.add_sti(sti_id='d', sti_type='keyboard', trigger_key=pygame.K_d, callback=cam_r)
    player.add_sti(sti_id='arrow_u', sti_type='keyboard', trigger_key=pygame.K_UP, callback=jet_u)
    player.add_sti(sti_id='arrow_d', sti_type='keyboard', trigger_key=pygame.K_DOWN, callback=jet_d)
    player.add_sti(sti_id='arrow_l', sti_type='keyboard', trigger_key=pygame.K_LEFT, callback=jet_l)
    player.add_sti(sti_id='arrow_r', sti_type='keyboard', trigger_key=pygame.K_RIGHT, callback=jet_r)
    player.add_sti(sti_id='space', sti_type='keyboard', trigger_key=pygame.K_SPACE, callback=jet_f_b)
    player.add_sti(sti_id='c', sti_type='keyboard', trigger_key=pygame.K_c, callback=jet_f_m)
    player.add_sti(sti_id='mouse', sti_type='mouse', trigger_key=1, mouse_r_type='w', callback=jet_m)
    player.add_sti(sti_id='fps', sti_type='text', text=fps_int, x=32, y=32)
    return player


def agent_routines(world):
    trc_max = 64
    target_respawn_counter = [trc_max, trc_max, trc_max, trc_max]
    while True:
        for key in world.core.params['agents'].keys():
            agent = world.core.params['agents'][key]
            agent.routine_check_events()
        spawn_targets(world=world, trc=target_respawn_counter, trc_max=trc_max)
        time.sleep(0.01)
