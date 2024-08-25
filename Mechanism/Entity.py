import threading
import uuid
from math import sqrt, ceil

from Engine.UI import Camera, EntitySprite, Button, KeyboardButton, Mouse, UIText


class Grid:
    def __init__(self, world, edge_length=8):
        self.lock = threading.Lock()
        self.world = world
        self.elen = edge_length
        self.center_x = self.world.world_x
        self.center_y = self.world.world_y
        # start from 0
        self.center_grid_index_x = ceil((self.center_x - round(self.elen / 2)) / self.elen)
        self.center_grid_index_y = ceil((self.center_y - round(self.elen / 2)) / self.elen)
        self.event_reg = {}
        self.grid2id = {}
        self.id2grid = {}

    def get_grid_by_point(self, world_x, world_y):
        def process_by_dim(world_ent, center, center_grid_index):
            d = world_ent - center
            if abs(d) < round(self.elen / 2):
                grid_index = center_grid_index
            else:
                if d > 0:
                    d -= round(self.elen / 2)
                    grid_index_d = ceil(abs(d) / self.elen)
                else:
                    d += round(self.elen / 2)
                    grid_index_d = -ceil(abs(d) / self.elen)
                grid_index = grid_index_d + center_grid_index
            return grid_index

        grid_index_x = process_by_dim(
            world_ent=world_x, center=self.center_x, center_grid_index=self.center_grid_index_x
        )
        grid_index_y = process_by_dim(
            world_ent=world_y, center=self.center_y, center_grid_index=self.center_grid_index_y
        )
        return grid_index_x, grid_index_y

    def get_grids_by_ent(self, ent, ent_box_edge_len=0, reg=True):
        x_l = ent.world_x - round(ent_box_edge_len / 2)
        x_r = ent.world_x + round(ent_box_edge_len / 2)
        y_t = ent.world_y - round(ent_box_edge_len / 2)
        y_b = ent.world_y + round(ent_box_edge_len / 2)
        gi_x_l, gi_y_t = self.get_grid_by_point(world_x=x_l, world_y=y_t)
        gi_x_r, gi_y_b = self.get_grid_by_point(world_x=x_r, world_y=y_b)
        if reg:
            self.reg_ent(ent=ent, gi_x_l=gi_x_l, gi_x_r=gi_x_r, gi_y_t=gi_y_t, gi_y_b=gi_y_b)
        return gi_x_l, gi_x_r, gi_y_b, gi_y_t

    def get_grids_by_event(self, event, reg=True):
        ent = event.att_ent
        event_diameter = event.radius * 2
        gi_x_l, gi_x_r, gi_y_b, gi_y_t = self.get_grids_by_ent(ent, ent_box_edge_len=event_diameter, reg=False)
        if reg:
            self.reg_event(event=event, gi_x_l=gi_x_l, gi_x_r=gi_x_r, gi_y_t=gi_y_t, gi_y_b=gi_y_b)
        return gi_x_l, gi_x_r, gi_y_t, gi_y_b

    def reg(self, reg_id, gi_x_l, gi_x_r, gi_y_b, gi_y_t):
        if reg_id not in self.id2grid.keys():
            self.id2grid[reg_id] = []
        self.clr(reg_id=reg_id, del_id=False)
        self.lock.acquire()
        self.id2grid[reg_id].append(gi_x_l)
        self.id2grid[reg_id].append(gi_x_r)
        self.id2grid[reg_id].append(gi_y_t)
        self.id2grid[reg_id].append(gi_y_b)
        for i in range(gi_x_l, gi_x_r + 1):
            if i not in self.grid2id.keys():
                self.grid2id[i] = {}
            for j in range(gi_y_t, gi_y_b + 1):
                if j not in self.grid2id[i].keys():
                    self.grid2id[i][j] = []
                if reg_id not in self.grid2id[i][j]:
                    self.grid2id[i][j].append(reg_id)
        self.lock.release()

    def clr(self, reg_id, del_id=True):
        assert reg_id in self.id2grid.keys()
        self.lock.acquire()
        if len(self.id2grid[reg_id]) > 0:
            gi_x_l_old = self.id2grid[reg_id][0]
            gi_x_r_old = self.id2grid[reg_id][1]
            gi_y_t_old = self.id2grid[reg_id][2]
            gi_y_b_old = self.id2grid[reg_id][3]
            for i in range(gi_x_l_old, gi_x_r_old + 1):
                if i not in self.grid2id.keys():
                    self.grid2id[i] = {}
                for j in range(gi_y_t_old, gi_y_b_old + 1):
                    if j not in self.grid2id[i].keys():
                        self.grid2id[i][j] = []
                    if reg_id in self.grid2id[i][j]:
                        self.grid2id[i][j].remove(reg_id)
            self.id2grid[reg_id].clear()
        if del_id:
            del self.id2grid[reg_id]
            if reg_id in self.event_reg.keys():
                del self.event_reg[reg_id]
        self.lock.release()

    def reg_ent(self, ent, gi_x_l, gi_x_r, gi_y_t, gi_y_b):
        self.reg(reg_id=ent.ent_id, gi_x_l=gi_x_l, gi_x_r=gi_x_r, gi_y_t=gi_y_t, gi_y_b=gi_y_b)

    def reg_event(self, event, gi_x_l, gi_x_r, gi_y_t, gi_y_b):
        if event not in self.event_reg.values():
            event_id = str(uuid.uuid4())
            self.event_reg[event_id] = event

        event_id = self.event2id(event)
        assert event_id is not None
        self.reg(reg_id=event_id, gi_x_l=gi_x_l, gi_x_r=gi_x_r, gi_y_t=gi_y_t, gi_y_b=gi_y_b)

    def event2id(self, event):
        event_id = None
        event_reg = self.event_reg.copy()
        for event_id in event_reg.keys():
            if self.event_reg[event_id] == event:
                break
        return event_id

    def ids_in_grid(self, gi_x, gi_y, filter_type=None):
        results = self.grid2id[gi_x][gi_y]
        event_reg = self.event_reg.copy()
        if filter_type is not None:
            if filter_type == 'event':
                results = [result for result in results if result not in event_reg.keys()]
            elif filter_type == 'entity':
                results = [result for result in results if result in event_reg.keys()]
            else:
                raise ValueError('unrecognized filter_type:{}'.format(filter_type))
        return results

    def ids_in_event(self, event, filter_type=None):
        results = []
        gi_x_l, gi_x_r, gi_y_t, gi_y_b = self.get_grids_by_event(event=event)
        for gi_x in range(gi_x_l, gi_x_r + 1):
            for gi_y in range(gi_y_t, gi_y_b + 1):
                results += self.ids_in_grid(gi_x=gi_x, gi_y=gi_y, filter_type=filter_type)
        return results


