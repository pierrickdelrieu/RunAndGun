import math

from autre.constants import *


class Projectile(pg.sprite.Sprite):
    containers: any

    images_path: list
    t: float
    gravity = 9.81
    angle: int
    velocity: float
    hit = (0, 0)  # indice 0 : le projectile a t'il touché quelque chose ? indice 1 : est-ce un joueur que ca a touche ?

    degats: int

    x: float
    y: float

    def __init__(
            self,
            screen_rect: pg.Rect,
            velocity: float,
            x: float,
            y: float,
            angle: int,
            degats: int,
            adversaire: tuple,
            chemin_images: str,
            monde: list,
    ):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.screen_rect = screen_rect

        self.velocity = velocity
        self.x = x
        self.y = y
        self.origin = (self.x, self.y)
        self.degats = degats
        self.angle = angle
        self.monde = monde

        self.adversaire = adversaire

        self.chemin_images = chemin_images

        self.image = pg.transform.scale(
            pg.image.load(
                self.chemin_images + "/projectile.png"
            ).convert_alpha(), (32, 32)
        )

        self.t = 0.5

        self.rect = self.image.get_rect()

        self.vx = self.velocity * math.cos(math.radians(self.angle))
        self.vy = self.velocity * math.sin(math.radians(self.angle))

    def update(self):
        adv = pg.Rect(
            self.adversaire[0] - LARGEUR_JOUEUR // 2,
            self.adversaire[1] - HAUTEUR_JOUEUR // 2,
            LARGEUR_JOUEUR, HAUTEUR_JOUEUR)

        if adv.collidepoint(*self.rect.center):
            self.image = pg.transform.scale(
                pg.image.load(
                    self.chemin_images + "/explosion.png"
                ).convert_alpha(),
                (64, 64),
            )
            self.vx, self.vy = 0, 0

            self.hit = (1, 1)
        else:
            if self.angle < 90:
                self.image = pg.transform.scale(
                    pg.image.load(
                        self.chemin_images + "/projectile.png"
                    ).convert_alpha(), (32, 32)
                )
            else:
                self.image = pg.transform.flip(
                    pg.transform.scale(
                        pg.image.load(
                            self.chemin_images + "/projectile.png"
                        ).convert_alpha(), (32, 32)
                    ),
                    True,
                    False
                )

            self.x = self.origin[0] + (self.vx * self.t)
            self.y = self.origin[1] - (
                    self.vy * self.t - (self.gravity / 2) * self.t * self.t
            )

            self.rect.left, self.rect.top = self.x, self.y

            self.t += 0.2

        for tile in self.monde:
            rect = pg.Rect(tile[0], tile[1], LARGEUR_TUILE, HAUTEUR_TUILE)

            if rect.collidepoint(*self.rect.center):
                self.hit = (1, 0)

        if 0 > self.x > self.screen_rect.right or self.y > self.screen_rect.bottom:
            self.hit = (1, 0)


class Type1(Projectile):
    containers: any

    degats = 10
    velocity = 150

    def __init__(
            self,
            screen_rect: pg.Rect,
            x: float,
            y: float,
            direction: int,
            angle: int,
            adversaire: tuple,
            monde: list,
            theme: str
    ):
        """
        Projectile de type 1
        Args:
            screen_rect (pg.Rect): -
            x (int): position X au lancé
            y (int): position Y au lancé
            direction (int): direction (1 -> vers la droite, -1 -> vers la gauche)
            angle (int): inclinaison du lancé
            adversaire (tuple): coordonnées de l'adversaire
            monde (list): tableau 2D avec les bloques du mondes
            theme (str): theme du monde
        """
        super().__init__(
            screen_rect,
            self.velocity,
            x,
            y,
            angle if direction == 1 else 180 - angle,
            self.degats,
            adversaire,
            ACCES_ARMES.format(theme) + "/1",
            monde,
        )


class Type2(Projectile):
    containers: any

    degats = 20
    velocity = 100

    def __init__(
            self,
            screen_rect: pg.Rect,
            x: float,
            y: float,
            direction: int,
            angle: int,
            adversaire: tuple,
            monde: list,
            theme: str
    ):
        """
        Projectile de type 1
        Args:
            screen_rect (pg.Rect): -
            x (int): position X au lancé
            y (int): position Y au lancé
            direction (int): direction (1 -> vers la droite, -1 -> vers la gauche)
            angle (int): inclinaison du lancé
            adversaire (tuple): coordonnées de l'adversaire
            monde (list): tableau 2D avec les bloques du mondes
            theme (str): theme du monde
        """
        super().__init__(
            screen_rect,
            self.velocity,
            x,
            y,
            angle if direction == 1 else 180 - angle,
            self.degats,
            adversaire,
            ACCES_ARMES.format(theme) + "/2",
            monde,
        )


class Type3(Projectile):
    containers: any

    degats = 30
    velocity = 95

    def __init__(
            self,
            screen_rect: pg.Rect,
            x: float,
            y: float,
            direction: int,
            angle: int,
            adversaire: tuple,
            monde: list,
            theme: str
    ):
        """
        Projectile de type 1
        Args:
            screen_rect (pg.Rect): -
            x (int): position X au lancé
            y (int): position Y au lancé
            direction (int): direction (1 -> vers la droite, -1 -> vers la gauche)
            angle (int): inclinaison du lancé
            adversaire (tuple): coordonnées de l'adversaire
            monde (list): tableau 2D avec les bloques du mondes
            theme (str): theme du monde
        """
        super().__init__(
            screen_rect,
            self.velocity,
            x,
            y,
            angle if direction == 1 else 180 - angle,
            self.degats,
            adversaire,
            ACCES_ARMES.format(theme) + "/3",
            monde,
        )
