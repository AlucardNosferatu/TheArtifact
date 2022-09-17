#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# noinspection SpellCheckingInspection
"""
Created on Sun Nov 25 16:15:36 2018

@author: jaymz
"""

import copy

import numpy as np
import pygame

from RayTracer import opticalElement
from RayTracer.menu import Menu
from RayTracer.opticalElement import FlatMirror, CurvedMirror

pygame.init()

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

PI = np.pi

size = (700, 700)
screen = pygame.display.set_mode(size)

coord_lims_default = np.array([[-1000.0, 1000.0], [-1000.0, 1000.0]])
coord_lims = coord_lims_default

MAX_BOUNCE = 100

ZOOM_FACTOR = 1.3


def screen_map_function(pos):
    rangeX = abs(coord_lims[0][0] - coord_lims[0][1])
    rangeY = abs(coord_lims[1][0] - coord_lims[1][1])
    scale_x = float(size[0]) / rangeX
    scale_y = float(size[1]) / rangeY
    return (
        int((pos[0] - coord_lims[0][0]) / rangeX * size[0]), int((-pos[1] - coord_lims[1][0]) / rangeY * size[1]),
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


pygame.display.set_caption("Ray Tracer")

# Loop until the user clicks the close button.
done = False

elements: list[FlatMirror | CurvedMirror] = []
rays = []

theta = 0
rays.append({'pos': np.array([-1000, 710]), 'dir': np.array([np.cos(np.pi * theta / 180), np.sin(np.pi * theta / 180)]),
             'color': RED})
theta = 0.2
rays.append({'pos': np.array([-1000, 710]), 'dir': np.array([np.cos(np.pi * theta / 180), np.sin(np.pi * theta / 180)]),
             'color': GREEN})
theta = -0.2
rays.append({'pos': np.array([-1000, 710]), 'dir': np.array([np.cos(np.pi * theta / 180), np.sin(np.pi * theta / 180)]),
             'color': BLUE})

# ------------Right Click Menu Functions-----------------------

menuEntries = ['Flat Mirror', 'Curved Mirror']
rightClickMenu = Menu([0, 0], menuEntries, rightClick=True, activated=False)


def add_flat_mirror():
    x_, y_, _, _ = screen_map_inv(mousePos)
    elements.append(opticalElement.FlatMirror([x_, y_], 45, 100, {'color': BLACK}))


def add_curved_mirror():
    x_, y_, _, _ = screen_map_inv(mousePos)
    elements.append(opticalElement.CurvedMirror([x_, y_], 45, [100, 1000], {'color': BLACK}))


rightClickMenu.assignFunction(0, add_flat_mirror)
rightClickMenu.assignFunction(1, add_curved_mirror)


# -------- Ray Tracing ---------------

def ray_trace():
    output_rays = [rays]

    for i_ in range(0, MAX_BOUNCE):
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


# -------- Main program loop---------------

# Keep track of mouse manipulations
mouseSelection_elementIndex: int | None = None
mouseNear_elementIndex = None

rotating_elementIndex = None
scaling_elementIndex = None

viewDrag_mouseStart = None
viewDrag_c_start = None
mousePos = None
while not done:
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
            done = True  # Flag that we are done so we exit this loop

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
