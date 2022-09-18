#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# noinspection SpellCheckingInspection
"""
Created on Sun Nov 25 16:15:36 2018

@author: jaymz
"""

import math

import numpy as np
import pygame

from AeroSim import conv_vert
from RayTracer import opticalElement
from RayTracer.opticalElement import FlatMirror, CurvedMirror, OpticalElement


# noinspection PyPep8Naming,PyMethodMayBeStatic
class CurvedReceiver(OpticalElement):
    rec_count = 0

    def __init__(self, pos, orientation, boundaries, properties):
        super().__init__(pos, orientation, boundaries, properties)
        self.properties['color'] = RED

    def reset_count(self):
        self.rec_count = 0

    def elementType(self):
        return 'CurvedReceiver'

    # self.boundaries = [angularSize, radius]
    # self.orientation = direction

    def getCenterPoint(self):
        angleCent = self.orientation * np.pi / 180
        return np.array([self.pos[0] - self.boundaries[1] * np.cos(angleCent),
                         self.pos[1] - self.boundaries[1] * np.sin(angleCent)])

    def rayIntersection(self, ray_pos, ray_dir):
        center = self.getCenterPoint()
        rx, ry, vx, vy, R = ray_pos[0] - center[0], ray_pos[1] - center[1], ray_dir[0], ray_dir[1], self.boundaries[1]
        angExtent = np.arctan(self.boundaries[0] / R) * 180 / np.pi
        if (2 * rx * vx + 2 * ry * vy) ** 2 - 4 * (-R ** 2 + rx ** 2 + ry ** 2) * (vx ** 2 + vy ** 2) < 0:
            # self.properties['color'] = RED
            return None
        t_val1 = (-2 * rx * vx - 2 * ry * vy - np.sqrt(
            (2 * rx * vx + 2 * ry * vy) ** 2 - 4 * (-R ** 2 + rx ** 2 + ry ** 2) * (vx ** 2 + vy ** 2))) / (
                         2 * (vx ** 2 + vy ** 2))
        t_val2 = (-2 * rx * vx - 2 * ry * vy + np.sqrt(
            (2 * rx * vx + 2 * ry * vy) ** 2 - 4 * (-R ** 2 + rx ** 2 + ry ** 2) * (vx ** 2 + vy ** 2))) / (
                         2 * (vx ** 2 + vy ** 2))

        intersect1 = np.array(ray_pos) + t_val1 * ray_dir
        intersect2 = np.array(ray_pos) + t_val2 * ray_dir

        angle1 = np.arctan2(intersect1[1] - center[1], intersect1[0] - center[0]) * 180 / np.pi % 360
        angle2 = np.arctan2(intersect2[1] - center[1], intersect2[0] - center[0]) * 180 / np.pi % 360

        b1, b2 = (self.orientation - angExtent) % 360, (self.orientation + angExtent) % 360

        if self.angleBetween(angle1, b1, b2):
            if self.angleBetween(angle2, b1, b2):
                dist1 = np.linalg.norm(ray_pos - intersect1)
                dist2 = np.linalg.norm(ray_pos - intersect2)
                if dist1 < dist2:
                    self.rec_count += 1
                    print(self.orientation, 'side 1')
                    self.properties['color'] = GREEN
                    return None
                self.rec_count += 1
                print(self.orientation, 'side 2')
                self.properties['color'] = GREEN
                return None
            else:
                self.rec_count += 1
                print(self.orientation, 'side 1')
                self.properties['color'] = GREEN
                return None

        elif self.angleBetween(angle2, b1, b2):
            self.rec_count += 1
            print(self.orientation, 'side 2')
            self.properties['color'] = GREEN
            return None
        else:
            # self.properties['color'] = RED
            return None

    def reflect(self, ray_pos, ray_dir, intersect):
        center = self.getCenterPoint()
        v_p = np.array([intersect[0] - center[0], intersect[1] - center[1]])
        v_p = v_p / np.linalg.norm(v_p)
        vin = np.array(ray_dir)
        return vin - 2 * np.dot(ray_dir, v_p) * v_p

    def checkBoundaries(self, pos):
        return False

    def angleBetween(self, angle, b1, b2):
        diff1, diff2 = abs(angle % 360 - b1 % 360), abs(angle % 360 - b2 % 360)
        width = abs(b1 - b2)
        if width > 180:
            width = 360 - width
        if diff1 > 180:
            diff1 = 360 - diff1
        if diff2 > 180:
            diff2 = 360 - diff2
        return (diff1 < width) and (diff2 < width)

    def setOrientation(self, angleDeg):
        self.orientation = angleDeg % 360

    def draw(self, scr, screenPosFunction):
        pass

    def drawSelected(self, scr, screenPosFunc):
        pass


