from math import sqrt

import pygame
from pygame import Surface

from Config import SurfaceCache, GameVars


class Camera:
    def __init__(self, screen: Surface, moving_speed=8):
        """
        初始化 Camera 对象。
        """
        self.world_x = 0  # 摄像头的 x 坐标
        self.world_y = 0  # 摄像头的 y 坐标
        self.w = screen.get_width()
        self.h = screen.get_height()
        self.moving_speed = moving_speed

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


class Entity(pygame.sprite.Sprite):
    all_sprites = pygame.sprite.RenderPlain()

    def __init__(self, image_path, world_x, world_y, cam):
        pygame.sprite.Sprite.__init__(self)
        if image_path.startswith('#'):
            self.image = SurfaceCache.cache[image_path]
        else:
            self.surface = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.world_x = world_x
        self.world_y = world_y
        self.cam = cam
        self.x = 0
        self.y = 0
        self.world2screen()
        self.check_visibility = True
        self.visible = True

        # noinspection PyTypeChecker
        Entity.all_sprites.add((self,))

    def ent_move(self, d_x=0, d_y=0):
        self.world_x += d_x
        self.world_y += d_y

    def ent_move_vector(self, f_x=0, f_y=0, displacement=0):
        mag = sqrt((f_x ** 2) + (f_y ** 2))
        if mag != 0.0:
            d_x = round(displacement * f_x / mag)
            d_y = round(displacement * f_y / mag)
            self.ent_move(d_x=d_x, d_y=d_y)

    def in_sight(self):
        return 0 < self.x < self.cam.w and 0 < self.y < self.cam.h

    def world2screen(self):
        self.x = self.world_x - self.cam.world_x + round(self.cam.w / 2)
        self.y = self.world_y - self.cam.world_y + round(self.cam.h / 2)
        self.rect.center = (self.x, self.y)

    # noinspection PyTypeChecker
    def update(self):
        # 'change self.rect to move'
        self.world2screen()
        if self.check_visibility:
            self.visible = self.in_sight()
        else:
            self.visible = True
        if self.visible:
            if not Entity.all_sprites.has((self,)):
                Entity.all_sprites.add((self,))
        else:
            if Entity.all_sprites.has((self,)):
                Entity.all_sprites.remove((self,))


def jet_m(jet):
    m_w_x, m_w_y = jet.cam.mouse_world_pos()
    d_w_x = m_w_x - jet.world_x
    d_w_y = m_w_y - jet.world_y
    if jet is not None:
        jet_spd = GameVars.g_vars['jet_spd']
        jet.ent_move_vector(f_x=d_w_x, f_y=d_w_y, displacement=jet_spd)
    return None, None


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.SCALED)
    all_sprites = Entity.all_sprites
    clock = pygame.time.Clock()
    SurfaceCache.load('#jet', 'Assets/F-5E.png')
    GameVars.load('jet_spd', 16)
    cam = Camera(screen=screen)
    cam.focus(world_x=0, world_y=0)
    jet = Entity(image_path='#jet', world_x=0, world_y=0, cam=cam)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    going = True
    nav = False
    while going:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                going = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                nav = True
            elif event.type == pygame.MOUSEBUTTONUP:
                nav = False
        if nav:
            jet_m(jet=jet)

        all_sprites.update()
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


# Game Over


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()
