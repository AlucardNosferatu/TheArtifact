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
from RayTracer.opticalElement import FlatMirror, CurvedMirror

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


def direct_draw(element):
    color = BLUE
    screenX, screenY, scaleX, scaleY = element.pos[0], element.pos[1], 1, 1
    angleRad = element.orientation * np.pi / 180
    if isinstance(element.properties, dict):
        color = element.properties['color']
    x1, y1 = element.boundaries * np.cos(angleRad) * scaleX + screenX, element.boundaries * np.sin(
        angleRad) * scaleY + screenY
    x2, y2 = -element.boundaries * np.cos(angleRad) * scaleX + screenX, -element.boundaries * np.sin(
        angleRad) * scaleY + screenY
    pygame.draw.line(screen, color, [x1, y1], [x2, y2], 7)


def screen_map_function(pos):
    rangeX = abs(coord_lims[0][0] - coord_lims[0][1])
    rangeY = abs(coord_lims[1][0] - coord_lims[1][1])
    scale_x = float(size[0]) / rangeX
    scale_y = float(size[1]) / rangeY
    return (
        int((pos[0] - coord_lims[0][0]) / rangeX * size[0]),
        int((-pos[1] - coord_lims[1][0]) / rangeY * size[1]),
        scale_x,
        scale_y)


def screen_map_inv(pos_screen):
    rangeX = abs(coord_lims[0][0] - coord_lims[0][1])
    rangeY = abs(coord_lims[1][0] - coord_lims[1][1])
    scale_x = float(size[0]) / rangeX
    scale_y = float(size[1]) / rangeY
    return (
        int((pos_screen[0] / size[0] * rangeX + coord_lims[0][0])),
        int(-pos_screen[1] * rangeY / size[1] - coord_lims[1][0]),
        scale_x, scale_y)


def add_flat_mirror():
    x_, y_, _, _ = screen_map_inv(mousePos)
    elements.append(opticalElement.FlatMirror([x_, y_], 45, 100, {'color': BLACK}))


def add_curved_mirror():
    x_, y_, _, _ = screen_map_inv(mousePos)
    elements.append(opticalElement.CurvedMirror([x_, y_], 45, [100, 1000], {'color': BLACK}))


