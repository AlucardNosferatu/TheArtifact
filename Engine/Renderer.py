class Renderer:
    def __init__(self, screen_size, pygame):
        self.pygame = pygame
        self.screen_size = screen_size
        self.screen = self.pygame.display.set_mode(screen_size)
        self.running = True
        self.draw_dict = {}

    def render_frame(self):
        # Clear the screen with a black background
        self.screen.fill((0, 0, 0))
        # Draw all objects from the global dictionary
        for key, (surface, position, visible, angle, magnify, flip) in self.draw_dict.items():
            # Blit the surface to the screen at the given position
            if visible:
                s = self.pygame.transform.rotate(surface=surface, angle=angle)
                s = self.pygame.transform.scale(surface=s, size=magnify)
                s = self.pygame.transform.flip(surface=s, flip_x=flip[0], flip_y=flip[1])
                self.screen.blit(s, position)
        # Update the display
        self.pygame.display.flip()

