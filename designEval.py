# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 16:25:38 2022

@author: Ted
"""
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
from WindTunnel.lbm import pylbm


def load_img(fn_img=r'WindTunnel/content/car.png'):
    return cv2.cvtColor(cv2.imread(fn_img), cv2.COLOR_BGR2GRAY)


def preprocess(array, rescale=False):
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
        array = cv2.resize(array, t_dim, interpolation=cv2.INTER_AREA)
        p_size = L_car / array.shape[1]
    array = (array < 127).astype(int)
    return array, p_size


def pad_shape(array, p_size):
    pad = {'left': 75, 'right': 75, 'top': 50, 'bottom': 50}
    padded = np.pad(array, [(int(pad['top'] / p_size), int(pad['bottom'] / p_size)),
                            (int(pad['left'] / p_size), int(pad['right'] / p_size))], 'constant', constant_values=0)
    return padded


def drag(self, padded):
    nu = 1 / 6
    # fluid points just left of the car
    kL = np.where(np.roll(padded, (0, -1), axis=(0, 1)) > padded)
    kR = np.where(np.roll(padded, (0, 1), axis=(0, 1)) > padded)
    kU = np.where(np.roll(padded, (-1, 0), axis=(0, 1)) > padded)
    kB = np.where(np.roll(padded, (1, 0), axis=(0, 1)) > padded)
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
    return P


def my_plot(self, padded):
    mx, my = np.meshgrid(range(padded.shape[1]), range(padded.shape[0]))
    # velocity
    v = self.fields['v'][0]
    vx = v[..., 2]
    vy = v[..., 1]
    v_mag = ((v ** 2).sum(axis=-1)) ** 0.5

    # -- for display
    v_mag[np.where(padded == 1)] = v_mag.max()

    # velocity difference
    dv = (((self.fields['v'] - self.V_old) ** 2).sum(axis=-1)) ** 0.5
    max_dv = dv.max()
    print('step: %d, max-dv: %.3g' % (self.step, max_dv))
    self.V_old = self.fields['v'].copy()
    self.hist['dv_max'].append(max_dv)

    if max_dv < self.dv_to_l:
        sys.exit()

    # calc drag
    P = drag(self, padded)
    fx = self.hist['fx'][-1]
    fy = self.hist['fy'][-1]
    # -- for display
    P[np.where(padded == 1)] = P.min()

    # display
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.imshow(v_mag)
    plt.axis('off')
    ttl = 'Velocity (time=%d): dv-max: %.3g' % (self.step, max_dv)
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
    self.fields['v'][0, :, 0, 2] = 1

    self.fields['v'][0, -1, :, :] = self.fields['v'][0, -2, :, :]   # open-bottom
    self.fields['v'][0, :, -1, :] = self.fields['v'][0, :, -2, :]   # open-right
    self.fields['v'][0, 0, :, :] = self.fields['v'][0, 1, :, :]     # open-top
    padded = self.padded
    if self.step % 10 == 0:
        dv = (((self.fields['v'] - self.V_old) ** 2).sum(axis=-1)) ** 0.5
        max_dv = dv.max()
        # noinspection PyUnusedLocal
        P = drag(self, padded)
        # self.hist['step'].append(self.step)
        # self.hist['fx'].append(fx)
        # self.hist['fy'].append(fy)
        self.hist['dv_max'].append(max_dv)

    if (self.step > 0) and (self.step % 100 == 0):
        my_plot(self, padded)


a = load_img(fn_img='airfoil.png')
a, pixel_size = preprocess(a)
M = pad_shape(a, pixel_size)
S = pylbm.LBM((1, *M.shape))
S.padded = M
S.fields['ns'][0, :, :, 0] = S.padded  # car

# track how the velocity profile changes
S.V_old = S.fields['v'].copy()
S.hist = {'dv_max': [], 'fx': [], 'fy': [], 'step': [],
          'fxN': [], 'fyN': [], 'fxU': [], 'fxB': [], 'fyL': [], 'fyR': []}
S.dv_to_l = 5e-4

cb = {'postMacro': [cb_vel]}

S.sim(steps=1000, callbacks=cb)
