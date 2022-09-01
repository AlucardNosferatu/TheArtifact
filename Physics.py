import pygame
from Box2D.b2 import world, polygonShape, staticBody, dynamicBody
from pygame.locals import (QUIT, KEYDOWN, K_ESCAPE)


def body_vertices_2_pygame_polygon(shape):
    v_pos = [(body.transform * v) * PPM for v in shape.vertices]
    v_pos = [(v[0], SCREEN_HEIGHT - v[1]) for v in v_pos]
    return v_pos


PPM = 20.0  # pixels per meter
TARGET_FPS = 60
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

dynamic_body = world.CreateDynamicBody(position=(10, 15), angle=3.14 / 4)
box = dynamic_body.CreatePolygonFixture(box=(2, 1), density=1, friction=0.1)

colors = {
    staticBody: (255, 255, 255, 255),
    dynamicBody: (127, 127, 127, 255),
}

running = True
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

    world.Step(TIME_STEP, 10, 10)

    pygame.display.flip()
    clock.tick(TARGET_FPS)

pygame.quit()
print('Done!')

# Basic Physics:√
# Collision:√
# Breakable Connection:×
# Lift & Drag:×
