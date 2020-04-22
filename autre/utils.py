import traceback

from autre.constants import *
from Class.Joueur import Joueur, Bras
from Class.Monde import Monde


def chargement(fenetre, etape):
    font = pg.font.Font(None, 100)
    nom_jeu = font.render("Projet Transverse", 1, (255, 255, 255))

    fenetre.blit(nom_jeu, (400, 200))

    pg.draw.rect(
        fenetre,
        pg.Color("white"),
        (300, 375, 825, 35),  # (abscisse,ordonné,longuer,hauteur)
    )
    pg.draw.rect(
        fenetre,
        pg.Color("cadetblue4"),
        (300, 375, 55 * etape, 35)
        # (abscisse,ordonné,longueur,hauteur)
    )

    pg.display.flip()


def chargement_textures(fenetre, theme: str):
    """
    Fonction qui sert a charger les textures des 2 joueurs et les retourner
    dans 2 tableaux

    Args:
        fenetre : -
        theme (str): Theme à appliquer aux joueurs

    Returns:
        (tuple): tuple contenant:

            texture_joueurs (list): Tableau avec les textures du joueur 1 et 2 ainsi que où ils regardent
            texture_bras (list): Tableau avec les textures du bras des joueurs 1 et 2 ainsi que où ils pointent
    """

    texture_joueurs = [
        # Joueur 1
        {  # -1 Pour quand le joueur regarde a gauche
            -1: pg.transform.flip(
                pg.transform.scale(
                    pg.image.load(
                        "{}/1/corps.png".format(ACCES_JOUEUR.format(theme))
                    ).convert_alpha(),
                    (LARGEUR_JOUEUR, HAUTEUR_JOUEUR),
                ),
                True,
                False,
            ),
            # 1 Pour quand il regarde a droite
            1: pg.transform.scale(
                pg.image.load(
                    "{}/1/corps.png".format(ACCES_JOUEUR.format(theme))
                ).convert_alpha(),
                (LARGEUR_JOUEUR, HAUTEUR_JOUEUR),
            ),
        },
        # Joueur 2
        {  # -1 Pour quand le joueur regarde a gauche
            -1: pg.transform.flip(
                pg.transform.scale(
                    pg.image.load(
                        "{}/2/corps.png".format(ACCES_JOUEUR.format(theme))
                    ).convert_alpha(),
                    (LARGEUR_JOUEUR, HAUTEUR_JOUEUR),
                ),
                True,
                False,
            ),
            # 1 Pour quand il regarde a droite
            1: pg.transform.scale(
                pg.image.load(
                    "{}/2/corps.png".format(ACCES_JOUEUR.format(theme))
                ).convert_alpha(),
                (LARGEUR_JOUEUR, HAUTEUR_JOUEUR),
            ),
        },
    ]

    chargement(fenetre, 2)

    texture_bras = [
        {  # meme idée que plus haut mais cette foi on enregistre les
            # bras dans un dict
            -1: {},
            1: {},
        },
        {-1: {}, 1: {}},
    ]

    for i in range(-4, 15, 2):
        image_joueur1 = pg.transform.scale(
            pg.image.load(
                "{}/1/bras/{}.png".format(ACCES_JOUEUR.format(theme), i)
            ).convert_alpha(),
            (LARGEUR_JOUEUR, HAUTEUR_JOUEUR),
        )
        image_joueur2 = pg.transform.scale(
            pg.image.load(
                "{}/2/bras/{}.png".format(ACCES_JOUEUR.format(theme), i)
            ).convert_alpha(),
            (LARGEUR_JOUEUR, HAUTEUR_JOUEUR),
        )

        texture_bras[0][-1][i] = pg.transform.flip(image_joueur1, True, False)
        texture_bras[0][1][i] = image_joueur1

        texture_bras[1][-1][i] = pg.transform.flip(image_joueur2, True, False)
        texture_bras[1][1][i] = image_joueur2

        chargement(fenetre, 3)

    return texture_joueurs, texture_bras


