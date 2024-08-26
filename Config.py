import pygame


class SurfaceCache:
    cache = {}

    @staticmethod
    def load(key, image_path):
        SurfaceCache.cache[key] = pygame.image.load(image_path).convert_alpha()


class GameVars:
    g_vars = {}

    @staticmethod
    def load(key, var):
        GameVars.g_vars[key] = var
