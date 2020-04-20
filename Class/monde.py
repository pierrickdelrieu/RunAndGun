import csv
import importlib

from .elements import *
from .constants import *


class World:
    id_niveau: int

    def __init__(self, theme: str):
        self.largeur_tuile = LARGEUR_TUILE
        self.hauteur_tuile = HAUTEUR_TUILE

        self.largeur_terrain = LARGEUR_TERRAIN
        self.hauteur_terrain = HAUTEUR_TERRAIN

        self.largeur_screen = self.largeur_tuile * self.largeur_terrain
        self.hauteur_screen = self.hauteur_tuile * self.hauteur_terrain

        self.niveau = []
        self.theme = theme

        self.tiles = {
            'V': Vide,
            'T': Terre,
            'S': Sol,
            'C': Caisse,
        }

    def chargement_map(self, id_niveau: int) -> None:
        self.id_niveau = id_niveau

        chemin = "{}/{}".format(ACCES_TERRAINS.format(self.theme), id_niveau)

        with open(f"{chemin}/model.csv", newline='') as model:
            lignes = csv.reader(model, delimiter=',')

            for ligne in lignes:
                print(', '.join(ligne))

    def save_map(self) -> None:
        background = pg.Surface(self.screen_size())
        background.blit(
            pg.image.load(f"{TILES_PATH}/sky.jpg").convert_alpha(),
            (0, 0)
        )

        y_max = int(self.screen_height / self.tile_height)
        x_max = int(self.screen_width / self.tile_width)

        for i in range(0, y_max):
            for j in range(0, x_max):
                x = j * self.tile_width
                y = i * self.tile_height
                item = self.level.layouts[i][j]

                background.blit(
                    self.tiles[item].render((x, y)),
                    (x, y)
                )

        pg.display.update()

        pg.image.save(background, f"resources/levels/{self.level_id}/map.png")

    def screen_size(self) -> tuple:
        size = (self.tile_width * self.size_tiles_x_world, self.tile_height * self.size_tiles_y_world)
        return size

    def hit_box(self) -> list:
        hit_box = []

        y_max = int(self.screen_height / self.tile_height)
        x_max = int(self.screen_width / self.tile_width)

        for i in range(0, y_max):
            for j in range(0, x_max):
                x = j * self.tile_width
                y = i * self.tile_height
                item = self.level.layouts[i][j]

                if item != 0:
                    hit_box.append((x, y))

        return hit_box
