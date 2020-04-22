from autre.constants import *
from Class.Menu import Menu

pg.init()
fenetre = pg.display.set_mode(RESOLUTION.size)


def callback():
    print("callback")


def themes(theme: tuple):
    print(theme)


def quitter():
    pg.quit()
    quit()


if __name__ == "__main__":
    clock = pg.time.Clock()
    menu = Menu(
        fenetre,
        couleur_fond=(155, 155, 255)
    )

    menu.ajout_texte(
        menu.couleur_fond,
        (190, 190, 70),
        "Sourcecodester",
        (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 200),
    )

    menu.ajout_bouton(
        menu.couleur_fond,
        (255, 255, 255),
        "START",
        (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 - 40),
        callback,
        identifiant="start"
    )
    menu.ajout_bouton(
        menu.couleur_fond,
        (255, 255, 255),
        "THEME: ",
        (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2),
        themes,
        type_bouton="select",
        options=[
            ("Bob l'eponge", "bob"),
            ("Mario", "mario"),
            ("Minecraft", "minecraft"),
            ("Star Wars", "star_wars"),
        ],
        identifiant="theme"
    )
    menu.ajout_bouton(
        menu.couleur_fond,
        (0, 0, 0),
        "QUIT",
        (RESOLUTION.size[0] // 2, RESOLUTION.size[1] // 2 + 40),
        quitter,
        identifiant="quit"
    )

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                quit()

        action = menu.bouton_press()

        if action is not None and action[0] != 0:
            ...

        clock.tick(20)