class Entity:
    sprite = None
    ent_id = None
    world_x = None
    world_y = None

    def __init__(self, core, ent_id, camera=None, grid=None):
        self.events = []
        self.core = core
        self.ent_id = ent_id
        if camera is None:
            camera = Camera(screen=self.core.renderer.screen)
        self.camera = camera
        self.belong_agent = None
        self.grid: Grid = grid

    def self_destruct(self):
        self.quit_grid_ent()
        if self.sprite is not None:
            self.core.append_routine(self.sprite.delete_routine, r_type='w', multi_inst=False)
        self.del_event(None, purge=True)

    def set_sprite(self, image_path, world_x, world_y):
        self.world_x = world_x
        self.world_y = world_y
        self.sprite = EntitySprite(
            name=self.ent_id, image_path=image_path, cam=self.camera, world_x=self.world_x, world_y=self.world_y,
            core=self.core
        )
        self.sync_grid()

    def move(self, d_x=0, d_y=0):
        self.world_x += d_x
        self.world_y += d_y
        if self.sprite is not None:
            self.sprite.move(d_x=d_x, d_y=d_y)
        self.sync_grid()

    def relocate(self, world_x=None, world_y=None):
        if world_x is not None:
            self.world_x = world_x
        if world_y is not None:
            self.world_y = world_y
        if self.sprite is not None:
            self.sprite.relocate(world_x=self.world_x, world_y=self.world_y)
        self.sync_grid()

    def sync_grid(self):
        if self.grid is not None:
            self.grid.get_grids_by_ent(ent=self)
            for event in self.events:
                self.grid.get_grids_by_event(event=event)

    def quit_grid_ent(self):
        if self.grid is not None:
            self.grid.clr(reg_id=self.ent_id)

    def quit_grid_event(self, events, purge=False):
        if self.grid is not None:
            if purge:
                events = self.events
            for event in events:
                event_id = self.grid.event2id(event=event)
                self.grid.clr(reg_id=event_id)

    def set_event(self, events, merge=False):
        if merge:
            for ev in events:
                if ev not in self.events:
                    ev.att_ent = self
                    self.events.append(ev)
        else:
            self.events = events
        self.sync_grid()

    def del_event(self, events, purge=False):
        self.quit_grid_event(events=events, purge=purge)
        if purge:
            self.events.clear()
        else:
            for ev in events:
                while ev in self.events:
                    ev.att_ent = None
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
        self.set_grid()

    def set_grid(self, grid: Grid = None, edge_length=None):
        if grid is None:
            if edge_length is None:
                edge_length = 8
            grid = Grid(world=self, edge_length=edge_length)
        self.grid = grid

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

    def new_entity(self, ent_id, image_path=None, world_x=None, world_y=None, belong_agent=None):
        self.entities[ent_id] = Entity(core=self.core, ent_id=ent_id, camera=self.camera, grid=self.grid)
        if image_path is not None and world_x is not None and world_y is not None:
            self.entities[ent_id].set_sprite(image_path=image_path, world_x=world_x, world_y=world_y)
        if belong_agent is not None:
            self.entities[ent_id].belong_agent = belong_agent

    def get_entity(self, ent_id):
        if ent_id in self.entities.keys():
            return self.entities[ent_id]
        else:
            return None

    def del_entity(self, ent_id):
        if ent_id in self.entities.keys():
            self.entities[ent_id].self_destruct()
            del self.entities[ent_id]
            return True
        else:
            return False

    def new_stimulation(
            self, sti_id, sti_type, image_path=None, x=None, y=None, trigger_key=None, mouse_r_type='u', text=None
    ):
        if sti_type == 'button':
            self.stimulation[sti_id] = Button(name=sti_id, image_path=image_path, x=x, y=y, core=self.core)
        elif sti_type == 'keyboard':
            self.stimulation[sti_id] = KeyboardButton(name=sti_id, core=self.core, trigger_key=trigger_key)
        elif sti_type == 'mouse':
            self.stimulation[sti_id] = Mouse(name=sti_id, core=self.core, trigger_key=trigger_key, r_type=mouse_r_type)
        elif sti_type == 'text':
            self.stimulation[sti_id] = UIText(name=sti_id, text=text, core=self.core, x=x, y=y)
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
