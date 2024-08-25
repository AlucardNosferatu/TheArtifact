import pygame
import pygame.mouse
from pygame import MOUSEBUTTONDOWN, Surface, MOUSEBUTTONUP, KEYDOWN, KEYUP

from Engine.Core import Core

buttons = []


class Camera:
    def __init__(self, screen: Surface):
        """
        初始化 Camera 对象。
        """
        self.world_x = 0  # 摄像头的 x 坐标
        self.world_y = 0  # 摄像头的 y 坐标
        self.w = screen.get_width()
        self.h = screen.get_height()

    def focus(self, world_x, world_y):
        self.world_x = world_x
        self.world_y = world_y

    def move(self, d_x=0, d_y=0):
        self.world_x += d_x
        self.world_y += d_y

    def mouse_world_pos(self):
        (mx, my) = pygame.mouse.get_pos()
        m_w_x = mx - round(self.w / 2) + self.world_x
        m_w_y = my - round(self.h / 2) + self.world_y
        return m_w_x, m_w_y


class Sprite:
    precached_surfaces = {}

    def __init__(self, name, image_path, x, y, core: Core):
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
        if image_path is not None:
            if image_path.startswith('#'):
                self.surface = Sprite.precached_surfaces[image_path]
            else:
                self.surface = pygame.image.load(self.image_path).convert_alpha()
        else:
            self.surface = None
        self.core = core
        self.core.append_routine(func=self.render_routine, r_type='w')

    @staticmethod
    def precache_surfaces(key, image_path):
        Sprite.precached_surfaces[key] = pygame.image.load(image_path).convert_alpha()

    def render_routine(self, params, recent_input):
        _, _ = params, recent_input
        return self.render()

    def delete_routine(self, params, recent_input):
        _, _ = params, recent_input
        ret_tuple = (self.name, ['DELETE_THIS', self])
        return ret_tuple

    def render(self):
        s = pygame.transform.rotate(surface=self.surface, angle=self.rotation)
        s = pygame.transform.scale(
            surface=s, size=(
                self.scale_x * self.surface.get_width() / 100, self.scale_y * self.surface.get_height() / 100
            )
        )
        s = pygame.transform.flip(surface=s, flip_x=self.flip_x, flip_y=self.flip_y)
        ret_tuple = (self.name, (s, (self.x, self.y), self.visible, None, None, None))
        return ret_tuple


class EntitySprite(Sprite):
    def __init__(self, name, image_path, cam: Camera, world_x, world_y, core: Core):
        self.cam = cam
        self.world_x = world_x
        self.world_y = world_y
        super().__init__(name=name, image_path=image_path, x=0, y=0, core=core)
        self.check_visibility = True
        self.update()

    def move(self, d_x=0, d_y=0):
        self.world_x += d_x
        self.world_y += d_y

    def relocate(self, world_x=None, world_y=None):
        if world_x is not None:
            self.world_x = world_x
        if world_y is not None:
            self.world_y = world_y

    def update(self):
        self.x = self.world_x - self.cam.world_x + round(self.cam.w / 2)
        self.y = self.world_y - self.cam.world_y + round(self.cam.h / 2)
        if self.check_visibility:
            self.visible = self.in_sight()
        else:
            self.visible = True

    def in_sight(self):
        return 0 < self.x < self.cam.w and 0 < self.y < self.cam.h

    def render(self):
        self.update()
        return super().render()


class EntityText(EntitySprite):
    text_generator = None

    def __init__(self, name, text, core: Core, cam: Camera, world_x, world_y, font=None, color=None):
        super().__init__(name=name, image_path=None, cam=cam, world_x=world_x, world_y=world_y, core=core)
        if font is None:
            self.font = pygame.font.Font('Assets/Roboto.ttf', 30)
        if color is None:
            self.color = (255, 0, 0)
        if callable(text):
            self.text_generator = text
            self.surface = None
        else:
            self.text_generator = None
            self.surface = self.font.render(text=text, antialias=True, color=pygame.Color(self.color))

    def render(self):
        if self.text_generator is not None:
            text = str(self.text_generator())
            self.surface = self.font.render(text.encode('utf-8'), True, pygame.Color(self.color))
        return super().render()


