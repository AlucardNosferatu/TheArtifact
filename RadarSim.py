import math

import numpy as np
import pygame
from matplotlib import pyplot as plt

# from AeroSim import s_rotate
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
    stat_ = {}
    px_ratio = 16
    for i_, t in enumerate(src_b_):
        t = list(t)
        t = [
            t[0] * px_ratio,
            t[1] * px_ratio
        ]
        src_b_[i_] = tuple(t)
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
    for i_, t in enumerate(src_b_):
        t = list(t)
        t = [
            t[0] - rect_offset[0],
            t[1] - rect_offset[1],
        ]
        src_b_[i_] = tuple(t)
    radius = math.sqrt(rect_size[0] ** 2 + rect_size[1] ** 2)
    start_points = []
    start_orient = []
    for i_ in range(int(360 / 5)):
        ang = i_ * 5
        sp = (np.cos(ang * np.pi / 180) * radius, np.sin(ang * np.pi / 180) * radius)
        start_points.append(sp)
        start_orient.append(ang)
        stat_.__setitem__(ang, 0)
    return src_b_, start_points, start_orient, radius, stat_


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
        if 17 < i_ < 19:
            theta = 5 * i_ + ang_offset
            rays_.append(
                {
                    'pos': np.array(list(start_point)),
                    'dir': np.array([np.cos(np.pi * theta / 180), np.sin(np.pi * theta / 180)]),
                    'color': GREEN
                }
            )
    return rays_


def ray_trace(rays_, stat_):
    max_bounce = 10
    output_rays_ = [rays_]
    for i_ in range(0, max_bounce):
        new_rays = []
        for r in output_rays_[-1]:
            min_dist = np.inf
            closest_elem = None
            closest_intersect = None
            for elem in elements:
                if elem.elementType() == 'CurvedMirror' and r['color'] != RED:
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
                    stat_[closest_elem.orientation] += 1
                    dir_new = r['dir']
                    dir_new = dir_new / np.linalg.norm(dir_new)
                    r['intersect'] = closest_intersect
                    new_rays.append({'pos': closest_intersect, 'dir': dir_new, 'color': GREEN})
                else:
                    dir_new = closest_elem.reflect(r['pos'], r['dir'], closest_intersect)
                    dir_new = dir_new / np.linalg.norm(dir_new)
                    r['intersect'] = closest_intersect
                    if r['color'] != GREEN:
                        new_rays.append({'pos': closest_intersect, 'dir': dir_new, 'color': BLUE})
                    else:
                        new_rays.append({'pos': closest_intersect, 'dir': dir_new, 'color': RED})
            else:
                r['intersect'] = None
        if len(new_rays) != 0:
            output_rays_.append(new_rays)
    return output_rays_, stat_


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
# src_b = [
#     (-1, 2),
#     (1, 2),
#     (3, 2),
#     (5, -2),
#     (4, -4),
#     (2, -4),
#     (0, -4),
#     (-2, -4),
#     (-3, -2)
# ]
# src_b = [
#     (-1, 2),
#     (0, 0),
#     (1, 2),
#     (2, 0),
#     (3, 2),
#     (5, -2),
#     (4, -4),
#     (3, -2),
#     (2, -4),
#     (1, -2),
#     (0, -4),
#     (-1, -2),
#     (-2, -4),
#     (-3, -2)
# ]
# for n, t in enumerate(src_b):
#     point_x = t[0]
#     point_y = t[1]
#     s_point_x, s_point_y = s_rotate(math.radians(9 * 5), point_x, point_y, 0, 0)
#     src_b[n] = (s_point_x, s_point_y)
elements = []
canvas_size: None | tuple = None


def radar_cross_section(src_b_):
    global elements, canvas_size
    src_b_, sp_list, so_list, rad, stat = get_start_points(src_b_)
    elements = polygon_mirror(src_b_, elements)
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
        print('current orient:', so_list[r_sp_index])
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
            done = True
            data_length = len(stat)
            # 将极坐标根据数据长度进行等分
            angles = np.linspace(0, 2 * np.pi, data_length, endpoint=False)
            labels = [key for key in stat.keys()]
            score = [v for v in stat.values()]
            # 使雷达图数据封闭
            score_a = np.concatenate((score, [score[0]]))
            angles = np.concatenate((angles, [angles[0]]))
            labels = np.concatenate((labels, [labels[0]]))
            # 设置图形的大小
            plt.figure(figsize=(8, 6), dpi=100)
            # 新建一个子图
            ax = plt.subplot(111, polar=True)
            # 绘制雷达图
            ax.plot(angles, score_a, color='g')
            # 设置雷达图中每一项的标签显示
            ax.set_thetagrids(angles * 180 / np.pi, labels)
            # 设置雷达图的0度起始位置
            ax.set_theta_zero_location('E')
            # 设置雷达图的坐标刻度范围
            ax.set_rlim(0, max(stat.values()))
            # 设置雷达图的坐标值显示角度，相对于起始角度的偏移量
            ax.set_rlabel_position(270)
            ax.set_title("RCS Estimation")
            plt.show()

        output_rays, stat = ray_trace(rays, stat)
        screen.fill(WHITE)
        for p in src_b_:
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


if __name__ == '__main__':
    radar_cross_section(src_b)
