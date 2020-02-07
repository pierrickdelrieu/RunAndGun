import pygame


class Tank(pygame.sprite.Sprite):
    def __init__(self, screen, tile_width):
        super().__init__()

        self.tile_width = tile_width
        self.screen = screen

        self.body = pygame.image.load(f"resources/sprites/tank.png")
        self.cannon = pygame.image.load(f"resources/sprites/cannon.png")

        self.tank = pygame.transform.scale(
                self.body,
                (tile_width, (tile_width * 178) // 489)  # (489 // 4, 178 // 4)
            )

    def render(self):
        return self.tank
