from autre.constants import *


class Caisse(pg.sprite.Sprite):
    def __init__(self, mode: str):
        super().__init__()
        self.pos = (0, 0)

        self.tuile = pg.transform.scale(
            pg.image.load("{}/caisse.png".format(ACCES_TUILES.format(mode))),
            (LARGEUR_TUILE, HAUTEUR_TUILE),
        )

    def afficher(self, pos: tuple):
        self.pos = pos
        return self.tuile
