import sys
import math
import pygame


def cal_pitch_angle(dy, dx):
    return math.atan2(dy, dx)


def cal_vel_factors(pitch_ang, speed_mag):
    vx = round(speed_mag * math.cos(pitch_ang * 3.14 / 180))
    vy = round(speed_mag * math.sin(pitch_ang * 3.14 / 180))
    return vx, vy


pygame.init()
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("The Artifact")

the_artifact_icon = pygame.image.load('../mark.png')
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
pitch_up_acc = 0
pitch_down_acc = 0
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 卸载所有模块
            pygame.quit()
            # 终止程序，确保退出程序
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                pitch_up = True
                pitch_up_acc = 0
            elif event.key == pygame.K_w:
                pitch_down = True
                pitch_down_acc = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                pitch_up = False
                pitch_up_acc = 0
            elif event.key == pygame.K_w:
                pitch_down = False
                pitch_down_acc = 0
    if pitch_up:
        pitch_up_acc += 1
        if pitch_up_acc >= 4:
            pitch_up_acc = 4
        current_pitch -= pitch_up_acc
    if pitch_down:
        pitch_down_acc += 1
        if pitch_down_acc >= 4:
            pitch_down_acc = 4
        current_pitch += pitch_down_acc
    lift_ang = current_pitch - 90
    vel_x_l, vel_y_l = cal_vel_factors(lift_ang, 2)
    vel_x_f, vel_y_f = cal_vel_factors(current_pitch, 10)
    vel_x = vel_x_l + vel_x_f
    vel_y = vel_y_l + vel_y_f
    vel_y += 4.9
    ax_canvas += vel_x
    ay_canvas += vel_y
    core = (ax_canvas, ay_canvas)
    screen.fill('white')
    icon_rotated = pygame.transform.rotate(the_artifact_icon, -current_pitch)
    screen.blit(icon_rotated, icon_rotated.get_rect(center=tuple(core)))
    pygame.display.update()
