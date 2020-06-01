from Class.Armes import Type1, Type2, Type3
from Class.GUI import VieGUI, EnergieGUI, ArmeGUI, TourGUI, AideGUI
from Class.Menu import Menu
from autre.utils import *

pg.init()
fenetre = pg.display.set_mode(RESOLUTION.size)

chargement(fenetre, 0)


def main(theme: str, id_niveau: int) -> dict:
    """
    Fonction mère de tout le projet

    Args :
        theme (str) : thème choisi par l'utilisateur
        id_niveau (int) : id du terrain (1 ou 2)

    Returns :
        (dict) : stats de jeu (gagnant, nom de tour, vie)
    """
    clock = pg.time.Clock()
    tour = 1
    tour_total = 1

    chargement(fenetre, 1)

    monde, fond = chargement_niveau(fenetre, theme, id_niveau)
    texture_joueurs, texture_bras = chargement_textures(fenetre, theme)
    toutes_les_images = pg.sprite.RenderUpdates()
    joueur1_corps, joueur1_bras, joueur2_corps, joueur2_bras = \
        application_texture(
            fenetre, monde, texture_joueurs, texture_bras, toutes_les_images
        )

    # Si on arrive ici, c'est que tout a été chargé donc on vire la barre de
    # chargement en forcant l'affichage sur la fenetre du fond qui vient
    # d'etre chargé
    fenetre.blit(fond, (0, 0))
    pg.display.flip()

    texte = pg.font.Font(None, 20)
    texte.set_italic(True)

    armes = [Type1, Type2, Type3]

    joueur1_energie = EnergieGUI(fenetre.get_rect(), joueur1_corps)
    joueur2_energie = EnergieGUI(fenetre.get_rect(), joueur2_corps)

    joueur1_vie = VieGUI(fenetre.get_rect(), joueur1_corps)
    joueur2_vie = VieGUI(fenetre.get_rect(), joueur2_corps)

    joueurs = {
        1: [joueur1_corps, joueur1_bras, joueur1_energie, joueur1_vie,
            armes[0]],
        2: [joueur2_corps, joueur2_bras, joueur2_energie, joueur2_vie,
            armes[0]],
    }

    arme_gui = ArmeGUI(theme)
    tour_gui = TourGUI()

    Type1.containers = toutes_les_images
    Type2.containers = toutes_les_images
    Type3.containers = toutes_les_images

    if pg.font:
        toutes_les_images.add(arme_gui)
        toutes_les_images.add(tour_gui)

        toutes_les_images.add(joueurs.get(1)[2])
        toutes_les_images.add(joueurs.get(2)[2])

        toutes_les_images.add(joueurs.get(1)[3])
        toutes_les_images.add(joueurs.get(2)[3])

        toutes_les_images.add(AideGUI())

    while joueurs.get(tour)[0].vie > 0:
        pg.display.set_caption(
            f"Projet Transverse! - fps:{round(clock.get_fps())}")
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                return {
                    "vie": {
                        1: joueurs.get(1)[0].vie,
                        2: joueurs.get(2)[0].vie,
                    },
                    "tour": tour_total
                }

        tour_gui.tour = tour
        arme_gui.arme = armes.index(joueurs.get(tour)[4]) + 1

        touche_presse = pg.key.get_pressed()
        toutes_les_images.clear(fenetre, fond)
        toutes_les_images.update()

        if joueurs.get(tour)[0].energie > 0:
            direction = touche_presse[pg.K_RIGHT] - touche_presse[pg.K_LEFT]

            joueurs.get(tour)[0].move(direction, monde.hit_box())
            joueurs.get(tour)[1].move(direction, monde.hit_box())
            joueurs.get(tour)[2].move(not joueurs.get(tour)[0].is_shooting)
            joueurs.get(tour)[3].move()

            joueurs.get(tour)[2].energie = joueurs.get(tour)[0].energie

        if not joueurs.get(tour)[0].is_shooting:
            if "projectile" in locals():
                pg.time.wait(1000)
                projectile.kill()
                del projectile

            joueurs.get(tour)[1].rotate(
                touche_presse[pg.K_UP] - touche_presse[pg.K_DOWN]
            )

            # changement d'arme (si la touche "a" est pressé, on prend l'arme
            # precedent, si c'est "z", on prend la suivante
            if touche_presse[pg.K_a]:
                selection = armes.index(joueurs.get(tour)[4])

                if selection == 0:
                    selection = len(armes) - 1
                else:
                    selection -= 1

                joueurs.get(tour)[4] = armes[selection]

                pg.time.wait(200)
            elif touche_presse[pg.K_z]:
                selection = armes.index(joueurs.get(tour)[4])

                if selection == len(armes) - 1:
                    selection = 0
                else:
                    selection += 1

                joueurs.get(tour)[4] = armes[selection]
                arme_gui.arme = selection + 1

                pg.time.wait(200)
            elif touche_presse[pg.K_i]:
                info = Menu(fenetre, couleur_fond=(105, 105, 105))
                info.ajout_texte(
                    None,
                    (190, 190, 70),
                    f"Info sur l'arme choisie: ",
                    (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 150),
                )
                info.ajout_image(
                    arme_gui.image,
                    (RESOLUTION.size[0] // 2 + 40,
                     RESOLUTION.size[1] // 2 - 80),
                )
                info.ajout_texte(
                    None,
                    (190, 190, 70),
                    f"Portée: {joueurs.get(tour)[4].velocity}",
                    (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 20),
                )
                info.ajout_texte(
                    None,
                    (190, 190, 70),
                    f"Dégats: {joueurs.get(tour)[4].degats}",
                    (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 + 20),
                )
                info.rerendre()
                pg.display.flip()

                pg.time.wait(2000)
                fenetre.blit(fond, (0, 0))
                pg.display.flip()

            # feu !
            if touche_presse[pg.K_SPACE]:
                joueurs.get(tour)[0].is_shooting = True
                projectile = joueurs.get(tour)[4](
                    screen_rect=fenetre.get_rect(),
                    x=joueurs.get(tour)[0].get_pos()[0],
                    y=joueurs.get(tour)[0].get_pos()[1],
                    direction=joueurs.get(tour)[0].regarde,
                    angle=joueurs.get(tour)[1].angle,
                    adversaire=joueurs.get(tour % 2 + 1)[0],
                    monde=monde.hit_box(),
                    theme=theme,
                )

                # on remet le fond de la jauge d'endurance du perso en noir
                # parce que ce n'est plus à lui de jouer
                joueurs.get(tour)[2].fond_couleur = (0, 0, 0)

        elif projectile.hit[0]:
            joueurs.get(tour)[0].is_shooting = False
            joueurs.get(tour)[0].energie = 100

            if projectile.hit[1]:
                joueurs.get(tour % 2 + 1)[0].vie -= projectile.degats

            if joueurs.get(tour % 2 + 1)[0].vie <= 0:
                return {
                    "vie": {
                        1: joueurs.get(1)[0].vie,
                        2: joueurs.get(2)[0].vie,
                    },
                    "tour": tour_total
                }

            tour = tour % 2 + 1
            tour_total += 1

        floor = toutes_les_images.draw(fenetre)
        pg.display.update(floor)

        clock.tick(20)


if __name__ == "__main__":
    try:
        main("bob", 1)
    except KeyboardInterrupt:
        pg.quit()
        quit()
    except Exception as e:
        crash(fenetre, e)