# -------- Ray Tracing ---------------

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
                # print(intersect)
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

    ZOOM_FACTOR = 1.3
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

    menuEntries = ['Flat Mirror', 'Curved Mirror']
    rightClickMenu = Menu([0, 0], menuEntries, rightClick=True, activated=False)
    rightClickMenu.assignFunction(0, add_flat_mirror)
    rightClickMenu.assignFunction(1, add_curved_mirror)
    # -------- Main program loop---------------

    # Keep track of mouse manipulations
    mouseSelection_elementIndex: int | None = None
    mouseNear_elementIndex = None

    rotating_elementIndex = None
    scaling_elementIndex = None

    viewDrag_mouseStart = None
    viewDrag_c_start = None

    while not end:
        for event in pygame.event.get():  # Handle events
            rightClickMenu.processMouseInput(event)
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
                    rotating_elementIndex = mouseNear_elementIndex
                elif event.unicode == 's':  # Scale
                    scaling_elementIndex = mouseNear_elementIndex
                elif event.unicode == '0':  # Reset View
                    coord_lims = coord_lims_default
                elif event.unicode == 'd':
                    if mouseNear_elementIndex is not None:
                        del elements[mouseNear_elementIndex]
                        mouseNear_elementIndex = None
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
                            mouseSelection_elementIndex = i
                    if mouseSelection_elementIndex is None:
                        x, y, scaleX, scaleY = screen_map_inv(mousePos)
                        viewDrag_mouseStart = np.array([x, y])
                        viewDrag_c_start = copy.deepcopy(coord_lims)
                elif event.button == 3:
                    continue

                elif event.button == 4:
                    x, y, scaleX, scaleY = screen_map_inv(mousePos)
                    coord_lims[0][0] = (coord_lims[0][0] - x) * ZOOM_FACTOR + x
                    coord_lims[0][1] = (coord_lims[0][1] - x) * ZOOM_FACTOR + x
                    coord_lims[1][0] = (coord_lims[1][0] + y) * ZOOM_FACTOR - y
                    coord_lims[1][1] = (coord_lims[1][1] + y) * ZOOM_FACTOR - y
                elif event.button == 5:
                    x, y, scaleX, scaleY = screen_map_inv(mousePos)
                    coord_lims[0][0] = (coord_lims[0][0] - x) / ZOOM_FACTOR + x
                    coord_lims[0][1] = (coord_lims[0][1] - x) / ZOOM_FACTOR + x
                    coord_lims[1][0] = (coord_lims[1][0] + y) / ZOOM_FACTOR - y
                    coord_lims[1][1] = (coord_lims[1][1] + y) / ZOOM_FACTOR - y
                rotating_elementIndex = None
                scaling_elementIndex = None

            elif event.type == pygame.MOUSEMOTION:  # Mouse movement events
                mousePos = np.array(pygame.mouse.get_pos())
                # print(mousePos)
                # print(mouseSelection_elementIndex)
                x, y, scaleX, scaleY = screen_map_inv(mousePos)
                if mouseSelection_elementIndex is not None:
                    mouseSelection_elementIndex: int
                    newPos = np.array([x, y])
                    print("Dragging element %d to pos " % mouseSelection_elementIndex + str(newPos))
                    elements[mouseSelection_elementIndex].pos = newPos
                elif rotating_elementIndex is not None:
                    relVect = np.array([x, y]) - elements[rotating_elementIndex].pos
                    newAngle = np.arctan2(relVect[1], relVect[0])
                    elements[rotating_elementIndex].setOrientation(180 * newAngle / np.pi)
                elif scaling_elementIndex is not None:
                    relVect = np.array([x, y]) - elements[scaling_elementIndex].pos
                    newScale = np.linalg.norm([relVect[1], relVect[0]])
                    if elements[scaling_elementIndex].elementType() == 'FlatMirror':
                        elements[scaling_elementIndex].boundaries = newScale
                    elif elements[scaling_elementIndex].elementType() == 'CurvedMirror':
                        elements[scaling_elementIndex].boundaries[0] = newScale

                elif viewDrag_mouseStart is not None:
                    dragVect = np.array([x, y]) - viewDrag_mouseStart
                    coord_lims = viewDrag_c_start + np.array([[-dragVect[0]] * 2, [dragVect[1]] * 2]) / 1.2

                else:
                    mouseNear_elementIndex = None
                    for i in range(0, len(elements)):
                        mousePos = np.array(pygame.mouse.get_pos())
                        if elements[i].checkIfMouseNear(mousePos, screen_map_function):
                            mouseNear_elementIndex = i

            elif event.type == pygame.MOUSEBUTTONUP:  # Mouse release event
                mousePos = np.array(pygame.mouse.get_pos())
                print(mousePos)
                print(mouseSelection_elementIndex)
                if mouseSelection_elementIndex is not None:
                    mouseSelection_elementIndex: int
                    x, y, _, _ = screen_map_inv(mousePos)
                    print("Moved element %d from " % mouseSelection_elementIndex + str(
                        elements[mouseSelection_elementIndex].pos) + " to pos " + str(mousePos))
                    elements[mouseSelection_elementIndex].pos = np.array([x, y])
                mouseSelection_elementIndex = None
                viewDrag_mouseStart = None

                # Handle window close
            if event.type == pygame.QUIT:  # If user clicked close
                end = True  # Flag that we are done so we exit this loop

        outputRays = ray_trace()

        # ----------------Drawing code should go here------------

        # Clear screen
        screen.fill(WHITE)

        # Draw the optical elements
        for i in range(0, len(elements)):
            if mouseNear_elementIndex is not None and mouseNear_elementIndex == i:
                elements[i].drawSelected(screen, screen_map_function)
            else:
                elements[i].draw(screen, screen_map_function)

        # Draw the rays
        for i in range(0, len(outputRays)):
            for j in range(0, len(outputRays[i])):
                x1, y1, _, _ = screen_map_function(outputRays[i][j]['pos'])
                if 'intersect' in outputRays[i][j] and outputRays[i][j]['intersect'] is not None:
                    x2, y2, _, _ = screen_map_function(outputRays[i][j]['intersect'])
                else:
                    x2, y2, _, _ = screen_map_function(
                        outputRays[i][j]['pos'] + outputRays[i][j]['dir'] * (np.max(coord_lims) - np.min(coord_lims)))
                if 'color' in outputRays[i][j]:
                    pygame.draw.line(screen, outputRays[i][j]['color'], [x1, y1], [x2, y2], 2)
                else:
                    pygame.draw.line(screen, RED, [x1, y1], [x2, y2], 2)

        rightClickMenu.draw(screen)
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
        outputRays = ray_trace()
        screen.fill(WHITE)
        for p in vert:
            pygame.draw.circle(screen, RED, p, 2)
        for p in p_list:
            pygame.draw.circle(screen, BLUE, p, 2)
        for i in range(0, len(elements)):
            direct_draw(elements[i])
        for i_ in range(0, len(outputRays)):
            for j_ in range(0, len(outputRays[i_])):
                x1, y1 = outputRays[i_][j_]['pos']
                if 'intersect' in outputRays[i_][j_] and outputRays[i_][j_]['intersect'] is not None:
                    x2, y2 = outputRays[i_][j_]['intersect']
                else:
                    x2, y2 = outputRays[i_][j_]['pos'] + outputRays[i_][j_]['dir'] * (
                            np.max(coord_lims) - np.min(coord_lims))
                if 'color' in outputRays[i_][j_]:
                    pygame.draw.line(screen, outputRays[i_][j_]['color'], [x1, y1], [x2, y2], 1)
                else:
                    pygame.draw.line(screen, GREEN, [x1, y1], [x2, y2], 1)
        pygame.display.flip()
        c.tick(1)
    # Exit thread after loop has been exited
    pygame.quit()


if __name__ == '__main__':
    radar_cross_section()
