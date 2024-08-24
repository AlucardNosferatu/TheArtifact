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
        ent_id = self.get_ent_id(type_name=type_name, i=i)
        self.world.new_entity(
            ent_id=ent_id, image_path=self.ent_db[type_name].image_path, world_x=world_x, world_y=world_y,
            belong_agent=self
        )
        self.ent_inst[type_name].append(i)
        return i

    def remove_ent_inst(self, type_name, i):
        if i in self.ent_inst[type_name]:
            ent_id = self.get_ent_id(type_name=type_name, i=i)
            self.world.del_entity(ent_id=ent_id)
            self.ent_inst[type_name].remove(i)
            return True
        else:
            return False

    def obtain_ent_inst(self, type_name, i):
        ent_id = self.get_ent_id(type_name=type_name, i=i)
        ent = self.world.get_entity(ent_id=ent_id)
        return ent

    def bind_ent_events(self, type_name, i, events=None, op=None):
        if op is None:
            if events is None:
                op = ['del', 'purge']
            else:
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
        results = []
        for type_name_db in self.ent_db.keys():
            if type_name is None or type_name == type_name_db:
                pass
            else:
                continue
            for i in self.ent_inst[type_name_db]:
                ent = self.obtain_ent_inst(type_name=type_name_db, i=i)
                if ent is not None:
                    for ev in ent.events:
                        if trigger_ent_type is None or trigger_ent_type == ev.trigger_ent_type:
                            pass
                        else:
                            continue
                        if trigger_function is None or trigger_function == ev.trigger_function:
                            pass
                        else:
                            continue
                        if priority is None or priority == ev.priority:
                            pass
                        else:
                            continue
                        if status is None or status == ev.status:
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
                    ent_list = self.world.entities.copy()
                    for ent_id in ent_list.keys():
                        trigger_ent = self.world.get_entity(ent_id=ent_id)
                        if trigger_ent is not None:
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
