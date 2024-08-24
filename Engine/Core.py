import threading

import pygame

from Engine.Controller import EventController
from Engine.Renderer import Renderer


class Core:
    eg_thread = None

    def __init__(self, screen_size=(1280, 720), fps=30, max_queue_size=256, recent_amount=16):
        self.fps = fps
        self.screen_size = screen_size
        self.max_queue_size = max_queue_size
        self.recent_amount = recent_amount
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

    def execute_game(self):
        for routine_func in self.world_routine:
            spr_key, spr = routine_func(params=self.params, recent_input=self.recent_input)
            if spr_key is not None:
                self.renderer.world_draw[spr_key] = spr
        for routine_func in self.ui_routine:
            spr_key, spr = routine_func(params=self.params, recent_input=self.recent_input)
            if spr_key is not None:
                self.renderer.ui_draw[spr_key] = spr

    def execute_game_loop(self):
        wait = 0.99 / self.fps
        while True:
            self.execute_game()
            pygame.time.wait(round(wait * 1000))

    def start_game_loop(self):
        self.eg_thread = threading.Thread(target=self.execute_game_loop)
        self.eg_thread.start()

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

    def engine_run(self):
        pygame.init()
        try:
            self.start_game_loop()
            while True:
                self.event_controller.handle_events()
                self.get_recent_input()
                self.renderer.render_frame()
                for event in self.recent_input:
                    e = event[0]
                    if e.type == pygame.QUIT:
                        return
                # 维持tick频率为30Hz
                self.clock.tick(self.fps)
        finally:
            pygame.quit()

    def get_recent_input(self):
        self.recent_input.clear()
        for _ in range(self.recent_amount):
            if len(self.event_controller.event_queue) > 0:
                self.recent_input.append(self.event_controller.event_queue.pop(0))
