from Class.armes import Tomato
from Class.constants import *
from Class.gui import Angle, Energie
from Class.joueur import Joueur, Bras
from Class.monde import Monde

chargement_etapes = 1

pg.init()
fenetre = pg.display.set_mode(RESOLUTION.size)


def chargement():
    font = pg.font.Font(None, 100)
    nom_jeu = font.render("Projet Transverse", 1, (255, 255, 255))

    fenetre.blit(nom_jeu, (400, 200))

    pg.draw.rect(
        fenetre, pg.color.Color('white'),
        (300, 375, 825, 35)  # (abscisse,ordonné,longuer,hauteur)
    )
    pg.draw.rect(
        fenetre, pg.color.Color('cadetblue4'),
        (300, 375, 55 * chargement_etapes, 35)
        # (abscisse,ordonné,longueur,hauteur)
    )

    pg.display.flip()


chargement()


def chargement_textures(theme: str):
    """
    Fonction qui sert a charger les textures des 2 joueurs et les retourner
    dans 2 tableaux

    Args:
        theme (str): Theme à appliquer aux joueurs

    Returns:
        (tuple): tuple contenant:

            texture_joueurs (list): Tableau avec les textures du joueur 1 et 2 ainsi que où ils regardent
            texture_bras (list): Tableau avec les textures du bras des joueurs 1 et 2 ainsi que où ils pointent
    """
    global chargement_etapes

    texture_joueurs = [
        # Joueur 1
        {  # -1 Pour quand le joueur regarde a gauche
            -1: pg.transform.flip(
                pg.transform.scale(
                    pg.image.load(
                        "{}/1/corps.png".format(ACCES_JOUEUR.format(theme))
                    ).convert_alpha(),
                    (LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
                ),
                True, False
            ),
            # 1 Pour quand il regarde a droite
            1: pg.transform.scale(
                pg.image.load(
                    "{}/1/corps.png".format(ACCES_JOUEUR.format(theme))
                ).convert_alpha(),
                (LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
            )
        },

        # Joueur 2
        {  # -1 Pour quand le joueur regarde a gauche
            -1: pg.transform.flip(
                pg.transform.scale(
                    pg.image.load(
                        "{}/2/corps.png".format(ACCES_JOUEUR.format(theme))
                    ).convert_alpha(),
                    (LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
                ),
                True, False
            ),
            # 1 Pour quand il regarde a droite
            1: pg.transform.scale(
                pg.image.load(
                    "{}/2/corps.png".format(ACCES_JOUEUR.format(theme))
                ).convert_alpha(),
                (LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
            )
        }
    ]

    chargement_etapes += 1
    chargement()

    texture_bras = [
        {  # meme idée que plus haut mais cette foi on enregistre les
            # bras dans un dict
            -1: {},
            1: {}
        },
        {
            -1: {},
            1: {}
        }
    ]

    for i in range(-4, 15, 2):
        image_joueur1 = pg.transform.scale(
            pg.image.load(
                "{}/1/bras/{}.png".format(ACCES_JOUEUR.format(theme), i)
            ).convert_alpha(),
            (LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
        )
        image_joueur2 = pg.transform.scale(
            pg.image.load(
                "{}/2/bras/{}.png".format(ACCES_JOUEUR.format(theme), i)
            ).convert_alpha(),
            (LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
        )

        texture_bras[0][-1][i] = pg.transform.flip(image_joueur1, True, False)
        texture_bras[0][1][i] = image_joueur1

        texture_bras[1][-1][i] = pg.transform.flip(image_joueur2, True, False)
        texture_bras[1][1][i] = image_joueur2

        chargement_etapes += 1
        chargement()

    return texture_joueurs, texture_bras


def chargement_niveau(theme: str, id_niveau: int):
    global chargement_etapes

    monde = Monde(theme)
    monde.chargement_map(1)
    monde.enregistrement_map()

    fond = pg.Surface(RESOLUTION.size)
    fond.blit(
        pg.image.load(
            "{}/{}/rendu.png".format(
                ACCES_TERRAINS.format(theme),
                id_niveau
            )).convert_alpha(),
        (0, 0))
    fenetre.blit(fond, (0, 0))
    pg.display.flip()

    chargement_etapes += 1
    chargement()

    return monde, fond


def application_texture(monde, texture_joueurs, texture_bras,
                        toutes_les_images):
    global chargement_etapes

    Joueur.containers = toutes_les_images
    Bras.containers = toutes_les_images

    joueur1 = Joueur(
        fenetre.get_rect(),
        monde.params.get(1),
        texture_joueurs[0],
        regarde=1,  # vers ou doit le perso (1 : droite, -1 : gauche)
        peau=1  # peau du perso, 1 : joueur 1, 2 : joueur 2
    )
    joueur2 = Joueur(
        fenetre.get_rect(),
        monde.params.get(2),
        texture_joueurs[1],
        regarde=-1,  # vers ou doit le perso (1 : droite, -1 : gauche)
        peau=2  # peau du perso, 1 : joueur 1, 2 : joueur 2
    )

    chargement_etapes += 1
    chargement()

    bras1 = Bras(
        fenetre.get_rect(),
        monde.params.get(1),
        texture_bras[0],
        regarde=1,  # vers ou doit pointer le bras (1 : droite, -1 : gauche)
        peau=1  # bras du perso, 1 : joueur 1, 2 : joueur 2
    )
    bras2 = Bras(
        fenetre.get_rect(),
        monde.params.get(2),
        texture_bras[1],
        regarde=-1,  # vers ou doit pointer le bras (1 : droite, -1 : gauche)
        peau=2  # bras du perso, 1 : joueur 1, 2 : joueur 2
    )

    chargement_etapes += 1
    chargement()

    return joueur1, bras1, joueur2, bras2


def main(theme: str, id_niveau: int):
    clock = pg.time.Clock()
    tour = 1

    chargement()

    monde, fond = chargement_niveau(theme, id_niveau)
    texture_joueurs, texture_bras = chargement_textures(theme)
    toutes_les_images = pg.sprite.RenderUpdates()
    joueur1, bras1, joueur2, bras2 = application_texture(
        monde,
        texture_joueurs, texture_bras,
        toutes_les_images
    )

    # Si on arrive ici, c'est que tout a été chargé donc on vire la barre de
    # chargement en forcant l'affichage sur la fenetre du fond qui vient 
    # d'etre chargé
    fenetre.blit(fond, (0, 0))
    pg.display.flip()

    text = pg.font.Font(None, 20)
    text.set_italic(True)

    Angle.containers = toutes_les_images
    Energie.containers = toutes_les_images

    angle_gui = Angle()
    energie_gui = Energie()

    joueurs = {
        1: [joueur1, bras1],
        2: [joueur2, bras2],
    }

    if pg.font:
        toutes_les_images.add(angle_gui)
        toutes_les_images.add(energie_gui)

    while joueurs.get(tour)[0].alive():
        pg.display.set_caption(f"Tank! - fps:{round(clock.get_fps())}")
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return

        touche_presse = pg.key.get_pressed()
        toutes_les_images.clear(fenetre, fond)
        toutes_les_images.update()

        if joueurs.get(tour)[0].energie > 0:
            direction = touche_presse[pg.K_RIGHT] - touche_presse[pg.K_LEFT]

            joueurs.get(tour)[0].move(direction, monde.hit_box())

            joueurs.get(tour)[1].move(direction)
            energie_gui.energie = joueurs.get(tour)[0].energie

        if not joueurs.get(tour)[0].is_shooting:
            # player.get(turn)[0].rotate(keystate[pg.K_UP] - keystate[pg.K_DOWN])
            joueurs.get(tour)[1].rotate(
                touche_presse[pg.K_UP] - touche_presse[pg.K_DOWN])
            angle_gui.angle = joueurs.get(tour)[1].angle

            if touche_presse[pg.K_SPACE]:
                joueurs.get(tour)[0].is_shooting = True
                tomato = Tomato(
                    screen_rect=fenetre.get_rect(),
                    velocity=150, x=joueurs.get(tour)[0].get_pos()[0],
                    y=joueurs.get(tour)[0].get_pos()[1],
                    direction=joueurs.get(tour)[0].regarde,
                    angle=joueurs.get(tour)[1].angle,
                    adv=joueurs.get(tour % 2 + 1)[0].get_pos(),
                    world=monde.hit_box()
                )
                tomato.update()

        floor = toutes_les_images.draw(fenetre)
        pg.display.update(floor)

        clock.tick(20)

    pg.time.wait(1000)
    pg.quit()


if __name__ == "__main__":
    try:
        main("bob", 1)
    except KeyboardInterrupt:
        pg.quit()
        quit()
