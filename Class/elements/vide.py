from autre.constants import *


class Vide(pg.sprite.Sprite):
    def __init__(self, mode: str):
        super().__init__()
        self.pos = (0, 0)

        self.tuile = pg.transform.scale(
            pg.image.load("{}/vide.png".format(ACCES_TUILES.format(mode))),
            (LARGEUR_TUILE, HAUTEUR_TUILE),
        )

    def afficher(self, pos: tuple):
        self.pos = pos
        return self.tuile