size = (700, 700)
screen = pygame.display.set_mode(size)

coord_lims_default = np.array([[-1000.0, 1000.0], [-1000.0, 1000.0]])
coord_lims = coord_lims_default
mousePos: np.ndarray | None = None
elements: list[FlatMirror | CurvedMirror | CurvedReceiver] = []
rays = []
MAX_BOUNCE = 100
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


def direct_draw_line(element):
    color = BLUE
    screen_x, screen_y, scale_x, scale_y = element.pos[0], element.pos[1], 1, 1
    angle_rad = element.orientation * np.pi / 180
    if isinstance(element.properties, dict):
        color = element.properties['color']
    x1, y1 = element.boundaries * np.cos(angle_rad) * scale_x + screen_x, element.boundaries * np.sin(
        angle_rad) * scale_y + screen_y
    x2, y2 = -element.boundaries * np.cos(angle_rad) * scale_x + screen_x, -element.boundaries * np.sin(
        angle_rad) * scale_y + screen_y
    pygame.draw.line(screen, color, [x1, y1], [x2, y2], 7)


def direct_draw_arc(element):
    screen_x, screen_y, scale_x, scale_y = element.pos[0], element.pos[1], 1, 1
    radius = element.boundaries[1]
    ang_ext = element.boundaries[0]
    dx_from_c = round(np.cos(element.orientation * np.pi / 180) * radius)
    dy_from_c = round(np.sin(element.orientation * np.pi / 180) * radius)
    c_x = screen_x - dx_from_c
    c_y = screen_y + dy_from_c
    top_left_x = c_x - radius
    top_left_y = c_y - radius
    color = element.properties['color']
    b1 = (element.orientation - (ang_ext / 2)) * np.pi / 180
    b2 = (element.orientation + (ang_ext / 2)) * np.pi / 180
    rect_ellipse = [
        top_left_x,
        top_left_y,
        radius * 2,
        radius * 2
    ]
    pygame.draw.arc(
        screen,
        color,
        rect_ellipse,
        b1,
        b2,
        1
    )


def ray_trace():
    output_rays = [rays]
    for i in range(0, MAX_BOUNCE):
        new_rays = []
        for r in output_rays[-1]:
            r: dict[str, None]
            min_dist = np.inf
            closest_elem = None
            closest_intersect = None
            for elem in elements:
                if elem.elementType() == 'CurvedReceiver':
                    if r['color'] == GREEN:
                        continue
                intersect = elem.rayIntersection(r['pos'], r['dir'])
                if elem.orientation == 105:
                    print('105', intersect, r)
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
                dir_new = closest_elem.reflect(r['pos'], r['dir'], closest_intersect)
                dir_new = dir_new / np.linalg.norm(dir_new)
                r['intersect'] = closest_intersect
                new_rays.append({'pos': closest_intersect, 'dir': dir_new, 'color': BLUE})
            else:
                r['intersect'] = None
        if len(new_rays) != 0:
            output_rays.append(new_rays)
        else:
            break
    return output_rays


def get_ray_start_p(rect_size):
    dx = rect_size[0]
    dy = rect_size[1]
    diameter = math.sqrt(dx ** 2 + dy ** 2)
    radius = diameter
    # radius=2*(diameter/2)
    # 1 start point per 5°
    points_list = []
    ang_list = []
    for i in range(int(360 / 5)):
        point = (round(np.cos(5 * i * np.pi / 180) * radius), round(np.sin(5 * i * np.pi / 180) * radius))
        point = list(point)
        point[0] += round(rect_size[0] / 2)
        point[1] += round(rect_size[1] / 2)
        point[1] = rect_size[1] - point[1]
        points_list.append(tuple(point))
        ang_list.append(i * 5)
    # center is 1/2 rect_size
    return points_list, ang_list, radius


