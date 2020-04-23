from autre.constants import *
from .Joueur import Joueur


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
        self.energie = 100
        self.update()
        self.rect = self.image.get_rect().move(10, 50)

    def update(self):
        text = f"Energie: {self.energie}%"

        if self.energie == 0:
            self.texte.set_underline(True)

        if self.energie < 10:
            self.couleur = pg.Color("Red")
        elif self.energie < 50:
            self.couleur = pg.Color("Orange3")
        elif self.energie < 75:
            self.couleur = pg.Color("Orange")

        self.image = self.texte.render(text, 0, self.couleur)


class Arme(pg.sprite.Sprite):
    image: pg.Surface

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.texte = pg.font.Font(None, 40)
        self.texte.set_bold(1)
        self.couleur = pg.Color("Black")
        self.arme = 1
        self.update()
        self.rect = self.image.get_rect().move(RESOLUTION.size[0] - 150, 10)

    def update(self):
        text = f"Arme: {self.arme}"

        self.image = self.texte.render(text, 0, self.couleur)


class Vie(pg.sprite.Sprite):
    image: pg.Surface

    def __init__(self, screen_rect, joueur: Joueur):
        pg.sprite.Sprite.__init__(self,)
        self.texte = pg.font.Font(None, 22)
        self.texte.set_bold(1)
        self.couleur = pg.Color("White")

        self.joueur = joueur
        self.screen_rect = screen_rect

        self.vie = self.joueur.vie

        self.update()

        self.rect = self.image.get_rect().move(
            self.joueur.get_pos()[0], self.joueur.get_pos()[1] + 15
        )

    def update(self):
        text = f"Vie: {self.vie}/100"

        if self.vie == 0:
            self.texte.set_underline(True)

        if self.vie < 10:
            self.couleur = pg.Color("Red")
        elif self.vie < 50:
            self.couleur = pg.Color("Orange3")
        elif self.vie < 75:
            self.couleur = pg.Color("Orange")

        self.image = self.texte.render(text, 0, self.couleur, (0, 0, 0))

    def move(self, direction):
        self.rect.move_ip(direction * self.joueur.vitesse, 0)
        self.rect = self.rect.clamp(self.screen_rect)

        if direction != 0:
            self.joueur.energie -= 1

        self.rect.top = self.joueur.orig_top
