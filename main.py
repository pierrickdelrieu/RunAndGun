from Class.armes import Tomato
from Class.gui import Angle, Energie, Vie

from utils import *

pg.init()
fenetre = pg.display.set_mode(RESOLUTION.size)

chargement(fenetre, 0)


def main(theme: str, id_niveau: int):
    clock = pg.time.Clock()
    tour = 1

    chargement(fenetre, 1)

    monde, fond = chargement_niveau(fenetre, theme, id_niveau)
    texture_joueurs, texture_bras = chargement_textures(fenetre, theme)
    toutes_les_images = pg.sprite.RenderUpdates()
    joueur1_corps, joueur1_bras, joueur2_corps, joueur2_bras = application_texture(
        fenetre, monde,
        texture_joueurs, texture_bras,
        toutes_les_images
    )

    # Si on arrive ici, c'est que tout a été chargé donc on vire la barre de
    # chargement en forcant l'affichage sur la fenetre du fond qui vient 
    # d'etre chargé
    fenetre.blit(fond, (0, 0))
    pg.display.flip()

    texte = pg.font.Font(None, 20)
    texte.set_italic(True)

    angle_gui = Angle()
    energie_gui = Energie()

    joueur1_vie = Vie(fenetre.get_rect(), joueur1_corps)
    joueur2_vie = Vie(fenetre.get_rect(), joueur2_corps)

    joueurs = {
        1: [joueur1_corps, joueur1_bras, joueur1_vie],
        2: [joueur2_corps, joueur2_bras, joueur2_vie],
    }

    if pg.font:
        toutes_les_images.add(angle_gui)
        toutes_les_images.add(energie_gui)
        toutes_les_images.add(joueurs.get(1)[2])
        toutes_les_images.add(joueurs.get(2)[2])

    while joueurs.get(tour)[0].vie > 0:
        pg.display.set_caption(f"Projet Transverse! - fps:{round(clock.get_fps())}")
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
            joueurs.get(tour)[2].move(direction)

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
    except Exception as e:
        crash(fenetre, e)
