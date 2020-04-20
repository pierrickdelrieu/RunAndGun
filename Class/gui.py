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


class Energie(pg.sprite.Sprite):
    image: pg.Surface

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.texte = pg.font.Font(None, 40)
        self.texte.set_bold(1)
        self.couleur = pg.Color("Black")
        self.update()
        self.rect = self.image.get_rect().move(10, 50)
        self.energie = 100

    def update(self):
        text = f"Energy: {self.energie}%"

        if self.energie == 0:
            self.texte.set_underline(True)

        if self.energie < 10:
            self.couleur = pg.Color('Red')
        elif self.energie < 50:
            self.couleur = pg.Color('Orange3')
        elif self.energie < 75:
            self.couleur = pg.Color('Orange')

        self.image = self.texte.render(text, 0, self.couleur)
