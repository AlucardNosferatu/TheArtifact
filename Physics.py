from math import sqrt

import pygame
from Box2D.b2 import world, polygonShape, staticBody, dynamicBody, fixtureDef
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)

cd_test = 0.3
ad_test = 1.295


def body_vertices_2_pygame_polygon(shape):
    v_pos = [(body.transform * v) * PPM for v in shape.vertices]
    v_pos = [(v[0], SCREEN_HEIGHT - v[1]) for v in v_pos]
    return v_pos


def point2line(point, line, center):
    m, n = point
    a, b, c = line
    if a != 0 or b != 0:
        if b != 0:
            y_of_same_x = (a * m + c) / (-b)
            if y_of_same_x > n:
                side = 0
            else:
                side = 1
        else:
            if m < (-c) / a:
                side = 0
            else:
                side = 1
        d = abs(a * m + b * n + c) / sqrt((a ** 2) + (b ** 2))
    else:
        dx = center.x - m
        dy = center.y - n
        side = 2
        d = sqrt((dx ** 2) + (dy ** 2))
    return d, side


def apply_drag(drag_body):
    v = drag_body.linearVelocity
    vertices = drag_body.fixtures[0].shape.vertices
    vertices = [(body.transform * vertex) for vertex in vertices]
    xc, yc = drag_body.worldCenter
    # v.y(x-xc)-v.x(y-yc)=0
    # v.y*x-v.x*y-v.y*xc+v.x*yc=0
    a = v.y
    b = -v.x
    c = v.x * yc - v.y * xc
    line = [a, b, c]
    longest_dist = [0, 0, 0]
    for vertex in vertices:
        dst, side = point2line(vertex, line, drag_body.worldCenter)
        if dst > longest_dist[side]:
            longest_dist[side] = dst
    if longest_dist[0] != 0 and longest_dist[1] != 0:
        ps_test = longest_dist[0] + longest_dist[1]
    else:
        ps_test = longest_dist[2] * 2
    force = v * (-v.length) * 0.5 * cd_test * ad_test * ps_test
    drag_body.ApplyForce(force, drag_body.worldCenter, True)


PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Simple pygame example')
clock = pygame.time.Clock()

world = world(gravity=(0, -50), doSleep=True)

ground_body = world.CreateStaticBody(
    position=(32, 2),
    shapes=polygonShape(box=(31, 1))
)
fixture = fixtureDef(shape=polygonShape(box=(1, 2)), density=1)
fixture2 = fixtureDef(shape=polygonShape(box=(2, 1)), density=1)
dynamic_body = world.CreateDynamicBody(position=(20, 50), angle=0, fixtures=fixture)
dynamic_body2 = world.CreateDynamicBody(position=(25, 50), angle=0, fixtures=fixture2)
joint = world.CreateRevoluteJoint(
    bodyA=dynamic_body,
    bodyB=dynamic_body2,
    anchor=(dynamic_body.worldCenter + dynamic_body2.worldCenter) / 2,
    collideConnected=True
)
colors = {
    staticBody: (255, 255, 255, 255),
    dynamicBody: (127, 127, 127, 255),
}
running = True
joint_exist = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
    screen.fill((0, 0, 0, 0))
    # Draw the world
    for body in world.bodies:  # or: world.bodies
        for fixture in body.fixtures:
            fix_vertices = body_vertices_2_pygame_polygon(fixture.shape)
            pygame.draw.polygon(screen, colors[body.type], fix_vertices)
        if body.type is dynamicBody:
            apply_drag(body)
    if joint_exist:
        x, y = joint.GetReactionForce(10)
        f = sqrt((x ** 2) + (y ** 2))
        print(f)
        if f > 500:
            world.DestroyJoint(joint)
            joint_exist = False
    world.Step(TIME_STEP, 10, 10)
    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print('Done!')

# Basic Physics:√
# Joint Collision:√
# Breakable Connection:√
# Drag:√
# Lift:×
