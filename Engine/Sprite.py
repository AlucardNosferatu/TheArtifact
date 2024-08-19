# (surface, (pos_x, pos_y), active, ang, (mag_x, mag_y), flip)
import pygame


class Sprite:
    def __init__(self, image_path, x, y):
        """
        初始化 Sprite 对象。
        :param x: Sprite 的 x 坐标，默认为 0。
        :param y: Sprite 的 y 坐标，默认为 0。
        """
        self.image_path = image_path
        self.x = x
        self.y = y
        self.flip_x = False
        self.flip_y = False
        self.scale_x = 100.0
        self.scale_y = 100.0
        self.visible = True
        self.rotation = 0.0
        self.surface = pygame.image.load(self.image_path)

    def render(self):
        return self.surface, (self.x, self.y), self.visible, self.rotation, (self.scale_x, self.scale_y), [
            self.flip_x,
            self.flip_y
        ]
