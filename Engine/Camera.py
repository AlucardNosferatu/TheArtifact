from pygame import Surface

from Engine.Sprite import Sprite


class Camera:
    def __init__(self, screen: Surface):
        """
        初始化 Camera 对象。
        """
        self.world_x = 0  # 摄像头的 x 坐标
        self.world_y = 0  # 摄像头的 y 坐标
        self.w = screen.get_width()
        self.h = screen.get_height()


class EntitySprite(Sprite):
    def __init__(self, image_path, cam: Camera, world_x, world_y):
        self.world_x = world_x
        self.world_y = world_y
        x = self.world_x - cam.world_x + round(cam.w / 2)
        y = self.world_y - cam.world_y + round(cam.h / 2)
        super().__init__(image_path, x, y)

    def update(self, cam: Camera):
        self.x = self.world_x - cam.world_x + round(cam.w / 2)
        self.y = self.world_y - cam.world_y + round(cam.h / 2)
        return self.surface, (self.x, self.y), self.visible, self.rotation, (self.scale_x, self.scale_y), [
            self.flip_x,
            self.flip_y
        ]
