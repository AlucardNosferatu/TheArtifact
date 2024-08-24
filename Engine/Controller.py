import time

import pygame


class EventController:
    def __init__(self, max_queue_size):
        self.max_queue_size = max_queue_size
        self.running = True
        self.event_queue = []

    def handle_events(self):
        # 获取当前时间戳
        timestamp = time.time()
        # 获取事件
        events = pygame.event.get()
        # 添加事件到队列
        # 将新事件和时间戳加入队列
        for event in events:
            self.event_queue.append((event, timestamp))
            # 如果队列已满，丢弃队首的事件
            if len(self.event_queue) > self.max_queue_size:
                self.event_queue.pop(0)
