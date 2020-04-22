from autre.constants import *


BOUTON_PRESS = False


def generation_couleur_survol(couleur: tuple) -> tuple:
    """
    Retourne une dégradé de la couleur pour quand on la survole
    Args:
        couleur (tuple): couleur de base

    Returns:
        (tuple): La couleur de base avec un dégradé

    """
    return (
        couleur[0] + (-50 if couleur[0] > 128 else 50),
        couleur[1] + (-50 if couleur[1] > 128 else 50),
        couleur[2] + (-50 if couleur[2] > 128 else 50),
    )


class Texte:
    def __init__(
        self,
        fenetre,
        couleur_fond: tuple,
        couleur_texte: tuple,
        texte: str,
        pos: tuple,
        **kwargs
    ):
        """
        Bouton pour le menu

        Args:
            fenetre: -
            couleur_fond (tuple): couleur derriere le texte du bouton
            couleur_texte (tuple): couleur du texte dans le bouton
            texte (str): Texte dans le bouton
            pos (tuple): Position du bouton
            **kwargs:
        """
        self.fenetre = fenetre
        self.couleur_fond = couleur_fond
        self.couleur_texte = couleur_texte

        self.texte = texte
        style_police = (
            "freesans"
            if kwargs.get("style_police") is None
            else kwargs.get("style_police")
        )
        taille_police = (
            48 if kwargs.get("taille_police") is None else kwargs.get("taille_police")
        )
        self.police = pg.font.SysFont(style_police, taille_police)

        self.titre = self.police.render(
            self.texte, True, self.couleur_texte, self.couleur_fond
        )
        self.rect_titre = self.titre.get_rect()
        self.rect_titre.center = pos

        self.fenetre.blit(self.titre, self.rect_titre)
        pg.display.flip()


class Bouton:
    rect_titre: any

    def __init__(
        self,
        fenetre,
        couleur_fond,
        couleur_texte: tuple,
        texte: str,
        pos: tuple,
        action: callable,
        identifiant: str,
        **kwargs
    ):
        """
        Bouton pour le menu

        Args:
            fenetre: -
            couleur_fond (tuple): couleur derriere le texte du bouton
            couleur_texte (tuple): couleur du texte dans le bouton
            texte (str): Texte dans le bouton
            pos (tuple): Position du bouton
            action (callable): Fonction a executer quand on clique sur le bouton
            **kwargs:
        """
        self.fenetre = fenetre
        self.couleur_fond = couleur_fond
        self.couleur_texte = couleur_texte
        self.pos = pos

        self.action = action
        self.identifiant = identifiant

        self.texte = texte
        style_police = (
            "freesans"
            if kwargs.get("style_police") is None
            else kwargs.get("style_police")
        )
        taille_police = (
            48 if kwargs.get("taille_police") is None else kwargs.get("taille_police")
        )
        self.police = pg.font.SysFont(style_police, taille_police)

        self.affiche(self.couleur_fond, self.couleur_texte)

    def affiche(self, couleur_fond, couleur_texte: tuple, marges: tuple = ()):
        titre = self.police.render(self.texte, True, couleur_texte, None)
        self.rect_titre = titre.get_rect()
        self.rect_titre.center = self.pos

        if 4 >= len(marges) > 0 and couleur_fond is not None:
            # si 2, alors les marges en haut et en bas seront marges[0]
            # et marges[1] sera pour les marges a droite et gauche
            if len(marges) == 2:
                rect_fond_titre = pg.Rect(
                    self.rect_titre[0] - marges[1],
                    self.rect_titre[1] - marges[0],
                    self.rect_titre[2] + marges[1] * 2,
                    self.rect_titre[3] + marges[0] * 2,
                )

                pg.draw.rect(self.fenetre, couleur_fond, rect_fond_titre)

            # marges[0] -> marge en haut, 1 -> a droite, 2 -> en bas, 3 -> gauche
            elif len(marges) == 4:
                rect_fond_titre = pg.Rect(
                    self.rect_titre[0] - marges[3],
                    self.rect_titre[1] - marges[0],
                    self.rect_titre[2] + marges[1],
                    self.rect_titre[3] + marges[2],
                )

                pg.draw.rect(self.fenetre, couleur_fond, rect_fond_titre)

        self.fenetre.blit(titre, self.rect_titre)

        pg.display.flip()

    def click(self):
        global BOUTON_PRESS

        couleur_texte_survol = generation_couleur_survol(self.couleur_texte)

        self.affiche(self.couleur_fond, couleur_texte_survol)

        if pg.mouse.get_pressed()[0] and not BOUTON_PRESS:
            BOUTON_PRESS = True
            return [1, self.identifiant, self.action()]
        elif not pg.mouse.get_pressed()[0]:
            BOUTON_PRESS = False
            return [0, self.identifiant, None]


class BoutonSelect(Bouton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.options = kwargs.get("options")
        self.choisie = 0

        self.texte_base = self.texte
        self.texte = self.texte_base + self.options[self.choisie % len(self.options)][0]

        self.affiche(self.couleur_fond, self.couleur_texte, (0, 100))

    def click(self):
        global BOUTON_PRESS

        couleur_texte_survol = generation_couleur_survol(self.couleur_texte)

        self.affiche(self.couleur_fond, couleur_texte_survol, (0, 100))

        if pg.mouse.get_pressed()[0] and not BOUTON_PRESS:
            BOUTON_PRESS = True
            self.choisie += 1
            self.texte = (
                self.texte_base + self.options[self.choisie % len(self.options)][0]
            )
            return [
                1,
                self.identifiant,
                self.action(self.options[self.choisie % len(self.options)]),
            ]
        elif not pg.mouse.get_pressed()[0]:
            BOUTON_PRESS = False
            return [0, self.identifiant, None]


class Menu:
    def __init__(self, fenetre, **kwargs):
        """
        Fenetre du menu

        Args:
            fenetre: -
            **kwargs:
        """
        self.fenetre = fenetre
        if kwargs.get("couleur_fond") is None:
            self.couleur_fond = (255, 255, 255)
        else:
            self.couleur_fond = kwargs.get("couleur_fond")

        self.fenetre.fill(self.couleur_fond)
        pg.display.flip()

        self.boutons = []

    def ajout_texte(self, *args, **kwargs):
        Texte(self.fenetre, *args, **kwargs)

    def ajout_bouton(self, *args, **kwargs):
        if kwargs.get("type_bouton") == "select":
            self.boutons.append(BoutonSelect(self.fenetre, *args, **kwargs))
        else:
            self.boutons.append(Bouton(self.fenetre, *args, **kwargs))

    def bouton_press(self):
        for bouton in self.boutons:
            dx = bouton.rect_titre[0]
            dy = bouton.rect_titre[1]

            fx = dx + bouton.rect_titre[2]
            fy = dy + bouton.rect_titre[3]

            pointeur = pg.mouse.get_pos()

            couleur_texte = bouton.couleur_texte

            if dx < pointeur[0] < fx and dy < pointeur[1] < fy:
                return bouton.click()
            else:
                bouton.affiche(bouton.couleur_fond, couleur_texte)
