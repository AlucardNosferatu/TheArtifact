from math import sqrt

import pygame
from Box2D.b2 import world, polygonShape, staticBody, dynamicBody, fixtureDef
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)


def body_vertices_2_pygame_polygon(shape):
    v_pos = [(body.transform * v) * PPM for v in shape.vertices]
    v_pos = [(v[0], SCREEN_HEIGHT - v[1]) for v in v_pos]
    return v_pos


PPM = 20.0  # pixels per meter
TARGET_FPS = 15
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480

# --- pygame setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Simple pygame example')
clock = pygame.time.Clock()

world = world(gravity=(0, -10), doSleep=True)

ground_body = world.CreateStaticBody(
    position=(16, 2),
    shapes=polygonShape(box=(15, 1))
)
fixture = fixtureDef(shape=polygonShape(box=(1, 2)), density=1)
dynamic_body = world.CreateDynamicBody(position=(12, 11), angle=0, fixtures=fixture)
dynamic_body2 = world.CreateDynamicBody(position=(10, 15), angle=0, fixtures=fixture)
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
            vertices = body_vertices_2_pygame_polygon(fixture.shape)
            pygame.draw.polygon(screen, colors[body.type], vertices)
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
# Lift & Drag:×
