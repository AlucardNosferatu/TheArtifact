import pygame

from Mechanism.Agent import Agent
from Mechanism.Entity import Entity
from Mechanism.Event import Event
from Mechanism.Utils import fly_toward

game_vars = {
    'jet_spd': 4,
    'bullet_spd': 2,
    'bullet_ttl': 64,
    'missile_spd': 2,
    'missile_ttl': 128
}

spr_key_path_pairs = [
    ['#city', 'Assets/city.png'],
    ['#button', 'Assets/btn.png'],
    ['#jet', 'Assets/F-5E.png'],
    ['#bullet', 'Assets/bullet.png'],
    ['#missile', 'Assets/missile.png'],
    ['#target', 'Assets/target.png']
]


def cam_u(params, recent_input):
    _ = recent_input
    world = params['world']
    delta_t_s = params['delta']
    camera = world.get_camera()
    displacement = round(camera.moving_speed * delta_t_s * 100)
    camera.move(d_y=-displacement)
    return None, None


def cam_d(params, recent_input):
    _ = recent_input
    world = params['world']
    delta_t_s = params['delta']
    camera = world.get_camera()
    displacement = round(camera.moving_speed * delta_t_s * 100)
    camera.move(d_y=displacement)
    return None, None


def cam_l(params, recent_input):
    _ = recent_input
    world = params['world']
    delta_t_s = params['delta']
    camera = world.get_camera()
    displacement = round(camera.moving_speed * delta_t_s * 100)
    camera.move(d_x=-displacement)
    return None, None


def cam_r(params, recent_input):
    _ = recent_input
    world = params['world']
    delta_t_s = params['delta']
    camera = world.get_camera()
    displacement = round(camera.moving_speed * delta_t_s * 100)
    camera.move(d_x=displacement)
    return None, None


def jet_u(params, recent_input):
    _ = recent_input
    player = params['agents']['player']
    delta_t_s = params['delta']
    jet = player.obtain_ent_inst(type_name='jet', i=player.ent_inst['jet'][0])
    jet_spd = params['game_vars']['jet_spd']
    if jet is not None:
        displacement = round(jet_spd * delta_t_s * 100)
        jet.move(d_y=-displacement)
    return None, None


def jet_d(params, recent_input):
    _ = recent_input
    player = params['agents']['player']
    delta_t_s = params['delta']
    jet = player.obtain_ent_inst(type_name='jet', i=player.ent_inst['jet'][0])
    if jet is not None:
        jet_spd = params['game_vars']['jet_spd']
        displacement = round(jet_spd * delta_t_s * 100)
        jet.move(d_y=displacement)
    return None, None


def jet_l(params, recent_input):
    _ = recent_input
    player = params['agents']['player']
    delta_t_s = params['delta']
    jet = player.obtain_ent_inst(type_name='jet', i=player.ent_inst['jet'][0])
    if jet is not None:
        jet_spd = params['game_vars']['jet_spd']
        displacement = round(jet_spd * delta_t_s * 100)
        jet.move(d_x=-displacement)
    return None, None


def jet_r(params, recent_input):
    _ = recent_input
    player = params['agents']['player']
    delta_t_s = params['delta']
    jet = player.obtain_ent_inst(type_name='jet', i=player.ent_inst['jet'][0])
    if jet is not None:
        jet_spd = params['game_vars']['jet_spd']
        displacement = round(jet_spd * delta_t_s * 100)
        jet.move(d_x=displacement)
    return None, None


def jet_m(params, recent_input):
    _ = recent_input
    world = params['world']
    player = params['agents']['player']
    delta_t_s = params['delta']
    m_w_x, m_w_y = world.get_camera().mouse_world_pos()
    jet = player.obtain_ent_inst(type_name='jet', i=player.ent_inst['jet'][0])
    if jet is not None:
        jet_spd = params['game_vars']['jet_spd']
        err = 2 * jet_spd
        displacement = round(jet_spd * delta_t_s * 100)
        fly_toward(tracker=jet, dest_x=m_w_x, dest_y=m_w_y, displacement=displacement, err=err)
    return None, None


