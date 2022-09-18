#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# noinspection SpellCheckingInspection
"""
Created on Sun Nov 25 16:15:36 2018

@author: jaymz
"""

import copy
import math

import numpy as np
import pygame

from AeroSim import conv_vert
from RayTracer import opticalElement
from RayTracer.menu import Menu
from RayTracer.opticalElement import FlatMirror, CurvedMirror, OpticalElement

size = (700, 700)
screen = pygame.display.set_mode(size)

coord_lims_default = np.array([[-1000.0, 1000.0], [-1000.0, 1000.0]])
coord_lims = coord_lims_default
mousePos: np.ndarray | None = None
elements: list[FlatMirror | CurvedMirror] = []
rays = []
MAX_BOUNCE = 100
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# noinspection PyPep8Naming,PyMethodMayBeStatic
class CurvedReceiver(OpticalElement):
    rec_count = 0

    def __init__(self, pos, orientation, boundaries, properties):
        super().__init__(pos, orientation, boundaries, properties)

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
                    return None
                return None
            else:
                return None

        elif self.angleBetween(angle2, b1, b2):
            return None
        else:
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
    # todo
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


def screen_map_function(pos):
    range_x = abs(coord_lims[0][0] - coord_lims[0][1])
    range_y = abs(coord_lims[1][0] - coord_lims[1][1])
    scale_x = float(size[0]) / range_x
    scale_y = float(size[1]) / range_y
    return (
        int((pos[0] - coord_lims[0][0]) / range_x * size[0]),
        int((-pos[1] - coord_lims[1][0]) / range_y * size[1]),
        scale_x,
        scale_y)


def screen_map_inv(pos_screen):
    range_x = abs(coord_lims[0][0] - coord_lims[0][1])
    range_y = abs(coord_lims[1][0] - coord_lims[1][1])
    scale_x = float(size[0]) / range_x
    scale_y = float(size[1]) / range_y
    return (
        int((pos_screen[0] / size[0] * range_x + coord_lims[0][0])),
        int(-pos_screen[1] * range_y / size[1] - coord_lims[1][0]),
        scale_x, scale_y)


def add_flat_mirror():
    x_, y_, _, _ = screen_map_inv(mousePos)
    elements.append(opticalElement.FlatMirror([x_, y_], 45, 100, {'color': BLACK}))


def add_curved_mirror():
    x_, y_, _, _ = screen_map_inv(mousePos)
    elements.append(opticalElement.CurvedMirror([x_, y_], 45, [100, 1000], {'color': BLACK}))


# -------- Ray Tracing ---------------

# noinspection PyPep8Naming
def ray_trace():
    output_rays = [rays]

    for i in range(0, MAX_BOUNCE):
        newRays = []
        # print("i = %d" % i)
        for r in output_rays[-1]:
            r: dict[str, None]
            minDist = np.inf
            closestElem = None
            closestIntersect = None
            for elem in elements:
                intersect = elem.rayIntersection(r['pos'], r['dir'])
                print(intersect)
                if intersect is None:
                    continue
                dist = np.linalg.norm(intersect - r['pos'])
                if dist < .0001:
                    continue
                #                if(closestElem is not None and elem == closestElem):
                #                    continue
                if minDist > dist:
                    minDist = dist
                    closestElem = elem
                    closestIntersect = intersect
            if closestElem is not None:
                dir_new = closestElem.reflect(r['pos'], r['dir'], closestIntersect)
                dir_new = dir_new / np.linalg.norm(dir_new)
                r['intersect'] = closestIntersect
                if 'color' in r:
                    newRays.append({'pos': closestIntersect, 'dir': dir_new, 'color': r['color']})
                else:
                    newRays.append({'pos': closestIntersect, 'dir': dir_new, 'color': r['color']})
            else:
                r['intersect'] = None
        if len(newRays) != 0:
            output_rays.append(newRays)
    return output_rays


