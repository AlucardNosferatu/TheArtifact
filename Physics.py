from math import sqrt

import pygame
from Box2D import b2RevoluteJoint, b2World, b2PolygonShape, b2_staticBody, b2_dynamicBody, b2FixtureDef
from pygame.locals import (QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_w, K_a, K_d)

cd_test = 0.3
ad_test = 1.295

PPM = 20.0  # pixels per meter
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Simple pygame example')
clock = pygame.time.Clock()

world = b2World(gravity=(0, -50), doSleep=True)
colors = {
    b2_staticBody: (255, 255, 255, 255),
    b2_dynamicBody: (127, 127, 127, 255),
}

joint: None | b2RevoluteJoint = None
joint_exist = True
body_init = []
loop_test = []
body_test = []
key_w_test = []
key_a_test = []
key_d_test = []
m_drag_test = []


def body_vertices_2_pygame_polygon(body, shape):
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
    vertices = [(drag_body.transform * vertex) for vertex in vertices]
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


def init_loop():
    global joint, world, body_init
    world.CreateStaticBody(
        position=(32, 2),
        shapes=b2PolygonShape(box=(31, 1))
    )
    for bi in body_init:
        bi()
    print('Done')


def test_1a():
    global joint, world
    fixture = b2FixtureDef(shape=b2PolygonShape(box=(1, 10)), density=100)
    fixture2 = b2FixtureDef(shape=b2PolygonShape(box=(10, 1)), density=0.01)
    dynamic_body = world.CreateDynamicBody(position=(20, 50), angle=-3.14 / 4, fixtures=fixture)
    dynamic_body2 = world.CreateDynamicBody(position=(40, 50), angle=0, fixtures=fixture2)
    joint = world.CreateRevoluteJoint(
        bodyA=dynamic_body,
        bodyB=dynamic_body2,
        anchor=(dynamic_body.worldCenter + dynamic_body2.worldCenter) / 2,
        collideConnected=True
    )


def test_1b():
    global joint, joint_exist
    if joint_exist:
        force = joint.GetReactionForce(1)
        print(force.length)
        if force.length > 500:
            world.DestroyJoint(joint)
            joint_exist = False


def test_2(body):
    if body.type is b2_dynamicBody:
        apply_drag(body)


def pygame_loop():
    global world, loop_test, body_test, key_w_test, key_a_test, key_d_test, m_drag_test
    running = True
    w_test = False
    a_test = False
    d_test = False
    m_start_pos = None
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            if event.type == KEYDOWN and event.key == K_w:
                w_test = True
            if event.type == KEYUP and event.key == K_w:
                w_test = False
            if event.type == KEYDOWN and event.key == K_a:
                a_test = True
            if event.type == KEYUP and event.key == K_a:
                a_test = False
            if event.type == KEYDOWN and event.key == K_d:
                d_test = True
            if event.type == KEYUP and event.key == K_d:
                d_test = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_start_pos = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                m_end_pos = event.pos
                for mdt in m_drag_test:
                    mdt(m_start_pos, m_end_pos)
                m_start_pos = None
        screen.fill((0, 0, 0, 0))
        for body in world.bodies:
            for fixture in body.fixtures:
                fix_vertices = body_vertices_2_pygame_polygon(body, fixture.shape)
                pygame.draw.polygon(screen, colors[body.type], fix_vertices)
            for bt in body_test:
                bt(body)
        for lt in loop_test:
            lt()
        if w_test:
            for wt in key_w_test:
                wt()
        if a_test:
            for at in key_a_test:
                at()
        if d_test:
            for dt in key_d_test:
                dt()
        world.Step(TIME_STEP, 10, 10)
        pygame.display.flip()
        clock.tick(TARGET_FPS)
    pygame.quit()
    print('Done!')


if __name__ == '__main__':
    body_init.append(test_1a)
    loop_test.append(test_1b)
    body_test.append(test_2)
    init_loop()
    pygame_loop()

# Basic Physics:√
# Joint Collision:√
# Breakable Connection:√
# Drag:√
# Lift:×
