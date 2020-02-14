import math

from .constants import TILE_WIDTH, TILE_HEIGHT

import pygame as pg


class Bullet(pg.sprite.Sprite):
    images_path: list
    t: float
    gravity = 9.81
    angle: int
    velocity: float
    hit = False

    damage: int

    x: float
    y: float

    def __init__(self,
                 screen_rect: pg.Rect,
                 velocity: float, x: float, y: float,
                 angle: int,
                 damage: int,
                 adv: tuple,
                 images_path,
                 world: list):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.screen_rect = screen_rect

        self.velocity = velocity
        self.x = x + 10
        self.y = y + 42
        self.origin = (self.x, self.y)
        self.damage = damage
        self.angle = angle
        self.world = world

        self.adv = adv

        self.images_path = images_path
        self.image = pg.transform.scale(
                pg.image.load(self.images_path[0]).convert_alpha(),
                (32, 32)
            )

        self.t = .5 if self.angle < 90 else .2

        self.rect = self.image.get_rect(
            center=self.screen_rect.center
        )

        self.damage = 10

        self.vx = self.velocity * math.cos(math.radians(self.angle))
        self.vy = self.velocity * math.sin(math.radians(self.angle))

    def update(self):
        print(self.x, self.y, self.adv, self.rect)
        adv = pg.Rect(self.adv[0], self.adv[1], 128, 128)
        if adv.colliderect(self.rect):
            self.image = pg.transform.scale(
                pg.image.load(f"resources/sprites/effects/explosion.png").convert_alpha(),
                (64, 64)
            )
            self.vx, self.vy = 0, 0
            self.hit = True
        else:
            self.x = self.origin[0] + (self.vx * self.t)
            self.y = self.origin[1] - (self.vy * self.t - (self.gravity / 2) * self.t * self.t)

            self.rect.left, self.rect.top = self.x, self.y

            self.t += .2

            # self.image = pg.transform.scale(
            #     pg.image.load(self.images_path[0]).convert_alpha(),
            #     (
            #         int((1 / self.y) * 10000),
            #         int((1 / self.y) * 10000)
            #     )
            # )

        for tile in self.world:
            rect = pg.Rect(tile[0], tile[1], TILE_WIDTH, TILE_HEIGHT)

            if rect.collidepoint(self.x, self.y + 20):
                pg.time.wait(1000)
                self.kill()

        if 0 > self.x > self.screen_rect.right or self.y > self.screen_rect.bottom:
            self.kill()


class Tomato(Bullet):
    damage = 10

    def __init__(self,
                 screen_rect: pg.Rect,
                 velocity: float, x: float, y: float,
                 direction: int, angle: int,
                 adv: tuple,
                 world: list):

        super().__init__(
            screen_rect,
            velocity, x, y,
            angle if direction == 1 else 180 - angle,
            self.damage, adv,
            [f"resources/sprites/bullets/tomato.png"],
            world
        )