def jet_f_b(params, recent_input):
    _ = recent_input
    world = params['world']
    player = params['agents']['player']
    type_name = 'bullet'
    jet = player.obtain_ent_inst(type_name='jet', i=player.ent_inst['jet'][0])
    i = player.create_ent_inst(type_name=type_name, world_x=jet.world_x, world_y=jet.world_y - 64)
    event = Event(radius=32, trigger_ent_type=['target', 'missile'], trigger_function=reach_target, world=player.world)
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
    delta_t_s = params['delta']
    type_name = 'bullet'
    for i in player.ent_inst[type_name]:
        bullet_spd = params['game_vars']['bullet_spd']
        bullet_ttl = params['game_vars']['bullet_ttl']
        bullet = player.obtain_ent_inst(type_name=type_name, i=i)
        displacement = round(bullet_spd * delta_t_s * 100)
        bullet.move(d_y=-displacement)
        if not hasattr(bullet, 'ttl'):
            bullet.__setattr__('ttl', bullet_ttl)
        bullet.ttl -= 1
        if bullet.ttl < 0:
            player.remove_ent_inst(type_name=type_name, i=i)
    return None, None


def missile_f(params, recent_input):
    _ = recent_input
    player = params['agents']['player']
    nature = params['agents']['nature']
    delta_t_s = params['delta']
    type_name = 'missile'
    for i in player.ent_inst[type_name]:
        missile = player.obtain_ent_inst(type_name=type_name, i=i)
        missile_spd = params['game_vars']['missile_spd']
        missile_ttl = params['game_vars']['missile_ttl']
        missile_t(missile=missile, nature=nature, delta_t_s=delta_t_s, missile_spd=missile_spd)
        if not hasattr(missile, 'ttl'):
            missile.__setattr__('ttl', missile_ttl)
        missile.ttl -= 1
        if missile.ttl < 0:
            player.remove_ent_inst(type_name=type_name, i=i)
    return None, None


def missile_t(missile, nature, delta_t_s, missile_spd):
    type_name = 'target'
    target_t = None
    dist_min = 999999
    for i in nature.ent_inst[type_name]:
        target = nature.obtain_ent_inst(type_name=type_name, i=i)
        dist = Entity.distance_between(ent1=target, ent2=missile)
        if dist < dist_min:
            dist_min = dist
            target_t = target
    displacement = round(missile_spd * delta_t_s * 100)
    if target_t is None:
        missile.move(d_y=-displacement)
    else:
        err = 2 * missile_spd
        fly_toward(
            tracker=missile, dest_x=target_t.world_x, dest_y=target_t.world_y, displacement=displacement, err=err
        )


def spawn_targets(game):
    nature = game.agents['nature']
    if 'target_respawn_counter_max' not in game.vars.keys():
        game.vars['target_respawn_counter_max'] = 64
    if 'target_respawn_counter' not in game.vars.keys():
        game.vars['target_respawn_counter'] = [
            game.vars['target_respawn_counter_max'], game.vars['target_respawn_counter_max'],
            game.vars['target_respawn_counter_max'], game.vars['target_respawn_counter_max']
        ]
    xy_pairs = [[560, 540], [1360, 540], [960, 940], [960, 140]]
    for i in range(len(xy_pairs)):
        xy_pair = xy_pairs[i]
        x = xy_pair[0]
        y = xy_pair[1]
        destroyed = True
        ent_list = list(game.world.entities.values()).copy()
        for ent in ent_list:
            if ent.world_x == x and ent.world_y == y:
                destroyed = False
                break
        if destroyed:
            game.vars['target_respawn_counter'][i] -= 1
        else:
            game.vars['target_respawn_counter'][i] = game.vars['target_respawn_counter_max']
        if game.vars['target_respawn_counter'][i] < 0:
            game.vars['target_respawn_counter'][i] = game.vars['target_respawn_counter_max']
            nature.create_ent_inst(type_name='target', world_x=x, world_y=y)


def spawn_jet(game):
    player = game.agents['player']
    player.create_ent_inst(type_name='jet', world_x=960, world_y=540)
    player.world_modules.remove(spawn_jet)


def reach_target(trigger_ent, triggered_ent, world):
    _, _ = trigger_ent, world
    nature = trigger_ent.belong_agent
    player = triggered_ent.belong_agent
    ent_id_dict = Agent.dec_ent_id(ent_id=trigger_ent.ent_id)
    nature.remove_ent_inst(type_name=ent_id_dict['type_name'], i=ent_id_dict['i'])
    ent_id_dict = Agent.dec_ent_id(ent_id=triggered_ent.ent_id)
    player.remove_ent_inst(type_name=ent_id_dict['type_name'], i=ent_id_dict['i'])


