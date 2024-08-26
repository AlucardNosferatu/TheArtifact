import random
from math import sin, cos

import pygame

from Mechanism.Event import Event


def vbar_u(params, recent_input):
    _ = recent_input
    player = params['agents']['player']
    delta_t_s = params['delta']
    type_name = 'vbar'
    for i in player.ent_inst[type_name]:
        jet = player.obtain_ent_inst(type_name=type_name, i=i)
        jet_spd = params['game_vars']['vbar_spd']
        if jet is not None:
            displacement = round(jet_spd * delta_t_s * 100)
            jet.move(d_y=-displacement)
    return None, None


def vbar_d(params, recent_input):
    _ = recent_input
    player = params['agents']['player']
    delta_t_s = params['delta']
    type_name = 'vbar'
    for i in player.ent_inst[type_name]:
        jet = player.obtain_ent_inst(type_name=type_name, i=i)
        jet_spd = params['game_vars']['vbar_spd']
        if jet is not None:
            displacement = round(jet_spd * delta_t_s * 100)
            jet.move(d_y=displacement)
    return None, None


def vbar_f(params, recent_input):
    _ = recent_input
    world = params['world']
    player = params['agents']['player']
    type_name = 'ball'
    jet = player.obtain_ent_inst(type_name='vbar', i=player.ent_inst['vbar'][0])
    if len(player.ent_inst[type_name]) <= 0:
        i = player.create_ent_inst(type_name=type_name, world_x=jet.world_x + 64, world_y=jet.world_y)
        event = Event(radius=16, trigger_ent_type=['vbar'], trigger_function=reach_vbar, world=player.world)
        event.status = 'persist'
        player.bind_ent_events(type_name=type_name, i=i, events=[event])
        angle = random.choice([random.randint(-90, -10), random.randint(10, 90)]) / 180
        params['ball_spd_vector'] = [5 * cos(angle), 5 * sin(angle)]
        params['score'] = 0
        world.core.append_routine(func=ball_m, r_type='w')
    return None, None


def ball_m(params, recent_input):
    _ = recent_input
    player = params['agents']['player']
    delta_t_s = params['delta']
    type_name = 'ball'
    for i in player.ent_inst[type_name]:
        bullet_spd = params['game_vars']['ball_spd']
        bullet = player.obtain_ent_inst(type_name=type_name, i=i)
        displacement = round(bullet_spd * delta_t_s * 100)
        destroyed = False
        if bullet.world_x < 320:
            player.remove_ent_inst(type_name=type_name, i=i)
            destroyed = True
        elif bullet.world_x > 1600:
            params['ball_spd_vector'][0] = -params['ball_spd_vector'][0]
            params['score'] += 1
        elif bullet.world_y <= 188 or bullet.world_y >= 892:
            params['ball_spd_vector'][1] = -params['ball_spd_vector'][1]
        if not destroyed:
            f_x, f_y = params['ball_spd_vector'][0], params['ball_spd_vector'][1]
            bullet.move_vector(f_x=f_x, f_y=f_y, displacement=displacement)
    return None, None


def spawn_vbar(game):
    player = game.agents['player']
    player.create_ent_inst(type_name='vbar', world_x=352, world_y=540)
    player.create_ent_inst(type_name='vbar', world_x=352, world_y=556)
    player.create_ent_inst(type_name='vbar', world_x=352, world_y=524)
    player.create_ent_inst(type_name='vbar', world_x=352, world_y=572)
    player.create_ent_inst(type_name='vbar', world_x=352, world_y=508)
    player.create_ent_inst(type_name='vbar', world_x=352, world_y=588)
    player.create_ent_inst(type_name='vbar', world_x=352, world_y=492)
    player.world_modules.remove(spawn_vbar)


def reach_vbar(trigger_ent, triggered_ent, world):
    _ = trigger_ent
    params = world.core.params
    params['ball_spd_vector'][0] = -params['ball_spd_vector'][0]
    delta_t_s = params['delta']
    bullet_spd = params['game_vars']['ball_spd']
    displacement = round(bullet_spd * delta_t_s * 100)
    f_x, f_y = params['ball_spd_vector'][0], params['ball_spd_vector'][1]
    triggered_ent.move_vector(f_x=f_x, f_y=f_y, displacement=displacement)


def score(sprite):
    if 'score' not in sprite.core.params.keys():
        sprite.core.params['score'] = 0
    return int(sprite.core.params['score'])


game_vars = {
    'vbar_spd': 4,
    'ball_spd': 2
}
spr_key_path_pairs = [
    ['#vbar', 'Assets/vbar.png'],
    ['#black', 'Assets/black.png'],
    ['#ball', 'Assets/bullet.png']
]
routines = {
    'vbar_u': vbar_u, 'vbar_d': vbar_d,
    'vbar_f': vbar_f, 'ball_m': ball_m,
}
player_params = {
    'ent_types': [
        {'render_order': 1, 'image_path': '#vbar', 'type_name': 'vbar'},
        {'render_order': 1, 'image_path': '#ball', 'type_name': 'ball'}
    ],
    'extra_routines': [spawn_vbar],
    'sti': [
        {'sti_id': 'w', 'sti_type': 'keyboard', 'trigger_key': pygame.K_w, 'callback': 'vbar_u'},
        {'sti_id': 's', 'sti_type': 'keyboard', 'trigger_key': pygame.K_s, 'callback': 'vbar_d'},
        {'sti_id': 'arrow_u', 'sti_type': 'keyboard', 'trigger_key': pygame.K_UP, 'callback': 'vbar_u'},
        {'sti_id': 'arrow_d', 'sti_type': 'keyboard', 'trigger_key': pygame.K_DOWN, 'callback': 'vbar_d'},
        {'sti_id': 'space', 'sti_type': 'keyboard', 'trigger_key': pygame.K_SPACE, 'callback': 'vbar_f'},
        {'sti_id': 'score', 'sti_type': 'text', 'text': score, 'x': 32, 'y': 32}
    ]
}
nature_params = {
    'ent_types': [
        {'render_order': 1, 'image_path': '#target', 'type_name': 'target'},
    ],
    'extra_routines': []
}
agents_params = {
    'player': player_params,
    'nature': nature_params
}
