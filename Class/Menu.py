from autre.constants import *


BOUTON_PRESS = False


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
        Texte pour le menu

        Args :
            fenetre : -
            couleur_fond (tuple) : couleur derriere le texte du bouton
            couleur_texte (tuple) : couleur du texte dans le bouton
            texte (str) : Texte dans le bouton
            pos (tuple) : Position du bouton
            **kwargs :
        """
        self.fenetre = fenetre
        self.couleur_fond = couleur_fond
        self.couleur_texte = couleur_texte

        self.pos = pos

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

    def affiche(self):
        """
        Affiche le texte sur l'écran
        """
        self.rect_titre.x = self.pos[0] - self.rect_titre.w // 2
        self.rect_titre.y = self.pos[1] - self.rect_titre.h // 2

        self.fenetre.blit(self.titre, self.rect_titre)


class Bouton:
    rect_titre: any

    def __init__(
            self,
            fenetre,
            image: pg.Surface,
            pos: tuple,
            action: callable,
            identifiant: str,
    ):
        """
        Bouton pour le menu

        Args :
            fenetre : -
            pos (tuple) : Position du bouton
            action (callable) : Fonction à exécuter quand on clique sur le bouton
        """
        self.fenetre = fenetre
        self.pos = pos

        self.action = action
        self.identifiant = identifiant

        self.image = image
        self.image_rect = self.image.get_rect()

        self.affiche()

    def affiche(self):
        """
        Affiche le bouton sur l'écran
        """
        self.image_rect.x = self.pos[0] - self.image_rect.w // 2
        self.image_rect.y = self.pos[1] - self.image_rect.h // 2

        self.fenetre.blit(self.image, self.image_rect)
        self.fenetre.blit(self.image, self.image_rect)

    def click(self) -> list:
        """
        Retourne un tableau contenant différentes infos sur le bouton

        Returns :
            (list) : indice 0 : 1 si cliqué, 0 sinon
                     indice 1 : l'identifiant du bouton
                     indice 2 : le retour de l'action effectuée par le bouton
        """
        return [1, self.identifiant, self.action()]


class Image:
    def __init__(self, fenetre, texture: pg.Surface, pos: tuple):
        """
        Image pour le menu

        Args :
            fenetre : -
            texture (pg.Surface) : Image à afficher
            pos (tuple) : Position de l'image
        """

        self.fenetre = fenetre
        self.texture = texture

        self.rect_image = self.texture.get_rect()
        self.rect_image.center = pos

        self.affiche()

    def affiche(self):
        """
        Affiche l'image sur l'écran
        """
        self.fenetre.blit(self.texture, self.rect_image)


class Menu:
    def __init__(self, fenetre, **kwargs):
        """
        Fenetre du menu

        Args :
            fenetre : -
            **kwargs :
        """
        self.fenetre = fenetre
        if kwargs.get("couleur_fond") is None:
            self.couleur_fond = (255, 255, 255)
        else:
            self.couleur_fond = kwargs.get("couleur_fond")

        self.fenetre.fill(self.couleur_fond)
        pg.display.flip()

        self.textes = []
        self.images = []
        self.boutons = []

    def ajout_texte(self, *args, **kwargs):
        """
        Ajoute un texte dans la structure du menu
        """
        self.textes.append(Texte(self.fenetre, *args, **kwargs))

    def ajout_image(self, *args, **kwargs):
        """
        Ajoute une image dans la structure du menu
        """
        self.images.append(Image(self.fenetre, *args, **kwargs))

    def ajout_bouton(self, *args, **kwargs):
        """
        Ajoute un bouton dans la structure du menu
        """
        self.boutons.append(Bouton(self.fenetre, *args, **kwargs))

    def rerendre(self):
        """
        Permet de rafraichir tous les éléments du menu
        """
        for bouton in self.boutons:
            bouton.affiche()

        for texte in self.textes:
            texte.affiche()

        for image in self.images:
            image.affiche()

    def supprime(self):
        """
        Vide tous les éléments du menu
        """
        self.boutons = []
        self.textes = []
        self.images = []

    def bouton_press(self):
        """
        Test si un des boutons du menu est pressé
        """
        dessus = False
        for bouton in self.boutons:
            if bouton.image_rect.collidepoint(pg.mouse.get_pos()):
                pg.mouse.set_cursor(*pg.cursors.diamond)
                dessus = True

                press = sum(pg.mouse.get_pressed())

                if press:
                    action = bouton.click()
                    pg.time.wait(300)

                    return action
        if not dessus:
            pg.mouse.set_cursor(*pg.cursors.arrow)