def fps_int(sprite):
    return int(sprite.core.clock.get_fps())


routines = {
    'cam_u': cam_u, 'cam_d': cam_d, 'cam_l': cam_l, 'cam_r': cam_r,
    'jet_u': jet_u, 'jet_d': jet_d, 'jet_l': jet_l, 'jet_r': jet_r, 'jet_m': jet_m,
    'jet_f_b': jet_f_b, 'jet_f_m': jet_f_m, 'bullet_f': bullet_f, 'missile_f': missile_f,
}

player_params = {
    'ent_types': [
        {'render_order': 1, 'image_path': '#jet', 'type_name': 'jet'},
        {'render_order': 1, 'image_path': '#bullet', 'type_name': 'bullet'},
        {'render_order': 1, 'image_path': '#missile', 'type_name': 'missile'},
    ],
    'extra_routines': [spawn_jet],
    'sti': [
        {'sti_id': 'btn_cam_u', 'sti_type': 'button', 'image_path': '#button', 'x': 640, 'y': 8, 'callback': 'cam_u'},
        {'sti_id': 'btn_cam_d', 'sti_type': 'button', 'image_path': '#button', 'x': 640, 'y': 712, 'callback': 'cam_d'},
        {'sti_id': 'btn_cam_l', 'sti_type': 'button', 'image_path': '#button', 'x': 8, 'y': 360, 'callback': 'cam_l'},
        {
            'sti_id': 'btn_cam_r', 'sti_type': 'button', 'image_path': '#button', 'x': 1272, 'y': 360,
            'callback': 'cam_r'
        },
        {
            'sti_id': 'btn_jet_u', 'sti_type': 'button', 'image_path': '#button', 'x': 1212, 'y': 612,
            'callback': 'jet_u'
        },
        {
            'sti_id': 'btn_jet_d', 'sti_type': 'button', 'image_path': '#button', 'x': 1212, 'y': 692,
            'callback': 'jet_d'
        },
        {
            'sti_id': 'btn_jet_l', 'sti_type': 'button', 'image_path': '#button', 'x': 1172, 'y': 652,
            'callback': 'jet_l'
        },
        {
            'sti_id': 'btn_jet_r', 'sti_type': 'button', 'image_path': '#button', 'x': 1252, 'y': 652,
            'callback': 'jet_r'
        },
        {'sti_id': 'w', 'sti_type': 'keyboard', 'trigger_key': pygame.K_w, 'callback': 'cam_u'},
        {'sti_id': 's', 'sti_type': 'keyboard', 'trigger_key': pygame.K_s, 'callback': 'cam_d'},
        {'sti_id': 'a', 'sti_type': 'keyboard', 'trigger_key': pygame.K_a, 'callback': 'cam_l'},
        {'sti_id': 'd', 'sti_type': 'keyboard', 'trigger_key': pygame.K_d, 'callback': 'cam_r'},
        {'sti_id': 'arrow_u', 'sti_type': 'keyboard', 'trigger_key': pygame.K_UP, 'callback': 'jet_u'},
        {'sti_id': 'arrow_d', 'sti_type': 'keyboard', 'trigger_key': pygame.K_DOWN, 'callback': 'jet_d'},
        {'sti_id': 'arrow_l', 'sti_type': 'keyboard', 'trigger_key': pygame.K_LEFT, 'callback': 'jet_l'},
        {'sti_id': 'arrow_r', 'sti_type': 'keyboard', 'trigger_key': pygame.K_RIGHT, 'callback': 'jet_r'},
        {'sti_id': 'space', 'sti_type': 'keyboard', 'trigger_key': pygame.K_SPACE, 'callback': 'jet_f_b'},
        {'sti_id': 'c', 'sti_type': 'keyboard', 'trigger_key': pygame.K_c, 'callback': 'jet_f_m'},
        {'sti_id': 'mouse', 'sti_type': 'mouse', 'trigger_key': 1, 'mouse_r_type': 'w', 'callback': 'jet_m'},
        {'sti_id': 'fps', 'sti_type': 'text', 'text': fps_int, 'x': 32, 'y': 32}
    ]
}
nature_params = {
    'ent_types': [
        {'render_order': 1, 'image_path': '#target', 'type_name': 'target'},
    ],
    'extra_routines': [spawn_targets]
}
agents_params = {
    'player': player_params,
    'nature': nature_params
}
