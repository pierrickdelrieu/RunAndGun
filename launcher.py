from autre.utils import *
from Class.Menu import Menu
from main import main

pg.init()
fenetre = pg.display.set_mode(RESOLUTION.size)

themes = {
    1: 'bob',
    2: 'mario',
    3: 'minecraft',
    4: 'pokemon',
    5: 'star_wars',
}
theme_choisi = 1
niveau_choisi = 1


def quitter():
    pg.quit()
    quit()


def page_game_over(_fenetre, resultat: dict) -> Menu:
    """
    Page de game over avec les stats de jeu affichées

    Args :
        _fenetre : -
        resultat (dict) : stats de jeu retournées par la fonction mère `main`

    Returns :
        (Menu) : menu à afficher
    """

    if resultat.get('vie')[1] <= 0:
        gagnant = 2
    else:
        gagnant = 1

    _menu = Menu(_fenetre, couleur_fond=(155, 155, 255))

    _menu.ajout_texte(
        None,
        (0, 0, 0),
        "Game Over !",
        (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 200),
        taille_police=84
    )

    _menu.ajout_texte(
        None,
        (0, 0, 0),
        f"Le joueur {gagnant} a gagné contre le joueur {gagnant % 2 + 1}"
        f" en {resultat.get('tour')} tours !",
        (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 150),
        taille_police=42
    )

    _menu.ajout_texte(
        None,
        (0, 0, 0),
        f"Vie du joueur 1: {resultat.get('vie')[1]}",
        (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 110),
        taille_police=42
    )
    _menu.ajout_texte(
        None,
        (0, 0, 0),
        f"Vie du joueur 2: {resultat.get('vie')[2]}",
        (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 80),
        taille_police=42
    )

    _menu.ajout_texte(
        None,
        (0, 0, 0),
        f"Appuyez sur `echap` pour quitter",
        (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 + 180),
        taille_police=24
    )

    _menu.rerendre()
    pg.display.flip()

    return _menu


def page_choix_terrain(_fenetre) -> Menu:
    """
    Page de choix du terrain

    Args :
        _fenetre : -

    Returns :
        (Menu) : menu à afficher
    """

    global niveau_choisi
    _menu = Menu(_fenetre, couleur_fond=(155, 155, 255))

    def retour():
        _menu.supprime()
        return page_choix_theme(_fenetre)

    def jouer():
        _menu.supprime()
        return page_game_over(
            _fenetre,
            main(themes[theme_choisi], niveau_choisi)
        )

    def changer_terrain():
        global niveau_choisi
        niveau_choisi = 1 if niveau_choisi == 2 else niveau_choisi + 1

        fond = pg.Surface(RESOLUTION.size)
        fond.blit(
            pg.image.load(
                "{}/{}/rendu.png".format(
                    ACCES_TERRAINS.format(themes[theme_choisi]),
                    niveau_choisi
                )
            ).convert_alpha(),
            (0, 0),
        )
        _fenetre.blit(fond, (0, 0))

        _menu.supprime()

        _menu.ajout_texte(
            None,
            (0, 0, 0),
            "Choix du terrain",
            (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 200),
            taille_police=84
        )
        _menu.ajout_texte(
            None,
            (0, 0, 0),
            f"choix: {themes[theme_choisi].capitalize().replace('_', ' ')}",
            (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 150),
            taille_police=42
        )
        _menu.ajout_texte(
            None,
            (0, 0, 0),
            f"terrain: {niveau_choisi}",
            (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 125),
            taille_police=42
        )

        _menu.ajout_bouton(
            pg.image.load("./autre/menu/bouton_play.png"),
            (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 25),
            jouer,
            identifiant="jouer",
        )
        _menu.ajout_bouton(
            pg.image.load("./autre/menu/bouton_changer.png"),
            (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 + 25),
            changer_terrain,
            identifiant="terrain",
        )

        _menu.ajout_bouton(
            pg.image.load("./autre/menu/bouton_retour.png"),
            (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 + 110),
            retour,
            identifiant="retour",
        )

        _menu.rerendre()
        pg.display.flip()

    changer_terrain()

    return _menu


def page_choix_theme(_fenetre) -> Menu:
    """
    Page de choix du niveau

    Args :
        _fenetre : -

    Returns :
        (Menu) : menu à afficher
    """

    global theme_choisi
    _menu = Menu(_fenetre, couleur_fond=(155, 155, 255))

    def choisir_terrain():
        _menu.supprime()
        return page_choix_terrain(_fenetre)

    def changer_theme():
        global theme_choisi
        theme_choisi = 1 if theme_choisi == len(themes) else theme_choisi + 1

        fond = pg.Surface(RESOLUTION.size)
        fond.blit(
            pg.image.load(
                "{}/fond.png".format(ACCES_TERRAINS.format(themes[theme_choisi]))
            ).convert_alpha(),
            (0, 0),
        )
        _fenetre.blit(fond, (0, 0))

        _menu.supprime()

        _menu.ajout_texte(
            None,
            (0, 0, 0),
            "Choix du theme",
            (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 200),
            taille_police=84
        )
        _menu.ajout_texte(
            None,
            (0, 0, 0),
            f"choix: {themes[theme_choisi].capitalize().replace('_', ' ')}",
            (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 150),
            taille_police=42
        )

        _menu.ajout_bouton(
            pg.image.load("./autre/menu/bouton_choisir.png"),
            (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 25),
            choisir_terrain,
            identifiant="suivant",
        )
        _menu.ajout_bouton(
            pg.image.load("./autre/menu/bouton_changer.png"),
            (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 + 25),
            changer_theme,
            identifiant="theme",
        )

        _menu.rerendre()
        pg.display.flip()

    changer_theme()

    return _menu


def page_accueil(_fenetre) -> Menu:
    """
    Page d'accueil du jeu

    Args :
        _fenetre : -

    Returns :
        (Menu) : menu à afficher
    """

    def start():
        _menu.supprime()
        return page_choix_theme(_fenetre)

    fond = pg.Surface(RESOLUTION.size)
    _fenetre.blit(fond, (0, 0))
    pg.display.flip()

    _menu = Menu(_fenetre, couleur_fond=(155, 155, 255))

    _menu.ajout_texte(
        _menu.couleur_fond,
        (0, 0, 0),
        "Projet Transverse !",
        (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 200),
        taille_police=84
    )

    _menu.ajout_bouton(
        pg.image.load("./autre/menu/bouton_play.png"),
        (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 25),
        start,
        identifiant="suivant",
    )
    _menu.ajout_bouton(
        pg.image.load("./autre/menu/bouton_quitter.png"),
        (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 + 25),
        quitter,
        identifiant="quit",
    )

    _menu.rerendre()

    return _menu


if __name__ == "__main__":
    clock = pg.time.Clock()
    menu = page_accueil(fenetre)
    pg.display.flip()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                pg.quit()
                quit()

        action = menu.bouton_press()

        if action is not None and action[0]:
            if action[1] in ['suivant', 'retour']:
                menu = action[2]

        clock.tick(20)
