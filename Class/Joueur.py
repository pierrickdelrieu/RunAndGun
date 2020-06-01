from autre.constants import *


class Joueur(pg.sprite.Sprite):
    containers: any

    vitesse = 5
    bonds = 10

    is_shooting: bool = False

    def __init__(
        self, screen_rect: pg.Rect, pos: tuple, textures, regarde: int
    ):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.screen_rect = screen_rect

        self.regarde = regarde
        self.images = textures
        self.image = textures.get(self.regarde)

        self.rect = self.image.get_rect(
            midbottom=(
                (pos[0] + 1) * LARGEUR_TUILE,
                (pos[1] + 1) * HAUTEUR_TUILE
            )
        )
        self.energie = 100
        self.vie = 100
        self.en_vie = True

    def move(self, direction: int, monde: list):
        """
        Fonction appelée lorsque qu'il y a un mouvement à effectuer au perso

        Args :
            direction (int) : si 1, vers la droite | si -1, vers la gauche
            monde (list) : liste contenant toutes les boites de
             collision du monde (cf Class/Monde.py#L90)
        """
        if direction:
            self.regarde = direction
        self.rect.move_ip(direction * self.vitesse, 0)
        self.rect = self.rect.clamp(self.screen_rect)

        self.image = self.images.get(self.regarde)

        if direction != 0:
            self.energie -= 1
            self.rect.top += 1 if self.rect.left % 2 else -1

        # est-ce que parmi toutes les boites de collision, le perso est sur
        # l'une d'elle ? si c'est le cas, alors dans la liste il y aura un 1,
        # max de 0, ..., 1, ... donne 1 donc True
        sol = max(
            pg.Rect(tile[0], tile[1] - 10, LARGEUR_TUILE, HAUTEUR_TUILE).collidepoint(
                self.rect.center[0], self.rect.center[1] + HAUTEUR_JOUEUR // 2
            )
            for tile in monde
        )

        # meme idée qu'avec `sol` mais en vérifiant cette fois si au-dessus
        # devant le perso et non en dessous
        obstacle = max(
            pg.Rect(tile[0], tile[1], LARGEUR_TUILE, HAUTEUR_TUILE).collidepoint(
                self.rect.center[0], self.rect.center[1] + HAUTEUR_JOUEUR // 3
            )
            for tile in monde
        )

        # si sol = 0, le perso flotte donc on le descend de la taille d'une
        # tuile pour qu'il "tombe" sur celle en dessous
        if not sol:
            self.rect.top += HAUTEUR_TUILE

        # si sol = 1 et obstacle = 1 alors le perso est face à un mur donc
        # on le monte de la hauteur d'une tuile
        if sol and obstacle:
            self.rect.top -= HAUTEUR_TUILE

    def get_pos(self) -> tuple:
        """
        Retourne simplement la position du joueur

        Returns :
            (tuple) : x et y du centre du perso
        """
        return self.rect.center


# Répétition de code (non propre donc à changer) pour appliquer les mêmes
# physiques que le corps du perso mais au bras
class Bras(pg.sprite.Sprite):
    containers: any

    angle = 0
    vitesse = 5
    bonds = 10

    def __init__(
        self, screen_rect: pg.Rect, pos: tuple, textures, regarde: int
    ):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.screen_rect = screen_rect

        self.regarde = regarde
        self.images = textures
        self.image = textures.get(self.regarde)

        self.image = self.images.get(regarde).get(self.angle)
        self.rect = self.image.get_rect(
            midbottom=(
                (pos[0] + 1) * LARGEUR_TUILE,
                (pos[1] + 1) * HAUTEUR_TUILE
            )
        )

    def move(self, direction, monde):
        if direction:
            self.regarde = direction
            self.rect.top += 1 if self.rect.left % 2 else -1

        self.rect.move_ip(direction * self.vitesse, 0)
        self.rect = self.rect.clamp(self.screen_rect)

        self.image = self.images[self.regarde][self.angle]

        sol = max(
            pg.Rect(tile[0], tile[1] - 10, LARGEUR_TUILE, HAUTEUR_TUILE).collidepoint(
                self.rect.center[0], self.rect.center[1] + HAUTEUR_JOUEUR // 2
            )
            for tile in monde
        )

        obstacle = max(
            pg.Rect(tile[0], tile[1], LARGEUR_TUILE, HAUTEUR_TUILE).collidepoint(
                self.rect.center[0], self.rect.center[1] + HAUTEUR_JOUEUR // 3
            )
            for tile in monde
        )

        if not sol:
            self.rect.top += HAUTEUR_TUILE

        if sol and obstacle:
            self.rect.top -= HAUTEUR_TUILE

    def rotate(self, angle):
        if angle != 0:
            if 15 > self.angle > -5:
                if angle == -1 and self.angle == -4 or angle == 1 and self.angle == 14:
                    return
                self.angle += angle * 2
                self.image = self.images.get(self.regarde).get(self.angle)
                pg.time.wait(100)

    def get_pos(self):
        return self.rect.center
