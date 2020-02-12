import pygame as pg


class Angle(pg.sprite.Sprite):
    angle = 0
    image: pg.Surface

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font(None, 40)
        self.font.set_bold(1)
        self.color = pg.Color("Black")
        self.update()
        self.rect = self.image.get_rect().move(10, 10)

    def update(self):
        text = f"Angle: {self.angle}°"
        self.image = self.font.render(text, 0, self.color)