def ray_sim():
    global mousePos, coord_lims
    pygame.init()

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    zoom_factor = 1.3
    pygame.display.set_caption("Ray Tracer")

    # Loop until the user clicks the close button.
    end = False

    theta = 0
    rays.append(
        {'pos': np.array([-1000, 710]), 'dir': np.array([np.cos(np.pi * theta / 180), np.sin(np.pi * theta / 180)]),
         'color': RED})
    theta = 0.2
    rays.append(
        {'pos': np.array([-1000, 710]), 'dir': np.array([np.cos(np.pi * theta / 180), np.sin(np.pi * theta / 180)]),
         'color': GREEN})
    theta = -0.2
    rays.append(
        {'pos': np.array([-1000, 710]), 'dir': np.array([np.cos(np.pi * theta / 180), np.sin(np.pi * theta / 180)]),
         'color': BLUE})

    # ------------Right Click Menu Functions-----------------------

    menu_entries = ['Flat Mirror', 'Curved Mirror']
    right_click_menu = Menu([0, 0], menu_entries, rightClick=True, activated=False)
    right_click_menu.assignFunction(0, add_flat_mirror)
    right_click_menu.assignFunction(1, add_curved_mirror)
    # -------- Main program loop---------------

    # Keep track of mouse manipulations
    mouse_selection_element_index: int | None = None
    mouse_near_element_index = None

    rotating_element_index = None
    scaling_element_index = None

    view_drag_mouse_start = None
    view_drag_c_start = None

    while not end:
        for event in pygame.event.get():  # Handle events
            right_click_menu.processMouseInput(event)
            if event.type == pygame.QUIT:
                print("User asked to quit.")
            # --------Keyboard Events---------------
            elif event.type == pygame.KEYDOWN:
                print(event)
                x, y, _, _ = screen_map_inv(mousePos)
                if event.unicode == 'n':
                    elements.append(opticalElement.FlatMirror(np.array([x, y]), -45, 100, {'color': BLACK}))
                elif event.unicode == '\x08':  # Backspace
                    if len(elements) > 0:
                        del elements[-1]
                elif event.unicode == 'r':  # Rotate
                    rotating_element_index = mouse_near_element_index
                elif event.unicode == 's':  # Scale
                    scaling_element_index = mouse_near_element_index
                elif event.unicode == '0':  # Reset View
                    coord_lims = coord_lims_default
                elif event.unicode == 'd':
                    if mouse_near_element_index is not None:
                        del elements[mouse_near_element_index]
                        mouse_near_element_index = None
                elif event.key == 282:
                    coord_lims = np.array(coord_lims) * 2
                elif event.key == 283:
                    coord_lims = np.array(coord_lims) / 2
                elif event.key == 276:  # Left Arrow
                    coord_lims = np.array(coord_lims) - (coord_lims[0][1] - coord_lims[0][0]) / 10 * np.array(
                        [[1.0, 1.0], [0.0, 0.0]])
                elif event.key == 275:  # Right Arrow
                    coord_lims = np.array(coord_lims) + (coord_lims[0][1] - coord_lims[0][0]) / 10 * np.array(
                        [[1.0, 1.0], [0.0, 0.0]])
                elif event.key == 273:  # Up Arrow
                    coord_lims = np.array(coord_lims) - (coord_lims[1][1] - coord_lims[1][0]) / 10 * np.array(
                        [[0.0, 0.0], [1.0, 1.0]])
                elif event.key == 274:  # Down Arrow
                    coord_lims = np.array(coord_lims) + (coord_lims[1][1] - coord_lims[1][0]) / 10 * np.array(
                        [[0.0, 0.0], [1.0, 1.0]])
            elif event.type == pygame.KEYUP:
                print("User let go of a key.")

            # -------Mouse Events--------
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Mouse click events
                print(event)
                mousePos = np.array(pygame.mouse.get_pos())
                if event.button == 1:
                    for i in range(0, len(elements)):
                        if elements[i].checkIfMouseNear(mousePos, screen_map_function):
                            print("Grabbed element %d" % i)
                            mouse_selection_element_index = i
                    if mouse_selection_element_index is None:
                        x, y, scale_x, scale_y = screen_map_inv(mousePos)
                        view_drag_mouse_start = np.array([x, y])
                        view_drag_c_start = copy.deepcopy(coord_lims)
                elif event.button == 3:
                    continue

                elif event.button == 4:
                    x, y, scale_x, scale_y = screen_map_inv(mousePos)
                    coord_lims[0][0] = (coord_lims[0][0] - x) * zoom_factor + x
                    coord_lims[0][1] = (coord_lims[0][1] - x) * zoom_factor + x
                    coord_lims[1][0] = (coord_lims[1][0] + y) * zoom_factor - y
                    coord_lims[1][1] = (coord_lims[1][1] + y) * zoom_factor - y
                elif event.button == 5:
                    x, y, scale_x, scale_y = screen_map_inv(mousePos)
                    coord_lims[0][0] = (coord_lims[0][0] - x) / zoom_factor + x
                    coord_lims[0][1] = (coord_lims[0][1] - x) / zoom_factor + x
                    coord_lims[1][0] = (coord_lims[1][0] + y) / zoom_factor - y
                    coord_lims[1][1] = (coord_lims[1][1] + y) / zoom_factor - y
                rotating_element_index = None
                scaling_element_index = None

            elif event.type == pygame.MOUSEMOTION:  # Mouse movement events
                mousePos = np.array(pygame.mouse.get_pos())
                # print(mousePos)
                # print(mouse_selection_element_index)
                x, y, scale_x, scale_y = screen_map_inv(mousePos)
                if mouse_selection_element_index is not None:
                    mouse_selection_element_index: int
                    new_pos = np.array([x, y])
                    print("Dragging element %d to pos " % mouse_selection_element_index + str(new_pos))
                    elements[mouse_selection_element_index].pos = new_pos
                elif rotating_element_index is not None:
                    rel_vect = np.array([x, y]) - elements[rotating_element_index].pos
                    new_angle = np.arctan2(rel_vect[1], rel_vect[0])
                    elements[rotating_element_index].setOrientation(180 * new_angle / np.pi)
                elif scaling_element_index is not None:
                    rel_vect = np.array([x, y]) - elements[scaling_element_index].pos
                    new_scale = np.linalg.norm([rel_vect[1], rel_vect[0]])
                    if elements[scaling_element_index].elementType() == 'FlatMirror':
                        elements[scaling_element_index].boundaries = new_scale
                    elif elements[scaling_element_index].elementType() == 'CurvedMirror':
                        elements[scaling_element_index].boundaries[0] = new_scale

                elif view_drag_mouse_start is not None:
                    drag_vect = np.array([x, y]) - view_drag_mouse_start
                    coord_lims = view_drag_c_start + np.array([[-drag_vect[0]] * 2, [drag_vect[1]] * 2]) / 1.2

                else:
                    mouse_near_element_index = None
                    for i in range(0, len(elements)):
                        mousePos = np.array(pygame.mouse.get_pos())
                        if elements[i].checkIfMouseNear(mousePos, screen_map_function):
                            mouse_near_element_index = i

            elif event.type == pygame.MOUSEBUTTONUP:  # Mouse release event
                mousePos = np.array(pygame.mouse.get_pos())
                print(mousePos)
                print(mouse_selection_element_index)
                if mouse_selection_element_index is not None:
                    mouse_selection_element_index: int
                    x, y, _, _ = screen_map_inv(mousePos)
                    print("Moved element %d from " % mouse_selection_element_index + str(
                        elements[mouse_selection_element_index].pos) + " to pos " + str(mousePos))
                    elements[mouse_selection_element_index].pos = np.array([x, y])
                mouse_selection_element_index = None
                view_drag_mouse_start = None

                # Handle window close
            if event.type == pygame.QUIT:  # If user clicked close
                end = True  # Flag that we are done so we exit this loop

        output_rays = ray_trace()

        # ----------------Drawing code should go here------------

        # Clear screen
        screen.fill(WHITE)

        # Draw the optical elements
        for i in range(0, len(elements)):
            if mouse_near_element_index is not None and mouse_near_element_index == i:
                elements[i].drawSelected(screen, screen_map_function)
            else:
                elements[i].draw(screen, screen_map_function)

        # Draw the rays
        for i in range(0, len(output_rays)):
            for j in range(0, len(output_rays[i])):
                x1, y1, _, _ = screen_map_function(output_rays[i][j]['pos'])
                if 'intersect' in output_rays[i][j] and output_rays[i][j]['intersect'] is not None:
                    x2, y2, _, _ = screen_map_function(output_rays[i][j]['intersect'])
                else:
                    x2, y2, _, _ = screen_map_function(
                        output_rays[i][j]['pos'] + output_rays[i][j]['dir'] * (np.max(coord_lims) - np.min(coord_lims)))
                if 'color' in output_rays[i][j]:
                    pygame.draw.line(screen, output_rays[i][j]['color'], [x1, y1], [x2, y2], 2)
                else:
                    pygame.draw.line(screen, RED, [x1, y1], [x2, y2], 2)

        right_click_menu.draw(screen)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 60 frames per second
        clock.tick(60)

    # Exit thread after loop has been exited
    pygame.quit()


def get_ray_start_p(rect_size):
    dx = rect_size[0]
    dy = rect_size[1]
    diameter = math.sqrt(dx ** 2 + dy ** 2)
    radius = diameter
    # radius=2*(diameter/2)
    # 1 start point per 5°
    points_list = []
    for i in range(int(360 / 5)):
        point = (round(np.cos(5 * i * np.pi / 180) * radius), round(np.sin(5 * i * np.pi / 180) * radius))
        point = list(point)
        point[0] += round(rect_size[0] / 2)
        point[1] += round(rect_size[1] / 2)
        point[1] = rect_size[1] - point[1]
        points_list.append(tuple(point))
    # center is 1/2 rect_size
    return points_list, radius


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
    p_list, rad = get_ray_start_p(canvas_size_pixel)
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
        ray_scan(p_list[r_sp_index], 90 - 5 * r_sp_index)
        r_sp_index += 1
        if r_sp_index >= len(p_list):
            r_sp_index = 0
        output_rays = ray_trace()
        screen.fill(WHITE)
        for p in vert:
            pygame.draw.circle(screen, RED, p, 2)
        for p in p_list:
            pygame.draw.circle(screen, BLUE, p, 2)
        for i in range(0, len(elements)):
            direct_draw_line(elements[i])
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
