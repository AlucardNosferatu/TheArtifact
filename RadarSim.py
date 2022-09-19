import math

import numpy as np
import pygame

from RayTracer import opticalElement
from RayTracer.rayTracer import BLACK, GREEN


def get_start_points(src_b_):
    px_ratio = 16
    for i, t in enumerate(src_b_):
        t = list(t)
        t = [
            t[0] * px_ratio,
            t[1] * px_ratio
        ]
        src_b_[i] = tuple(t)
    max_x = src_b_[0][0]
    max_y = src_b_[0][1]
    min_x = src_b_[0][0]
    min_y = src_b_[0][1]
    for v in src_b_:
        if v[0] > max_x:
            max_x = v[0]
        elif v[0] < min_x:
            min_x = v[0]
        if v[1] > max_y:
            max_y = v[1]
        elif v[1] < min_y:
            min_y = v[1]
    rect_size = (
        max_x - min_x,
        max_y - min_y
    )
    rect_offset = [
        rect_size[0] * 0.5 + min_x,
        rect_size[1] * 0.5 + min_y
    ]
    for i, t in enumerate(src_b_):
        t = list(t)
        t = [
            t[0] - rect_offset[0],
            t[1] - rect_offset[1],
        ]
        src_b_[i] = tuple(t)
    radius = math.sqrt(rect_size[0] ** 2 + rect_size[1] ** 2)
    start_points = []
    start_orient = []
    for i in range(int(360 / 5)):
        ang = i * 5
        sp = (np.cos(ang * np.pi / 180) * radius, np.sin(ang * np.pi / 180) * radius)
        start_points.append(sp)
        start_orient.append(ang)
    return src_b_, start_points, start_orient, radius


def polygon_mirror(src_b_, elements_):
    for i in range(len(src_b_)):
        start = src_b_[i]
        if i == len(src_b_) - 1:
            end = src_b_[0]
        else:
            end = src_b_[i + 1]
        pos = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        ang = math.atan2(dy, dx) * 180 / math.pi
        length = math.sqrt(dx ** 2 + dy ** 2)
        half_length = length / 2
        elements_.append(opticalElement.FlatMirror(np.array(pos), ang, half_length, {'color': BLACK}))
    return elements_


def ray_scan(start_point, ang_offset, rays_):
    for i in range(int(180 / 5) + 1):
        theta = 5 * i + ang_offset
        rays_.append(
            {
                'pos': np.array(list(start_point)),
                'dir': np.array([np.cos(np.pi * theta / 180), np.sin(np.pi * theta / 180)]),
                'color': GREEN
            }
        )
    return rays_


src_b = [
    (-4 + 5, 1 + 5),
    (-6 + 5, 0 + 5),
    (-4 + 5, -1 + 5),
    (4 + 5, -1 + 5),
    (6 + 5, 0 + 5),
    (4 + 5, 1 + 5)
]
elements = []
src_b, sp_list, so_list, rad = get_start_points(src_b)
elements = polygon_mirror(src_b, elements)
pygame.init()
clock = pygame.time.Clock()
canvas_size = (
    2 * rad + 100,
    2 * rad + 100
)
screen = pygame.display.set_mode(canvas_size)
pygame.display.set_caption("Ray Tracer")
rays = []
r_sp_index = 0
while True:
    for event_ in pygame.event.get():
        # -------Mouse Events--------
        if event_.type == pygame.MOUSEBUTTONDOWN:  # Mouse click events
            print(event_)
        elif event_.type == pygame.MOUSEBUTTONUP:  # Mouse release event
            print(event_)
        if event_.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
    rays = ray_scan(sp_list[r_sp_index], 90 + 5 * r_sp_index, rays)
    r_sp_index += 1
    if r_sp_index >= len(p_list):
        r_sp_index = 0
    rays.clear()
