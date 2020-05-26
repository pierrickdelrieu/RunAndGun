from autre.constants import *
from .Joueur import Joueur


class VieGUI(pg.sprite.Sprite):
    image: pg.Surface

    def __init__(self, screen_rect, joueur: Joueur):
        pg.sprite.Sprite.__init__(self,)
        self.texte = pg.font.Font(None, 22)
        self.texte.set_bold(1)
        self.couleur = pg.Color("White")

        self.joueur = joueur
        self.screen_rect = screen_rect

        self.update()

        # -10 / -26 : tatonnement pour aligner correctement...
        self.rect = self.image.get_rect().move(
            self.joueur.get_pos()[0] - LARGEUR_JOUEUR // 2 - 10,
            self.joueur.get_pos()[1] - HAUTEUR_JOUEUR // 2 - 26,
        )

    def update(self):
        texte = self.texte.render(
            f"Vie: {self.joueur.vie}/100", True, self.couleur, (0, 0, 0)
        )

        self.image = pg.Surface((texte.get_width(), texte.get_height()))

        self.image.blit(texte, (0, 0))

    def move(self):
        # -10 / -26 : tatonnement pour aligner correctement...
        self.rect = self.image.get_rect().move(
            self.joueur.get_pos()[0] - LARGEUR_JOUEUR // 2 - 10,
            self.joueur.get_pos()[1] - HAUTEUR_JOUEUR // 2 - 26,
        )


class ArmeGUI(pg.sprite.Sprite):
    image: pg.Surface

    def __init__(self, theme: str):
        pg.sprite.Sprite.__init__(self)
        self.texte = pg.font.Font(None, 40)
        self.texte.set_bold(1)
        self.couleur = pg.Color("Black")
        self.arme = 1

        self.theme = theme

        self.update()

        self.rect = self.image.get_rect().move(RESOLUTION.size[0] - 150, 10)

    def update(self):
        texte = self.texte.render(f"Arme: ", 0, self.couleur)
        self.image = pg.Surface(
            (texte.get_width() + 100, texte.get_height()), pg.SRCALPHA
        )
        arme = pg.transform.scale(
            pg.image.load(
                f"{ACCES_ARMES.format(self.theme)}/{self.arme}/projectile.png"
            ).convert_alpha(),
            (26, 26),
        )
        self.image.blit(texte, (0, 0))
        self.image.blit(arme, (texte.get_width(), 0))


class TourGUI(pg.sprite.Sprite):
    image: pg.Surface

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.texte = pg.font.Font(None, 40)
        self.texte.set_bold(1)
        self.couleur = pg.Color("Black")
        self.tour = 1
        self.update()

        self.rect = self.image.get_rect().move(10, 10)

    def update(self):
        texte = f"Tour: joueur {self.tour}"

        self.image = self.texte.render(texte, 0, self.couleur)


class EnergieGUI(pg.sprite.Sprite):
    image: pg.Surface

    def __init__(self, screen_rect, joueur: Joueur):
        pg.sprite.Sprite.__init__(self,)
        self.texte = pg.font.Font(None, 22)
        self.texte.set_bold(1)
        self.couleur = pg.Color("White")

        self.joueur = joueur
        self.screen_rect = screen_rect

        self.energie = self.joueur.energie
        self.fond_couleur = (0, 0, 0)

        self.update()

        # -25 / +15 : tatonnement pour aligner correctement...
        self.rect = self.image.get_rect().move(
            self.joueur.get_pos()[0] - LARGEUR_JOUEUR // 2 - 25,
            self.joueur.get_pos()[1] - HAUTEUR_JOUEUR // 2 + 15,
        )

    def update(self):
        if self.joueur.energie < 10:
            couleur = pg.Color("Red")
        elif self.joueur.energie < 50:
            couleur = pg.Color("Orange3")
        elif self.joueur.energie < 75:
            couleur = pg.Color("Orange")
        else:
            couleur = self.couleur

        texte = self.texte.render(
            f"Déplacement: {self.joueur.energie}%",
            True, couleur, self.fond_couleur
        )

        self.image = pg.Surface((texte.get_width(), texte.get_height()))

        self.image.blit(texte, (0, 0))

    def move(self, ton_tour=False):
        if ton_tour:
            self.fond_couleur = (6, 96, 14)
        else:
            self.fond_couleur = (0, 0, 0)

        # -10 : tatonnement pour aligner correctement...
        self.rect = self.image.get_rect().move(
            self.joueur.get_pos()[0] - LARGEUR_JOUEUR // 2 - 10,
            self.joueur.get_pos()[1] - HAUTEUR_JOUEUR // 2 - 10,
        )


class AideGUI(pg.sprite.Sprite):
    image: pg.Surface

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.texte = pg.font.Font(None, 30)
        self.texte.set_bold(1)
        self.couleur = pg.Color("Black")

        self.update()
        # -20 : tatonnement pour aligner correctement...
        self.rect = self.image.get_rect().move(10, RESOLUTION.size[1] - 20)

    def update(self):
        texte = f"A: arme précédente | Z: arme suivante | I: info sur l'arme"

        self.image = self.texte.render(texte, 0, self.couleur)
