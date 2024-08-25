import threading
import time

import pygame

from Engine.Controller import EventController
from Engine.Renderer import Renderer


class Core:

    def __init__(self, screen_size=(1280, 720), fps=60, max_queue_size=64):
        self.icl_thread = None
        self.fps = fps
        self.screen_size = screen_size
        self.max_queue_size = max_queue_size
        self.queue_lock = threading.Lock()
        self.clock = pygame.time.Clock()
        self.params = {}  # 游戏机制的全局参数字典
        self.event_controller = None
        self.renderer = Renderer(screen_size=self.screen_size, core=self)  # 渲染器实例
        self.event_controller = EventController(self.max_queue_size)
        self.world_routine = []
        self.ui_routine = []
        self.routines = {'w': self.world_routine, 'u': self.ui_routine}
        self.recent_input = []
        self.last_tick = None

    def io_schedule(self):
        for routine_func in self.world_routine:
            spr_key, spr = routine_func(params=self.params, recent_input=self.recent_input)
            if spr_key is not None:
                self.renderer.world_draw[spr_key] = spr
        for routine_func in self.ui_routine:
            spr_key, spr = routine_func(params=self.params, recent_input=self.recent_input)
            if spr_key is not None:
                self.renderer.ui_draw[spr_key] = spr

    def io_schedule_loop(self):
        self.last_tick = time.time()
        while True:
            self.io_schedule()
            current_tick = time.time()
            self.params['delta'] = current_tick - self.last_tick
            self.last_tick = current_tick

    def start_io_schedule_loop(self):
        self.icl_thread = threading.Thread(target=self.io_schedule_loop)
        self.icl_thread.start()

    def append_routine(self, func, r_type='w', multi_inst=False):
        if not self.has_routine(func=func, r_type=r_type) or multi_inst:
            self.routines[r_type].append(func)

    def insert_routine(self, func, r_type='w', multi_inst=False):
        if not self.has_routine(func=func, r_type=r_type) or multi_inst:
            self.routines[r_type].insert(0, func)

    def has_routine(self, func, r_type='w'):
        return func in self.routines[r_type]

    def remove_routine(self, func, r_type='w', purge=True):
        while self.has_routine(func=func, r_type=r_type):
            self.routines[r_type].remove(func)
            if not purge:
                break

    def io_module_loop(self):
        self.start_io_schedule_loop()
        self.io_execute_loop()

    def io_execute_loop(self):
        run = True
        while run:
            run = self.io_execute()
            # 维持tick频率为30Hz
            self.clock.tick(self.fps)

    def io_execute(self):
        self.event_controller.handle_events()
        self.get_recent_input()
        self.renderer.render_frame()
        run = True
        for event in self.recent_input:
            e = event[0]
            if e.type == pygame.QUIT:
                run = False
        return run

    def get_recent_input(self):
        self.recent_input = self.event_controller.event_queue.copy()