class Button(Sprite):
    def __init__(self, name, image_path, x, y, core: Core):
        super().__init__(name=name, image_path=image_path, x=x, y=y, core=core)
        self.callback = None
        self.reg_button()
        self.core.remove_routine(func=self.render_routine)
        self.core.append_routine(func=self.check_click, r_type='u')

    def reg_button(self):
        buttons.append(self)

    def in_button(self):
        border = 0
        hh = self.surface.get_height() / 2
        hw = self.surface.get_width() / 2
        (mx, my) = pygame.mouse.get_pos()
        x_in_btn = (self.x - hw) + border < mx < (self.x + hw) - border
        y_in_btn = (self.y - hh) + border < my < (self.y + hh) - border
        return x_in_btn and y_in_btn

    def check_click(self, params, recent_input):
        for event in recent_input:
            if event[0].type == MOUSEBUTTONDOWN and event[0].button == 1:
                if self.in_button():
                    if self.callback is not None:
                        self.core.append_routine(func=self.callback, r_type='u')
            elif event[0].type == MOUSEBUTTONUP and event[0].button == 1:
                if self.callback is not None:
                    self.core.remove_routine(func=self.callback, r_type='u')
        return self.render()

    def reg_callback(self, callback):
        self.callback = callback

    def del_callback(self, r_type='u'):
        if self.callback is not None:
            if r_type not in ['u', 'w', 'both']:
                raise ValueError('unrecognized r_type:{}'.format(r_type))
            if r_type == 'both':
                self.core.remove_routine(func=self.callback, r_type='u')
                self.core.remove_routine(func=self.callback, r_type='w')
            else:
                self.core.remove_routine(func=self.callback, r_type=r_type)
            self.callback = None
            return True
        else:
            return False


class UIText(Button):
    text_generator = None

    def __init__(self, name, text, core: Core, x, y, font=None, color=None):
        super().__init__(name=name, image_path=None, x=x, y=y, core=core)
        if font is None:
            self.font = pygame.font.Font('Assets/Roboto.ttf', 30)
        if color is None:
            self.color = (255, 0, 0)
        if callable(text):
            self.text_generator = text
            self.surface = None
        else:
            self.text_generator = None
            self.surface = self.font.render(text=text, antialias=True, color=pygame.Color(self.color))

    def render(self):
        if self.text_generator is not None:
            text = str(self.text_generator())
            self.surface = self.font.render(text.encode('utf-8'), True, pygame.Color(self.color))
        return super().render()


class KeyboardButton(Button):
    def __init__(self, name, core: Core, trigger_key):
        super().__init__(name=name, image_path='Assets/btn.png', x=0, y=0, core=core)
        self.trigger_key = trigger_key

    def reg_button(self):
        pass

    def in_button(self):
        return False

    def check_click(self, params, recent_input):
        # if len(recent_input) > 0:
        #     print('check thread', recent_input)
        for event in recent_input:
            if event[0].type == KEYDOWN and event[0].key == self.trigger_key:
                if self.callback is not None:
                    self.core.append_routine(func=self.callback, r_type='u')
            elif event[0].type == KEYUP and event[0].key == self.trigger_key:
                if self.callback is not None:
                    self.core.remove_routine(func=self.callback, r_type='u')
        return None, None


class Mouse(KeyboardButton):
    def __init__(self, name, core: Core, trigger_key, r_type='u'):
        super().__init__(name=name, core=core, trigger_key=trigger_key)
        self.r_type = r_type

    def in_button(self):
        for button in buttons:
            if button.in_button():
                return False
        return True

    def check_click(self, params, recent_input):
        for event in recent_input:
            if event[0].type == MOUSEBUTTONDOWN and event[0].button == self.trigger_key:
                if self.in_button():
                    if self.callback is not None:
                        self.core.append_routine(func=self.callback, r_type=self.r_type)
            elif event[0].type == MOUSEBUTTONUP and event[0].button == self.trigger_key:
                if self.callback is not None:
                    self.core.remove_routine(func=self.callback, r_type=self.r_type)
        return None, None
