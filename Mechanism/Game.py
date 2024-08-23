from math import sqrt

import pygame

from Mechanism.Entity import Entity


class Event:
    def __init__(self, att_ent, radius, trigger_ent_type: list, trigger_function, world, priority=1):
        self.att_ent = att_ent
        self.radius = radius
        self.trigger_ent_type: list = trigger_ent_type
        self.trigger_function = trigger_function
        self.world = world
        self.priority = priority
        self.status = 'idle'
        # ['idle', 'triggered']

    def is_triggered(self, trigger_ent, triggered_ent: None | Entity = None, distance=None):
        if triggered_ent is None:
            triggered_ent = self.att_ent
        if distance is None:
            distance = Entity.distance_between(ent1=triggered_ent, ent2=trigger_ent)
        if distance <= self.radius:
            ent_id = trigger_ent.ent_id
            ent_type_name = Agent.dec_ent_id(ent_id=ent_id)['type_name']
            if ent_type_name in self.trigger_ent_type:
                return True
        return False

    def triggered(self, trigger_ent, triggered_ent=None):
        if triggered_ent is None:
            triggered_ent = self.att_ent
        self.trigger_function(trigger_ent, triggered_ent, self.world)
        self.status = 'triggered'


class EntTemplate:
    def __init__(self, render_order, image_path, type_name):
        self.render_order = render_order
        self.image_path = image_path
        self.type_name = type_name


class Agent:
    ent_id_temp = '{}#{}_{}_{}'

    def __init__(self, world, agent_id):
        self.agent_id = agent_id
        self.world = world
        core = self.world.core
        if 'agents' not in core.params.keys():
            core.params['agents'] = {}
        core.params['agents'][agent_id] = self
        self.ent_db: dict[str, EntTemplate] = {}
        self.ent_inst: dict[str, list[int]] = {}

    def get_ent_id(self, type_name, i):
        ent_temp: EntTemplate = self.ent_db[type_name]
        ent_id = Agent.ent_id_temp.format(ent_temp.render_order, type_name, self.agent_id, i)
        return ent_id

    @staticmethod
    def dec_ent_id(ent_id):
        ent_id_dict = {
            'render_order': int(ent_id.split('#')[0]), 'type_name': ent_id.split('#')[1].split('_')[0],
            'agent_id': ent_id.split('#')[1].split('_')[1], 'i': int(ent_id.split('#')[1].split('_')[2])
        }
        return ent_id_dict

    def update_ent_type(self, render_order, image_path, type_name):
        self.ent_db[type_name] = EntTemplate(
            render_order=render_order, image_path=image_path, type_name=type_name
        )
        if type_name not in self.ent_inst.keys():
            self.ent_inst[type_name] = []

    def create_ent_inst(self, type_name, world_x, world_y):
        i = 0
        while i in self.ent_inst[type_name]:
            i += 1
        self.ent_inst[type_name].append(i)
        ent_id = self.get_ent_id(type_name=type_name, i=i)
        self.world.new_entity(
            ent_id=ent_id, image_path=self.ent_db[type_name].image_path, world_x=world_x, world_y=world_y
        )

    def remove_ent_inst(self, type_name, i):
        if i in self.ent_inst[type_name]:
            self.ent_inst[type_name].remove(i)
            ent_id = self.get_ent_id(type_name=type_name, i=i)
            self.bind_ent_events(type_name=type_name, i=i, events=None)
            self.world.del_entity(ent_id=ent_id)
            return True
        else:
            return False

    def obtain_ent_inst(self, type_name, i):
        ent_id = self.get_ent_id(type_name=type_name, i=i)
        ent = self.world.get_entity(ent_id=ent_id)
        return ent

    def bind_ent_events(self, type_name, i, events: None | list[Event] = None, op=None):
        if op is None:
            op = ['set', 'merge']
        if i in self.ent_inst[type_name]:
            ent = self.obtain_ent_inst(type_name=type_name, i=i)
            if op[0] == 'set':
                assert events is not None
                ent.set_event(events=events, merge=op[1] == 'merge')
            elif op[0] == 'del':
                ent.del_event(events=events, purge=op[1] == 'purge')
            else:
                raise ValueError('unrecognized op0:{}'.format(op[0]))

    # self.radius = radius
    # self.trigger_ent_type: list = trigger_ent_type
    # self.trigger_function = trigger_function
    # self.world = world
    # self.priority = priority
    # self.status = 'idle'
    def list_ent_events(
            self, type_name=None, trigger_ent_type=None, trigger_function=None, priority=None, status=None
    ):
        results: list[Event] = []
        for type_name_db in self.ent_db.keys():
            if type_name is not None and type_name == type_name_db:
                pass
            else:
                continue
            for i in self.ent_inst[type_name_db]:
                ent = self.obtain_ent_inst(type_name=type_name, i=i)
                for ev in ent.events:
                    if trigger_ent_type is not None and trigger_ent_type == ev.trigger_ent_type:
                        pass
                    else:
                        continue
                    if trigger_function is not None and trigger_function == ev.trigger_function:
                        pass
                    else:
                        continue
                    if priority is not None and priority == ev.priority:
                        pass
                    else:
                        continue
                    if status is not None and status == ev.status:
                        pass
                    else:
                        continue
                    results.append(ev)
        return results

    def routine_check_events(self):
        pending_remove = []
        for i in range(0, 9):
            events = self.list_ent_events(priority=i)
            for event in events:
                if event.status == 'triggered':
                    pending_remove.append(event)
                elif event.status == 'idle':
                    for ent_id in self.world.entities.keys():
                        trigger_ent = self.world.get_entity(ent_id=ent_id)
                        if event.is_triggered(trigger_ent=trigger_ent):
                            event.triggered(trigger_ent=trigger_ent)
                else:
                    raise NotImplementedError('unrecognized event.status:{}'.format(event.status))
        for event in pending_remove:
            ent = event.att_ent
            ent_id = ent.ent_id
            ent_id_dict = Agent.dec_ent_id(ent_id=ent_id)
            self.bind_ent_events(
                type_name=ent_id_dict['type_name'], i=ent_id_dict['i'], events=[event], op=['del', 'single']
            )


class Player(Agent):
    def __init__(self, world):
        super().__init__(world, 'player')

    def add_sti(
            self, sti_id, sti_type, image_path=None, x=None, y=None, trigger_key=None, mouse_r_type='u', callback=None
    ):
        self.world.new_stimulation(
            sti_id, sti_type, image_path=image_path, x=x, y=y, trigger_key=trigger_key, mouse_r_type=mouse_r_type
        )
        if callback is not None:
            self.add_callback(sti_id=sti_id, callback=callback)

    def add_callback(self, sti_id, callback):
        self.world.sti_add_callback(sti_id=sti_id, callback=callback)

    def del_callback(self, sti_id, r_type='u'):
        self.world.sti_del_callback(sti_id=sti_id, r_type=r_type)


class Nature(Agent):
    def __init__(self, world):
        super().__init__(world, 'nature')


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


def world_changing(world):
    player = Player(world=world)
    nature = Nature(world=world)
    player.update_ent_type(render_order=1, image_path='Assets/F-5E.png', type_name='jet')
    nature.update_ent_type(render_order=1, image_path='Assets/target.png', type_name='target')

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
    player.add_sti(sti_id='mouse', sti_type='mouse', trigger_key=1, mouse_r_type='w', callback=jet_m)

    player.create_ent_inst(type_name='jet', world_x=960, world_y=540)
