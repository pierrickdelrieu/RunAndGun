import math

import pygame as pg


class Bullet(pg.sprite.Sprite):
    images_path = [f"resources/sprites/bullets/tomato.png"]
    t = 1
    gravity = 9.81
    angle: int
    velocity: float

    damage: int

    x: float
    y: float

    def __init__(self,
                 screen_rect: pg.Rect,
                 velocity: float, x: float, y: float,
                 angle: int,
                 damage: int,
                 adv: tuple):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.screen_rect = screen_rect

        self.velocity = velocity
        self.x = x
        self.y = y
        self.origin = (self.x, self.y)
        self.damage = damage
        self.angle = angle

        self.adv = adv

        self.image = pg.transform.scale(
                pg.image.load(self.images_path[0]).convert_alpha(),
                (16, 16)
            )

        self.rect = self.image.get_rect(
            center=self.screen_rect.center
        )

        self.pos = pg.math.Vector2(
            self.screen_rect.midright[0], self.screen_rect.midright[1] - 30
        )
        self.damage = 10

        self.vx = self.velocity * math.cos(math.radians(self.angle))
        self.vy = self.velocity * math.sin(math.radians(self.angle))

    def update(self):
        print(self.x, self.y, self.vx, self.vy, self.adv)
        if self.adv[0] + 20 > self.x > self.adv[0] - 20 and self.adv[1] + 20 > self.y > self.adv[1] - 20:
            self.image = pg.transform.scale(
                pg.image.load(f"resources/sprites/effects/explosion.png").convert_alpha(),
                (64, 64)
            )
        else:

            self.x = self.origin[0] + (self.vx * self.t)
            self.y = self.origin[1] - (self.vy * self.t - (self.gravity / 2) * self.t * self.t)

            self.rect.left, self.rect.top = self.x, self.y

            self.t += .2

            self.image = pg.transform.scale(
                pg.image.load(self.images_path[0]).convert_alpha(),
                (
                    int((1 / self.y) * 10000),
                    int((1 / self.y) * 10000)
                )
            )

        if 0 > self.x > self.screen_rect.right or self.y > self.screen_rect.bottom:
            self.kill()


class Tomato(Bullet):
    damage = 10

    def __init__(self,
                 screen_rect: pg.Rect,
                 velocity: float, x: float, y: float,
                 direction: int, angle: int,
                 adv: tuple):
        super().__init__(screen_rect, velocity, x, y, angle if direction == 1 else 180 - angle, self.damage, adv)

        Bullet.images = [f"resources/sprites/bullets/tomato.png"]
