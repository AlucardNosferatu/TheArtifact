import cv2
import numpy as np

from Config import map_width, map_height


def compose_map():
    w = map_width
    h = map_height
    terrain = []
    row = []
    cave_f_alt = 0
    cave_c_alt = 0
    surface_alt = 32
    for i in range(w):
        row.append([cave_f_alt, cave_c_alt, surface_alt])
    for _ in range(h):
        terrain.append(row.copy())
    terrain = np.array(terrain).astype(dtype=np.uint8)
    center = [int(0.5 * w), int(0.5 * h)]
    terrain = cv2.fillPoly(
        img=terrain,
        pts=np.array(
            [
                [
                    (center[0] - 2, center[1] - 14), (center[0] + 2, center[1] - 14),
                    (center[0] + 2, center[1] + 14), (center[0] - 2, center[1] + 14)
                ]
            ]
        ),
        color=(0, 0, 40)
    )
    terrain = cv2.fillPoly(
        img=terrain,
        pts=np.array(
            [
                [
                    (center[0] - 2, center[1] - 12), (center[0] + 2, center[1] - 12),
                    (center[0] + 2, center[1] + 12), (center[0] - 2, center[1] + 12)
                ]
            ]
        ),
        color=(0, 0, 48)
    )
    terrain = cv2.fillPoly(
        img=terrain,
        pts=np.array(
            [
                [
                    (center[0] - 2, center[1] - 10), (center[0] + 2, center[1] - 10),
                    (center[0] + 2, center[1] + 10), (center[0] - 2, center[1] + 10)
                ]
            ]
        ),
        color=(0, 0, 56)
    )
    terrain = cv2.fillPoly(
        img=terrain,
        pts=np.array(
            [
                [
                    (center[0] - 2, center[1] - 8), (center[0] + 2, center[1] - 8),
                    (center[0] + 2, center[1] + 8), (center[0] - 2, center[1] + 8)
                ]
            ]
        ),
        color=(0, 0, 64)
    )
    terrain = cv2.fillPoly(
        img=terrain,
        pts=np.array(
            [
                [
                    (center[0] - 2, center[1] - 6), (center[0] + 2, center[1] - 6),
                    (center[0] + 2, center[1] + 6), (center[0] - 2, center[1] + 6)
                ]
            ]
        ),
        color=(0, 0, 72)
    )
    terrain = cv2.fillPoly(
        img=terrain,
        pts=np.array(
            [
                [
                    (center[0] - 2, center[1] - 4), (center[0] + 2, center[1] - 4),
                    (center[0] + 2, center[1] + 4), (center[0] - 2, center[1] + 4)
                ]
            ]
        ),
        color=(0, 0, 80)
    )
    terrain = cv2.fillPoly(
        img=terrain,
        pts=np.array(
            [
                [
                    (center[0] - 2, center[1] - 2), (center[0] + 2, center[1] - 2),
                    (center[0] + 2, center[1] + 2), (center[0] - 2, center[1] + 2)
                ]
            ]
        ),
        color=(32, 64, 80)
    )
    return terrain


if __name__ == '__main__':
    t = compose_map()
    cv2.imshow('terrain', t)
    cv2.waitKey()
