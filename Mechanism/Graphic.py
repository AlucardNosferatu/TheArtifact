# (surface, (pos_x, pos_y), active, ang, (mag_x, mag_y), flip)
import pygame
import pygame.mouse
from pygame import MOUSEBUTTONDOWN, Surface

from Mechanism.Game import Game


class Camera:
    def __init__(self, screen: Surface):
        """
        初始化 Camera 对象。
        """
        self.world_x = 0  # 摄像头的 x 坐标
        self.world_y = 0  # 摄像头的 y 坐标
        self.w = screen.get_width()
        self.h = screen.get_height()


class Sprite:
    def __init__(self, name, image_path, x, y, game: Game):
        """
        初始化 Sprite 对象。
        :param x: Sprite 的 x 坐标，默认为 0。
        :param y: Sprite 的 y 坐标，默认为 0。
        """
        self.name = name
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
        self.game = game
        self.game.load_routine(func=self.render_routine, r_type='w')

    def render_routine(self, params, recent_input):
        return self.render()

    def render(self):
        ret_tuple = (
            self.name,
            (
                self.surface,
                (self.x, self.y),
                self.visible,
                self.rotation,
                (self.scale_x * self.surface.get_width() / 100, self.scale_y * self.surface.get_height() / 100),
                [self.flip_x, self.flip_y]
            )
        )
        return ret_tuple


class EntitySprite(Sprite):
    def __init__(self, name, image_path, cam: Camera, world_x, world_y, game):
        self.cam = cam
        self.world_x = world_x
        self.world_y = world_y
        super().__init__(name=name, image_path=image_path, x=0, y=0, game=game)
        self.update()

    def update(self):
        self.x = self.world_x - self.cam.world_x + round(self.cam.w / 2)
        self.y = self.world_y - self.cam.world_y + round(self.cam.h / 2)
        self.visible = self.in_sight()

    def in_sight(self):
        return 0 < self.x < self.cam.w and 0 < self.y < self.cam.h

    def render(self):
        self.update()
        return super().render()


class Button(Sprite):
    def __init__(self, name, image_path, x, y, game: Game):
        super().__init__(name=name, image_path=image_path, x=x, y=y, game=game)
        self.callback = None
        self.game.remove_routine(func=self.render_routine)
        self.game.load_routine(func=self.check_click, r_type='u')

    def check_click(self, params, recent_input):
        border = 0
        hh = self.surface.get_height() / 2
        hw = self.surface.get_width() / 2
        for event in recent_input:
            e = event[0]
            timestamp = event[1]
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                (mx, my) = pygame.mouse.get_pos()
                if (self.x - hw) + border < mx < (self.x + hw) - border and (self.y - hh) + border < my < (
                        self.y + hh) - border:
                    if self.callback is not None:
                        self.game.load_routine(func=self.callback)
        return self.render()

    def reg_callback(self, callback):
        self.callback = callback
