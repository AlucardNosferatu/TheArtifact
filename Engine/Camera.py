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
        self.cam = cam
        self.world_x = world_x
        self.world_y = world_y
        super().__init__(image_path, 0, 0)
        self.update()

    def update(self):
        self.x = self.world_x - self.cam.world_x + round(self.cam.w / 2)
        self.y = self.world_y - self.cam.world_y + round(self.cam.h / 2)

    def render(self):
        self.update()
        return super().render()
