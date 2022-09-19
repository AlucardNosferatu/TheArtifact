import math

import numpy as np
import pygame

from RayTracer import opticalElement
from RayTracer.opticalElement import BLACK, GREEN, WHITE, RED, BLUE


def screen_map_function(pos):
    return (
        int(pos[0] + (canvas_size[0] / 2)),
        int(-pos[1] + (canvas_size[1] / 2)),
        1,
        1
    )


def screen_map_inv(pos_screen):
    return (
        int(pos_screen[0] - (canvas_size[0] / 2)),
        int(-(pos_screen[1] - (canvas_size[0] / 2))),
        1,
        1
    )


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
    for i_ in range(len(src_b_)):
        start = src_b_[i_]
        if i_ == len(src_b_) - 1:
            end = src_b_[0]
        else:
            end = src_b_[i_ + 1]
        pos = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        ang = math.atan2(dy, dx) * 180 / math.pi
        length = math.sqrt(dx ** 2 + dy ** 2)
        half_length = length / 2
        elements_.append(opticalElement.FlatMirror(np.array(pos), ang, half_length, {'color': BLACK}))
    return elements_


def circle_receiver(elements_, start_points, start_ang, radius):
    for i_ in range(len(start_points)):
        elements_.append(
            opticalElement.CurvedMirror(
                start_points[i_],
                start_ang[i_],
                [10, radius],
                {'color': BLACK}
            )
        )
    return elements_


def ray_scan(start_point, ang_offset, rays_):
    for i_ in range(int(180 / 5) + 1):
        theta = 5 * i_ + ang_offset
        rays_.append(
            {
                'pos': np.array(list(start_point)),
                'dir': np.array([np.cos(np.pi * theta / 180), np.sin(np.pi * theta / 180)]),
                'color': GREEN
            }
        )
    return rays_


def ray_trace(rays_):
    max_bounce = 10
    output_rays_ = [rays_]
    for i_ in range(0, max_bounce):
        new_rays = []
        for r in output_rays_[-1]:
            min_dist = np.inf
            closest_elem = None
            closest_intersect = None
            for elem in elements:
                if elem.elementType() == 'CurvedMirror' and r['color'] == GREEN:
                    continue
                intersect = elem.rayIntersection(r['pos'], r['dir'])
                if intersect is None:
                    continue
                dist = np.linalg.norm(intersect - r['pos'])
                if dist < .0001:
                    continue
                if min_dist > dist:
                    min_dist = dist
                    closest_elem = elem
                    closest_intersect = intersect
            if closest_elem is not None:
                closest_elem.properties['color'] = RED
                if closest_elem.elementType() == 'CurvedMirror':
                    dir_new = r['dir']
                    dir_new = dir_new / np.linalg.norm(dir_new)
                    r['intersect'] = closest_intersect
                    new_rays.append({'pos': closest_intersect, 'dir': dir_new, 'color': GREEN})
                else:
                    dir_new = closest_elem.reflect(r['pos'], r['dir'], closest_intersect)
                    dir_new = dir_new / np.linalg.norm(dir_new)
                    r['intersect'] = closest_intersect
                    new_rays.append({'pos': closest_intersect, 'dir': dir_new, 'color': RED})
            else:
                r['intersect'] = None
        if len(new_rays) != 0:
            output_rays_.append(new_rays)
    return output_rays_


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
elements = circle_receiver(elements, sp_list, so_list, rad)
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
done = False
while not done:
    for event_ in pygame.event.get():
        # -------Mouse Events--------
        if event_.type == pygame.MOUSEBUTTONDOWN:  # Mouse click events
            print(event_)
        elif event_.type == pygame.MOUSEBUTTONUP:  # Mouse release event
            print(event_)
        if event_.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
    rays.clear()
    rays = ray_scan(sp_list[r_sp_index], 90 + 5 * r_sp_index, rays)
    r_sp_index += 1
    if r_sp_index >= len(sp_list):
        r_sp_index = 0
    output_rays = ray_trace(rays)
    screen.fill(WHITE)
    for p in src_b:
        x, y, _, _ = screen_map_function(p)
        pygame.draw.circle(screen, RED, (x, y), 2)
    for p in sp_list:
        x, y, _, _ = screen_map_function(p)
        pygame.draw.circle(screen, BLUE, (x, y), 2)
    for i in range(0, len(elements)):
        elements[i].draw(screen, screen_map_function)
        elements[i].properties['color'] = BLACK
    for i in range(0, len(output_rays)):
        for j in range(0, len(output_rays[i])):
            x1, y1, _, _ = screen_map_function(output_rays[i][j]['pos'])
            if 'intersect' in output_rays[i][j] and output_rays[i][j]['intersect'] is not None:
                x2, y2, _, _ = screen_map_function(output_rays[i][j]['intersect'])
            else:
                x2, y2, _, _ = screen_map_function(
                    output_rays[i][j]['pos'] + output_rays[i][j]['dir'] * np.max(canvas_size)
                )
            if 'color' in output_rays[i][j]:
                pygame.draw.line(screen, output_rays[i][j]['color'], [x1, y1], [x2, y2], 1)
            else:
                pygame.draw.line(screen, GREEN, [x1, y1], [x2, y2], 1)
    pygame.display.flip()
    clock.tick(1)
    # Exit thread after loop has been exited
pygame.quit()
