# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 16:25:38 2022

@author: Ted
"""
import math

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

from WindTunnel.lbm import pylbm


# 逆时针旋转
def n_rotate(angle, value_x, value_y, point_x, point_y):
    value_x = np.array(value_x)
    value_y = np.array(value_y)
    n_rotate_x = (value_x - point_x) * math.cos(angle) - (value_y - point_y) * math.sin(angle) + point_x
    n_rotate_y = (value_x - point_x) * math.sin(angle) + (value_y - point_y) * math.cos(angle) + point_y
    return round(n_rotate_x, 2), round(n_rotate_y, 2)


# 顺时针旋转
def s_rotate(angle, value_x, value_y, point_x, point_y):
    value_x = np.array(value_x)
    value_y = np.array(value_y)
    s_rotate_x = (value_x - point_x) * math.cos(angle) + (value_y - point_y) * math.sin(angle) + point_x
    s_rotate_y = (value_y - point_y) * math.cos(angle) - (value_x - point_x) * math.sin(angle) + point_y
    return s_rotate_x, s_rotate_y


def load_img(fn_img=r'WindTunnel/content/car.png'):
    return cv2.cvtColor(cv2.imread(fn_img), cv2.COLOR_BGR2GRAY)


def conv_vert(body, vert_list=False):
    px_ratio = 64
    if vert_list:
        vert = body
    else:
        vert = body.fixtures[0].shape.vertices
    max_x = vert[0][0]
    max_y = vert[0][1]
    min_x = vert[0][0]
    min_y = vert[0][1]
    for v in vert:
        if v[0] > max_x:
            max_x = v[0]
        elif v[0] < min_x:
            min_x = v[0]
        if v[1] > max_y:
            max_y = v[1]
        elif v[1] < min_y:
            min_y = v[1]
    canvas_size = (
        max_x - min_x,
        max_y - min_y
    )
    canvas_size_pixel = (
        int(canvas_size[0] * px_ratio) + 1,
        int(canvas_size[1] * px_ratio) + 1
    )
    canvas_offset = [
        canvas_size[0] * 0.5 + min_x,
        canvas_size[1] * 0.5 + min_y
    ]
    center_offset = [int(0.5 * c) for c in canvas_size_pixel]

    for i, t in enumerate(vert):
        t = list(t)
        t = [
            t[0] - canvas_offset[0],
            t[1] - canvas_offset[1]
        ]
        t = [c * px_ratio for c in t]
        t[0] += center_offset[0]
        t[1] += center_offset[1]
        t[1] = canvas_size_pixel[1] - t[1]
        t = tuple(t)
        vert[i] = t
    return vert, canvas_size_pixel


def draw_poly(vert, canvas_size):
    empty_canvas = Image.new('L', canvas_size, 'white')
    drawObject = ImageDraw.Draw(empty_canvas)
    drawObject.polygon(vert, fill="black", outline="black")
    # noinspection PyTypeChecker
    return np.array(empty_canvas)


def scale2lattices(array, rescale=False):
    L_car = 7 * 25.4
    if rescale:
        scale = .5
        # rescale if necessary
        if scale != 1:
            t_dim = (int(array.shape[1] * scale), int(array.shape[0] * scale))
            array = cv2.resize(array, t_dim, interpolation=cv2.INTER_AREA)
        p_size = L_car / array.shape[1]
    else:
        # fixed car resolution
        LB_car = 300
        f = LB_car / array.shape[1]
        t_dim = (int(array.shape[1] * f), int(array.shape[0] * f))
        array = cv2.resize(array, t_dim, interpolation=cv2.INTER_CUBIC)
        p_size = L_car / array.shape[1]
    array = (array < 127).astype(int)
    return array, p_size


def pad_shape(array, p_size):
    pad = {'left': 50, 'right': 50, 'top': 25, 'bottom': 25}
    padded = np.pad(array, [(int(pad['top'] / p_size), int(pad['bottom'] / p_size)),
                            (int(pad['left'] / p_size), int(pad['right'] / p_size))], 'constant', constant_values=0)
    return padded


def update_drag(self):
    nu = 1 / 6
    # fluid points just left of the car
    kL = np.where(np.roll(self.padded, (0, -1), axis=(0, 1)) > self.padded)
    kR = np.where(np.roll(self.padded, (0, 1), axis=(0, 1)) > self.padded)
    kU = np.where(np.roll(self.padded, (-1, 0), axis=(0, 1)) > self.padded)
    kB = np.where(np.roll(self.padded, (1, 0), axis=(0, 1)) > self.padded)
    # normal forces
    P = self.fields['rho'][0, :, :, 0] / 3
    fxN = sum(P[kL]) - sum(P[kR])
    fyN = sum(P[kU]) - sum(P[kB])

    # tangential drag force, tau=mu*du/dy|y=0; Fd=tau*area
    vy = self.fields['v'][0, :, :, 1]
    vx = self.fields['v'][0, :, :, 2]
    # since velocity=0 at 0
    # -- drag along horizontal surfaces; tau=(nu*1)*((vx-0)/1)
    tauB = nu * vx[kB]
    fxB = sum(tauB)
    tauU = nu * vx[kU]
    fxU = sum(tauU)
    # -- lift along horizontal surfaces
    tauL = nu * 1 * vy[kL]
    fyL = sum(tauL)
    tauR = nu * 1 * vy[kR]
    fyR = sum(tauR)

    self.hist['step'].append(self.step)
    self.hist['fxN'].append(fxN)
    self.hist['fxB'].append(fxB)
    self.hist['fxU'].append(fxU)
    self.hist['fx'].append(fxN + fxB + fxU)

    self.hist['fyN'].append(fyN)
    self.hist['fyL'].append(fyL)
    self.hist['fyR'].append(fyR)
    self.hist['fy'].append(fyN + fyL + fyR)


def my_plot(self):
    mx, my = np.meshgrid(range(self.padded.shape[1]), range(self.padded.shape[0]))
    # velocity
    v = self.fields['v'][0]
    vx = v[..., 2]
    vy = v[..., 1]
    v_mag = ((v ** 2).sum(axis=-1)) ** 0.5

    # -- for display
    v_mag[np.where(self.padded == 1)] = v_mag.max()

    # calc drag
    P = self.fields['rho'][0, :, :, 0] / 3
    fx = self.hist['fx'][-1]
    fy = self.hist['fy'][-1]
    # -- for display
    P[np.where(self.padded == 1)] = P.min()

    # display
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.imshow(v_mag)
    plt.axis('off')
    ttl = 'Velocity (time=%d): dv-max: %.3g' % (self.step, self.hist['dv_max'][-1])
    plt.title(ttl)
    plt.colorbar()
    plt.streamplot(mx, my, vx, vy, color='r', density=.8)

    plt.subplot(2, 1, 2)
    plt.imshow(P)
    plt.axis('off')
    ttl = 'Pressure: fx=%.3g, fy=%.3g' % (fx, fy)
    plt.title(ttl)
    plt.colorbar()
    plt.streamplot(mx, my, vx, vy, color='r', density=.8)
    plt.tight_layout()

    # plt.savefig(fn_out, dpi=200)
    plt.show()

    # diagnostic
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.plot(self.hist['step'], self.hist['dv_max'])
    plt.xlabel('step')
    plt.ylabel(r'$\Delta$$v_{max}$')
    plt.title('Convergence')
    plt.yscale('log')

    plt.subplot(1, 3, 2)
    plt.plot(self.hist['step'], self.hist['fx'], label='fx-total', linewidth=3)
    plt.plot(self.hist['step'], self.hist['fxN'], label='fx-normal')
    plt.plot(self.hist['step'], self.hist['fxB'], label='fx-bottom')
    plt.plot(self.hist['step'], self.hist['fxU'], label='fx-top')
    plt.xlabel('step')
    plt.ylabel('fx')
    plt.title('Force-X')
    plt.legend()

    plt.subplot(1, 3, 3)
    plt.plot(self.hist['step'], self.hist['fy'], label='fy-total', linewidth=3)
    plt.plot(self.hist['step'], self.hist['fyN'], label='fy-normal')
    plt.plot(self.hist['step'], self.hist['fyL'], label='fy-left')
    plt.plot(self.hist['step'], self.hist['fyR'], label='fy-right')
    plt.xlabel('step')
    plt.ylabel('fy')
    plt.title('Force-Y')
    plt.legend()

    plt.tight_layout()
    # plt.savefig(fn_out2, dpi=200)
    plt.show()


def cb_vel(self):
    # vx,vy for left wall
    self.fields['v'][0, :, 0, 1] = 0
    self.fields['v'][0, :, 0, 2] = .1
    self.fields['v'][0, -1, :, :] = self.fields['v'][0, -2, :, :]  # open-bottom
    self.fields['v'][0, :, -1, :] = self.fields['v'][0, :, -2, :]  # open-right
    self.fields['v'][0, 0, :, :] = self.fields['v'][0, 1, :, :]  # open-top
    dv = (((self.fields['v'] - self.V_old) ** 2).sum(axis=-1)) ** 0.5
    max_dv = dv.max()
    # print('max-dv: %.3g' % (max_dv,))
    self.V_old = self.fields['v'].copy()
    self.hist['dv_max'].append(max_dv)
    update_drag(self)
    # if (self.step > 0) and (self.step % 100 == 0):
    #     my_plot(self)


def cb_get_final_result(self):
    # print('Step:', self.step)
    if self.step == self.total_steps - 1:
        # my_plot(self)
        drag = self.hist['fx'][-1]
        lift = self.hist['fy'][-1]
        print('lift:', lift, 'drag:', drag)


if __name__ == '__main__':
    a = load_img(fn_img='airfoil.png')
    a, pixel_size = scale2lattices(a)
    M = pad_shape(a, pixel_size)
    S = pylbm.LBM((1, *M.shape))
    S.padded = M
    S.fields['ns'][0, :, :, 0] = S.padded  # car

    # track how the velocity profile changes
    S.V_old = S.fields['v'].copy()
    S.hist = {'dv_max': [], 'fx': [], 'fy': [], 'step': [],
              'fxN': [], 'fyN': [], 'fxU': [], 'fxB': [], 'fyL': [], 'fyR': []}

    cb = {'postMacro': [cb_vel]}

    S.sim(steps=1000, callbacks=cb)
