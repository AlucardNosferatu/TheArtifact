from Engine.Core import Core
from Engine.UI import Camera, EntitySprite


class Entity:
    sprite = None
    ent_id = None

    def __init__(self, core: Core, ent_id):
        self.core = core
        self.ent_id = ent_id
        self.camera = Camera(screen=self.core.renderer.screen)

    def set_sprite(self, image_path, world_x, world_y):
        self.sprite = EntitySprite(
            name=self.ent_id, image_path=image_path, cam=self.camera, world_x=world_x, world_y=world_y, core=self.core
        )


class World(Entity):
    def __init__(self, core: Core, map_image, cam_x=None, cam_y=None, scale_x=200.0, scale_y=200.0):
        super().__init__(core=core, ent_id='world')
        self.set_sprite(image_path=map_image, world_x=0, world_y=0, scale_x=scale_x, scale_y=scale_y)
        if cam_x is not None and cam_y is not None:
            self.camera.focus(world_x=cam_x, world_y=cam_y)
        else:
            self.camera.focus(world_x=self.sprite.world_x, world_y=self.sprite.world_y)
        self.entities: dict[str, Entity] = {}

    def set_sprite(self, image_path, scale_x=200.0, scale_y=200.0, world_x=-1, world_y=-1):
        super().set_sprite(image_path=image_path, world_x=0, world_y=0)
        self.sprite.world_x = round(self.sprite.surface.get_width() / 2)
        self.sprite.world_y = round(self.sprite.surface.get_height() / 2)
        self.sprite.check_visibility = False
        self.sprite.scale_x = scale_x
        self.sprite.scale_y = scale_y

    def new_entity(self, ent_id, image_path=None, world_x=None, world_y=None):
        self.entities[ent_id] = Entity(core=self.core, ent_id=ent_id)
        if image_path is not None:
            self.entities[ent_id].set_sprite(image_path=image_path, world_x=world_x, world_y=world_y)
