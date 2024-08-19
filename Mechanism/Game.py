import pygame.mouse
from pygame import MOUSEBUTTONDOWN

from Engine.Sprite import Sprite


class Game:
    engine_ptr = None

    def load_routine(self, func, multi_inst=False):
        if not self.has_routine(func=func) or multi_inst:
            self.engine_ptr.routine.append(func)

    def has_routine(self, func):
        return func in self.engine_ptr.routine

    def remove_routine(self, func):
        while self.has_routine(func=func):
            self.engine_ptr.routine.remove(func)


class Button(Sprite):
    def __init__(self, btn_name, image_path, x, y, game: Game):
        super().__init__(image_path, x, y)
        self.callback = None
        self.game = game
        self.game.load_routine(func=self.check_click)
        self.btn_name = btn_name

    def check_click(self, params, recent_input):
        hh = self.surface.get_height() / 2
        hw = self.surface.get_width() / 2
        for event in recent_input:
            e = event[0]
            timestamp = event[1]
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                (mx, my) = pygame.mouse.get_pos()
                if (self.x - hw) + 10 < mx < (self.x + hw) - 10 and (self.y - hh) + 10 < my < (self.y + hh) - 10:
                    if self.callback is not None:
                        self.game.load_routine(func=self.callback)
        return self.btn_name, self.render()

    def reg_callback(self, callback):
        self.callback = callback
