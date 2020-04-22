import csv
import importlib

from .elements import *
from autre.constants import *


class Monde:
    id_niveau: int

    def __init__(self, theme: str):
        self.largeur_screen = LARGEUR_TUILE * LARGEUR_TERRAIN
        self.hauteur_screen = HAUTEUR_TUILE * HAUTEUR_TERRAIN

        self.niveau = []
        self.theme = theme
        self.params = {}

        self.tuiles = {
            "V": Vide(self.theme),
            "T": Terre(self.theme),
            "S": Sol(self.theme),
            "C": Caisse(self.theme),
        }

    def chargement_map(self, id_niveau: int) -> None:
        """
        Charge le niveau correspondant a l'id, dans self.niveau
        Args:
            id_niveau (int): ID du niveau a charger
        """
        self.id_niveau = id_niveau

        chemin = "{}/{}".format(ACCES_TERRAINS.format(self.theme), id_niveau)

        # on charge le niveau qui est sauvegardé dans un .csv car plus simple
        # de travailler dessus depui un tableur
        with open(f"{chemin}/model.csv", newline="") as model:
            lignes = csv.reader(model, delimiter=",")

            self.niveau = list(lignes)

        params = importlib.import_module(f"{chemin.replace('/', '.')}.params")
        self.params[1] = params.pos_perso1
        self.params[2] = params.pos_perso2

    def enregistrement_map(self) -> None:
        """
        Enregistre le niveau dans un .png pour, par la suite, n'avoir
        qu'a afficher une image en fond d'ecran
        """
        fond = pg.Surface(self.taille_screen())
        fond.blit(
            pg.image.load(
                "{}/fond.png".format(ACCES_TERRAINS.format(self.theme))
            ).convert_alpha(),
            (0, 0),
        )

        x_max = self.largeur_screen // LARGEUR_TUILE
        y_max = self.hauteur_screen // HAUTEUR_TUILE

        for i in range(0, y_max):
            for j in range(0, x_max):
                x = j * LARGEUR_TUILE
                y = i * HAUTEUR_TUILE
                tuile = self.niveau[i][j]

                fond.blit(self.tuiles[tuile].afficher((x, y)), (x, y))

        pg.display.update()

        pg.image.save(
            fond,
            "{}/{}/rendu.png".format(ACCES_TERRAINS.format(self.theme), self.id_niveau),
        )

    def taille_screen(self) -> tuple:
        size = (self.largeur_screen, self.hauteur_screen)
        return size

    def hit_box(self) -> list:
        hit_box = []

        x_max = self.largeur_screen // LARGEUR_TUILE
        y_max = self.hauteur_screen // HAUTEUR_TUILE

        for i in range(0, y_max):
            for j in range(0, x_max):
                x = j * LARGEUR_TUILE
                y = i * HAUTEUR_TUILE
                item = self.niveau[i][j]

                if item != "V":
                    hit_box.append((x, y))

        return hit_box
