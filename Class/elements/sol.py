import random

from Class.constants import *


NOMBRE = 3


class Sol(pg.sprite.Sprite):
    def __init__(self, mode: str):
        super().__init__()
        self.pos = (0, 0)

        self.tuiles = []
        for i in range(1, NOMBRE):
            self.tuiles.append(pg.transform.scale(
                pg.image.load(
                    "{}/sol{}.png".format(
                        ACCES_TUILES.format(mode),
                        i
                    )
                ), (LARGEUR_TUILE, HAUTEUR_TUILE)
            ))

    def afficher(self, pos):
        self.pos = pos
        return self.tuiles[random.randint(0, NOMBRE - 1)]
