import sys

import pygame

from Trash.artifacts_Deprecated import Artifact

pygame.init()
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("The Artifact")

the_artifact = Artifact()
the_artifact_icon = pygame.image.load('mark.png')
world_width = 1024
world_height = 768
ax = 512
ay = 384
w = the_artifact_icon.get_width()
h = the_artifact_icon.get_height()
ax_canvas = round(ax * 1024 / world_width) - round(w / 2)
ay_canvas = 768 - round(ay * 768 / world_height) - round(h / 2)
current_pitch = 0.0
clock = pygame.time.Clock()
pitch_up = False
pitch_down = False
throttle_up = False
throttle_down = False
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 卸载所有模块
            pygame.quit()
            # 终止程序，确保退出程序
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pitch_up = True
                the_artifact.ThisInput.pitch_neutral()
            elif event.key == pygame.K_s:
                pitch_down = True
                the_artifact.ThisInput.pitch_neutral()
            elif event.key == pygame.K_UP:
                throttle_up = True
            elif event.key == pygame.K_DOWN:
                throttle_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                pitch_up = False
                the_artifact.ThisInput.pitch_neutral()
            elif event.key == pygame.K_s:
                pitch_down = False
                the_artifact.ThisInput.pitch_neutral()
            elif event.key == pygame.K_UP:
                throttle_up = False
            elif event.key == pygame.K_DOWN:
                throttle_down = False

    if pitch_up:
        the_artifact.ThisInput.pitch_up()
    if pitch_down:
        the_artifact.ThisInput.pitch_down()
    if throttle_up:
        the_artifact.ThisInput.throttle_up()
    if throttle_down:
        the_artifact.ThisInput.throttle_down()

    the_artifact.update_stats(drag=2, gravity=0.5)
    core = (the_artifact.ThisStats.location[0], 768-the_artifact.ThisStats.location[1])
    screen.fill('white')
    icon_rotated = pygame.transform.rotate(the_artifact_icon, -the_artifact.ThisStats.ang)
    screen.blit(icon_rotated, icon_rotated.get_rect(center=tuple(core)))
    pygame.display.update()
