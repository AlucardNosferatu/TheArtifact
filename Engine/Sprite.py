# (surface, (pos_x, pos_y), active, ang, (mag_x, mag_y), flip)
class Sprite:
    def __init__(self, pygame, image_path, x=0, y=0, visible=True, rotation=0):
        """
        初始化 Sprite 对象。

        :param x: Sprite 的 x 坐标，默认为 0。
        :param y: Sprite 的 y 坐标，默认为 0。
        :param visible: Sprite 是否可见，默认为 True。
        :param rotation: Sprite 的旋转角度（以度为单位），默认为 0。
        """
        self.pygame = pygame
        self.image_path = image_path
        self.x = x
        self.y = y
        self.visible = visible
        self.rotation = rotation
        self.surface = self.pygame.image.load(self.image_path)
        self.original_surface = self.surface  # 保留原始图像以便于旋转