def fit_square(points, old_scr_size, new_scr_size):
    dx = (new_scr_size[0] - old_scr_size[0]) / 2
    dy = (new_scr_size[1] - old_scr_size[1]) / 2
    for i, point in enumerate(points):
        point = list(point)
        point[0] += dx
        point[1] += dy
        points[i] = tuple(point)
    return points


def ray_scan(start_point, ang_offset):
    for i in range(int(180 / 5) + 1):
        theta = 5 * i + ang_offset
        rays.append(
            {
                'pos': np.array(list(start_point)),
                'dir': np.array([np.cos(np.pi * theta / 180), np.sin(np.pi * theta / 180)]),
                'color': GREEN
            }
        )


def polygon_mirror(vertices):
    for i in range(len(vertices)):
        start = vertices[i]
        if i == len(vertices) - 1:
            end = vertices[0]
        else:
            end = vertices[i + 1]
        pos = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        ang = math.atan2(dy, dx) * 180 / math.pi
        length = math.sqrt(dx ** 2 + dy ** 2)
        half_length = length / 2
        elements.append(opticalElement.FlatMirror(np.array(pos), ang, half_length, {'color': BLACK}))


def circle_receiver(start_points, start_ang, radius):
    for i in range(len(start_points)):
        elements.append(CurvedReceiver(start_points[i], start_ang[i], [5, radius], {'color': RED}))


def radar_cross_section():
    global size, screen
    src_b = [
        (-4, 2),
        (-5, 2),
        (-6, 0),
        (-2, -1),
        (8, -1),
        (10, 0),
        (7, 1.5),
        (-3.5, 0)
    ]
    vert, canvas_size_pixel = conv_vert(src_b, True)
    p_list, a_list, rad = get_ray_start_p(canvas_size_pixel)
    size = (round(2 * rad) + 100, round(2 * rad) + 100)
    p_list = fit_square(p_list, canvas_size_pixel, size)
    vert = fit_square(vert, canvas_size_pixel, size)
    screen = pygame.display.set_mode(size)
    pygame.init()
    c = pygame.time.Clock()
    pygame.display.set_caption("Ray Tracer")
    done = False
    r_sp_index = 0
    polygon_mirror(vert)
    circle_receiver(p_list, a_list, rad)
    reset_count = False
    while not done:
        print('next source:')
        for event_ in pygame.event.get():
            # -------Mouse Events--------
            if event_.type == pygame.MOUSEBUTTONDOWN:  # Mouse click events
                print(event_)
            elif event_.type == pygame.MOUSEBUTTONUP:  # Mouse release event
                print(event_)
            if event_.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
        rays.clear()
        ray_scan(p_list[r_sp_index], 90 - 5 * r_sp_index)
        r_sp_index += 1
        if r_sp_index >= len(p_list):
            r_sp_index = 0
            reset_count = True
        output_rays = ray_trace()
        screen.fill(WHITE)
        for p in vert:
            pygame.draw.circle(screen, RED, p, 2)
        for p in p_list:
            pygame.draw.circle(screen, BLUE, p, 2)
        for i in range(0, len(elements)):
            if elements[i].elementType() == 'FlatMirror':
                direct_draw_line(elements[i])
            elif elements[i].elementType() == 'CurvedReceiver':
                direct_draw_arc(elements[i])
                if reset_count:
                    print(elements[i].orientation, elements[i].rec_count)
                    elements[i].reset_count()
        if reset_count:
            reset_count = False
        for i_ in range(0, len(output_rays)):
            for j_ in range(0, len(output_rays[i_])):
                x1, y1 = output_rays[i_][j_]['pos']
                if 'intersect' in output_rays[i_][j_] and output_rays[i_][j_]['intersect'] is not None:
                    x2, y2 = output_rays[i_][j_]['intersect']
                else:
                    x2, y2 = output_rays[i_][j_]['pos'] + output_rays[i_][j_]['dir'] * (
                            np.max(coord_lims) - np.min(coord_lims))
                if 'color' in output_rays[i_][j_]:
                    pygame.draw.line(screen, output_rays[i_][j_]['color'], [x1, y1], [x2, y2], 1)
                else:
                    pygame.draw.line(screen, GREEN, [x1, y1], [x2, y2], 1)
        pygame.display.flip()
        c.tick(1)
    # Exit thread after loop has been exited
    pygame.quit()


if __name__ == '__main__':
    radar_cross_section()