def chargement_niveau(fenetre, theme: str, id_niveau: int):
    """
    Fonction qui sert a charger le terrain

    Args:
        fenetre : -
        theme (str): Theme terrain a charger
        id_niveau (int): ID du niveau a charger

    Returns:
        (tuple): tuple contenant:

            monde (list): -
            fond (list): -
    """
    monde = Monde(theme)
    monde.chargement_map(id_niveau)
    monde.enregistrement_map()

    fond = pg.Surface(RESOLUTION.size)
    fond.blit(
        pg.image.load(
            "{}/{}/rendu.png".format(ACCES_TERRAINS.format(theme), id_niveau)
        ).convert_alpha(),
        (0, 0),
    )
    fenetre.blit(fond, (0, 0))
    pg.display.flip()

    chargement(fenetre, 0)

    return monde, fond


def application_texture(
    fenetre, monde, texture_joueurs, texture_bras, toutes_les_images
):
    """

    Args:
        fenetre: -
        monde: -
        texture_joueurs: images du corps pour les joueurs
        texture_bras: images du bras pour les joueurs
        toutes_les_images: toutes les images chargées sur la fenetre

    Returns:
        (tuple): tuple contenant:

            joueur1 (Joueur): instance du joueur 1
            bras1 (Bras): instance du bras du joueur 1

            joueur2 (Joueur): instance du joueur 2
            bras2 (Bras): instance du bras du joueur 2
    """
    Joueur.containers = toutes_les_images
    Bras.containers = toutes_les_images

    joueur1 = Joueur(
        fenetre.get_rect(),
        monde.params.get(1),
        texture_joueurs[0],
        regarde=1,  # vers ou doit le perso (1 : droite, -1 : gauche)
        peau=1,  # peau du perso, 1 : joueur 1, 2 : joueur 2
    )
    joueur2 = Joueur(
        fenetre.get_rect(),
        monde.params.get(2),
        texture_joueurs[1],
        regarde=-1,  # vers ou doit le perso (1 : droite, -1 : gauche)
        peau=2,  # peau du perso, 1 : joueur 1, 2 : joueur 2
    )

    chargement(fenetre, 5)

    bras1 = Bras(
        fenetre.get_rect(),
        monde.params.get(1),
        texture_bras[0],
        regarde=1,  # vers ou doit pointer le bras (1 : droite, -1 : gauche)
        peau=1,  # bras du perso, 1 : joueur 1, 2 : joueur 2
    )
    bras2 = Bras(
        fenetre.get_rect(),
        monde.params.get(2),
        texture_bras[1],
        regarde=-1,  # vers ou doit pointer le bras (1 : droite, -1 : gauche)
        peau=2,  # bras du perso, 1 : joueur 1, 2 : joueur 2
    )

    chargement(fenetre, 6)

    return joueur1, bras1, joueur2, bras2


def crash(fenetre, e):
    """
    Fonction pour afficher une erreur (s'il y en a une) et quitter le programme
    Args:
        fenetre: -
        e: erreur
    """
    texte = pg.font.Font(None, 20)

    fond = pg.Surface(RESOLUTION.size)

    fenetre.blit(fond, (0, 0))
    pg.display.flip()

    tb = traceback.TracebackException.from_exception(e)
    message = "Une erreur est survenue, la fenetre va se fermer dans 5s\n\n\n"
    message += "Erreur: \n" + "\n".join(tb.format())

    for j, lignes in enumerate(message.split("\n")):
        err = texte.render(lignes, 0, pg.Color("Red"))

        fenetre.blit(err, (10, j * 17 + 30))
        pg.display.flip()

    for i in range(6, 1, -1):
        pg.display.set_caption(f"Erreur! fermeture dans {i}")
        pg.time.wait(1000)

    pg.quit()
    quit()
