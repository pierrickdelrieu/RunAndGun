from Class.armes import Tomato
from Class.constants import *
from Class.gui import Angle, Energy
from Class.joueur import Joueur, Bras
from Class.monde import World


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
    texture_joueurs = [
        # Joueur 1
        {   # -1 Pour quand le joueur regarde a gauche
            -1: pg.transform.flip(
                pg.transform.scale(
                    pg.image.load(
                        f"themes/{theme}/joueur/1/corps.png"
                    ).convert_alpha(),
                    (LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
                ),
                True, False
            ),
            # 1 Pour quand il regarde a droite
            1: pg.transform.scale(
                pg.image.load(
                    f"themes/{theme}/joueur/1/corps.png"
                ).convert_alpha(),
                (LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
            )
        },

        # Joueur 2
        {   # -1 Pour quand le joueur regarde a gauche
            -1: pg.transform.flip(
                pg.transform.scale(
                    pg.image.load(
                        f"themes/{theme}/joueur/2/corps.png"
                    ).convert_alpha(),
                    (LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
                ),
                True, False
            ),
            # 1 Pour quand il regarde a droite
            1: pg.transform.scale(
                pg.image.load(
                    f"themes/{theme}/joueur/2/corps.png"
                ).convert_alpha(),
                (LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
            )
        }
    ]

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
                f"themes/{theme}/joueur/1/bras/{i}.png"
            ).convert_alpha(),
            (LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
        )
        image_joueur2 = pg.transform.scale(
            pg.image.load(
                f"themes/{theme}/joueur/2/bras/{i}.png"
            ).convert_alpha(),
            (LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
        )

        texture_bras[0][-1][i] = pg.transform.flip(image_joueur1, True, False)
        texture_bras[0][-1][i] = image_joueur1

        texture_bras[0][-1][i] = pg.transform.flip(image_joueur2, True, False)
        texture_bras[0][-1][i] = image_joueur2

    return texture_joueurs, texture_bras


def main(theme: str):
    pg.init()
    clock = pg.time.Clock()
    tour = 1

    screen = pg.display.set_mode(RESOLUTION.size)

    text = pg.font.Font(None, 20)
    text.set_italic(True)

    world = World(theme)
    world.chargement_map(1)
    world.save_map()

    background = pg.Surface(RESOLUTION.size)
    background.blit(
        pg.image.load(f"resources/levels/{level}/map.png").convert_alpha(),
        (0, 0))
    screen.blit(background, (0, 0))
    pg.display.flip()

    all_sprites = pg.sprite.RenderUpdates()

    Joueur.containers = all_sprites
    Bras.containers = all_sprites
    Tomato.containers = all_sprites

    Angle.containers = all_sprites
    Energy.containers = all_sprites

    player1 = Joueur(screen.get_rect(), world.level.players.get(1), 1,
                     'patrick')
    player2 = Joueur(screen.get_rect(), world.level.players.get(2), -1, 'bob')

    arm1 = Bras(screen.get_rect(), world.level.players.get(1), 1, 'patrick')
    arm2 = Bras(screen.get_rect(), world.level.players.get(2), -1, 'bob')

    angle_gui = Angle()
    fuel_gui = Energy()

    player = {
        1: [player1, arm1],
        2: [player2, arm2],
    }

    if pg.font:
        all_sprites.add(angle_gui)
        all_sprites.add(fuel_gui)

    while player.get(turn)[0].alive():
        pg.display.set_caption(f"Tank! - fps:{round(clock.get_fps())}")
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return

        keystate = pg.key.get_pressed()
        all_sprites.clear(screen, background)
        all_sprites.update()

        if player.get(turn)[0].energy > 0:
            direction = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]

            player.get(turn)[0].move(direction, world.hit_box())

            player.get(turn)[1].move(direction)
            fuel_gui.energy = player.get(turn)[0].energy

        if not player.get(turn)[0].is_shooting:
            # player.get(turn)[0].rotate(keystate[pg.K_UP] - keystate[pg.K_DOWN])
            player.get(turn)[1].rotate(keystate[pg.K_UP] - keystate[pg.K_DOWN])
            angle_gui.angle = player.get(turn)[1].angle

            if keystate[pg.K_SPACE]:
                player.get(turn)[0].is_shooting = True
                tomato = Tomato(
                    screen_rect=screen.get_rect(),
                    velocity=150, x=player.get(turn)[0].get_pos()[0],
                    y=player.get(turn)[0].get_pos()[1],
                    direction=player.get(turn)[0].facing,
                    angle=player.get(turn)[1].angle,
                    adv=player.get(turn % 2 + 1)[0].get_pos(),
                    world=world.hit_box()
                )
                tomato.update()

        floor = all_sprites.draw(screen)
        pg.display.update(floor)

        clock.tick(20)

    pg.time.wait(1000)
    pg.quit()


if __name__ == "__main__":
    try:
        main("bob")
    except KeyboardInterrupt:
        pg.quit()
        quit()
