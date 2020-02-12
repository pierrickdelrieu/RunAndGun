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


class Fuel(pg.sprite.Sprite):
    fuel: int
    image: pg.Surface

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font(None, 40)
        self.font.set_bold(1)
        self.color = pg.Color("Black")
        self.update()
        self.rect = self.image.get_rect().move(10, 50)

    def update(self):
        text = f"Fuel: {self.fuel}%"

        if self.fuel == 0:
            self.font.set_underline(True)

        if self.fuel < 10:
            self.color = pg.Color('Red')
        elif self.fuel < 50:
            self.color = pg.Color('Orange3')
        elif self.fuel < 75:
            self.color = pg.Color('Orange')

        self.image = self.font.render(text, 0, self.color)
