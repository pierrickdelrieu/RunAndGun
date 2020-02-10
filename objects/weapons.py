import math

import pygame as pg


class Bullet(pg.sprite.Sprite):
    images = []
    t = 0
    gravity = 9.81
    angle = 30
    velocity = 140

    def __init__(self, screen_rect):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.screen_rect = screen_rect

        self.image = self.images[0]

        self.rect = self.image.get_rect(
            center=self.screen_rect.midleft
        )

        self.pos = pg.math.Vector2(
            self.screen_rect.midright[0], self.screen_rect.midright[1] - 30
        )
        self.vel = pg.math.Vector2(0, -450)
        self.damage = 10

        self.X = 30
        self.Y = 30
        self.vx = self.velocity * math.cos(math.radians(self.angle))
        self.vy = self.velocity * math.sin(math.radians(self.angle))

    def update(self):
        if self.X > self.pos[0] - 80:
            self.image = pg.transform.scale(
                pg.image.load(f"resources/sprites/effects/explosion.png").convert_alpha(),
                (64, 64)
            )
        else:
            self.X = self.vx * self.t
            self.Y = 400 - (self.vy * self.t - (self.gravity / 2) * self.t * self.t)

            self.rect.left, self.rect.top = self.X, self.Y

            self.t += .25
            print(self.X, self.Y, self.t, self.pos[0] - self.X)

            # self.image = pg.transform.scale(
            #     pg.image.load(f"resources/sprites/bullets/tomato.png").convert_alpha(),
            #     (
            #         int(-(14 * self.t ** 2) / 9 + (28 * self.t) / 3 + 16),
            #         int(-(14 * self.t ** 2) / 9 + (28 * self.t) / 3 + 16)
            #     )
            # )

        if self.rect.bottom <= 0:
            self.kill()
