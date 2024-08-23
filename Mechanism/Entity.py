from math import sqrt

from Engine.UI import Camera, EntitySprite, Button, KeyboardButton, Mouse


class Entity:
    sprite = None
    ent_id = None
    world_x = None
    world_y = None

    def __init__(self, core, ent_id, camera=None):
        self.events = []
        self.core = core
        self.ent_id = ent_id
        if camera is None:
            camera = Camera(screen=self.core.renderer.screen)
        self.camera = camera

    def set_sprite(self, image_path, world_x, world_y):
        self.world_x = world_x
        self.world_y = world_y
        self.sprite = EntitySprite(
            name=self.ent_id, image_path=image_path, cam=self.camera, world_x=self.world_x, world_y=self.world_y,
            core=self.core
        )

    def move(self, d_x=0, d_y=0):
        self.world_x += d_x
        self.world_y += d_y
        if self.sprite is not None:
            self.sprite.move(d_x=d_x, d_y=d_y)

    def relocate(self, world_x=None, world_y=None):
        if world_x is not None:
            self.world_x = world_x
        if world_y is not None:
            self.world_y = world_y
        if self.sprite is not None:
            self.sprite.relocate(world_x=self.world_x, world_y=self.world_y)

    def set_event(self, events, merge=False):
        if merge:
            for ev in events:
                if ev not in self.events:
                    self.events.append(ev)
        else:
            self.events = events

    def del_event(self, events, purge=False):
        if purge:
            self.events.clear()
        else:
            for ev in events:
                while ev in self.events:
                    self.events.remove(ev)

    @staticmethod
    def distance_between(ent1, ent2):
        # ent1, ent2 could be camera as well
        x1, y1 = ent1.world_x, ent1.world_y
        x2, y2 = ent2.world_x, ent2.world_y
        dist = sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))
        return dist


class World(Entity):
    def __init__(self, core, map_image, cam_x=None, cam_y=None, scale_x=200.0, scale_y=200.0, world_id='0#world'):
        super().__init__(core=core, ent_id=world_id)
        self.core.params['world'] = self
        self.set_sprite(image_path=map_image, world_x=0, world_y=0, scale_x=scale_x, scale_y=scale_y)
        if cam_x is not None and cam_y is not None:
            self.camera.focus(world_x=cam_x, world_y=cam_y)
        else:
            self.camera.focus(world_x=self.sprite.world_x, world_y=self.sprite.world_y)
        self.entities: dict[str, Entity] = {}
        self.stimulation = {}

    def get_camera(self):
        return self.camera

    def set_sprite(self, image_path, scale_x=200.0, scale_y=200.0, world_x=-1, world_y=-1):
        super().set_sprite(image_path=image_path, world_x=0, world_y=0)
        world_x = round(self.sprite.surface.get_width() / 2)
        world_y = round(self.sprite.surface.get_height() / 2)
        self.relocate(world_x=world_x, world_y=world_y)
        self.sprite.check_visibility = False
        self.sprite.scale_x = scale_x
        self.sprite.scale_y = scale_y

    def new_entity(self, ent_id, image_path=None, world_x=None, world_y=None):
        self.entities[ent_id] = Entity(core=self.core, ent_id=ent_id, camera=self.camera)
        if image_path is not None and world_x is not None and world_y is not None:
            self.entities[ent_id].set_sprite(image_path=image_path, world_x=world_x, world_y=world_y)

    def get_entity(self, ent_id):
        if ent_id in self.entities.keys():
            return self.entities[ent_id]
        else:
            return None

    def del_entity(self, ent_id):
        if ent_id in self.entities.keys():
            del self.entities[ent_id]
            return True
        else:
            return False

    def new_stimulation(self, sti_id, sti_type, image_path=None, x=None, y=None, trigger_key=None, mouse_r_type='u'):
        if sti_type == 'button':
            self.stimulation[sti_id] = Button(name=sti_id, image_path=image_path, x=x, y=y, core=self.core)
        elif sti_type == 'keyboard':
            self.stimulation[sti_id] = KeyboardButton(name=sti_id, core=self.core, trigger_key=trigger_key)
        elif sti_type == 'mouse':
            self.stimulation[sti_id] = Mouse(name=sti_id, core=self.core, trigger_key=trigger_key, r_type=mouse_r_type)
        else:
            raise ValueError('unrecognized sti_type:{}'.format(sti_type))

    def get_stimulation(self, sti_id):
        if sti_id in self.stimulation.keys():
            return self.stimulation[sti_id]
        else:
            return None

    def del_stimulation(self, sti_id):
        if sti_id in self.stimulation.keys():
            self.sti_del_callback(sti_id=sti_id, r_type='both')
            del self.stimulation[sti_id]
            return True
        else:
            return False

    def sti_add_callback(self, sti_id, callback):
        self.stimulation[sti_id].reg_callback(callback=callback)

    def sti_del_callback(self, sti_id, r_type='u'):
        self.stimulation[sti_id].del_callback(r_type=r_type)

    def start(self):
        self.core.engine_run()
