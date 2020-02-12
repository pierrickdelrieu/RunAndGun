from objects.constants import *
from objects.player import Player, Life
from objects.weapons import Tomato
from objects.world import World
from objects.gui import Angle, Fuel


def main():
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    clock = pg.time.Clock()

    level = 1
    turn = 2

    screen = pg.display.set_mode(SCREENRECT.size)

    img = {-1: {}, 1: {}}
    for i in range(-4, 17, 2):
        img[-1][i] = pg.transform.flip(
            pg.transform.scale(
                pg.image.load(f"resources/sprites/player/{i}.png").convert_alpha(),
                (96, (96 * 215) // 631)
            ),
            True, False
        )

        img[1][i] = pg.transform.scale(
            pg.image.load(f"resources/sprites/player/{i}.png").convert_alpha(),
            (96, (96 * 215) // 631)
        )

    Player.images = img
    Player.life = 100
    Player.fuel = 100

    text = pg.font.Font(None, 20)
    text.set_italic(True)
    Life.life = 100
    Life.images = [
        text.render(f"Life: {Player.life}%", 0, (0, 0, 0))
    ]

    img = pg.transform.scale(
        pg.image.load(f"resources/sprites/bullets/tomato.png").convert_alpha(),
        (16, 16)
    )
    Tomato.images = [
        img
    ]

    Fuel.fuel = 100

    world = World()
    world.load_map(level)
    world.save_map()

    background = pg.Surface(SCREENRECT.size)
    background.blit(pg.image.load(f"resources/levels/{level}/map.png").convert_alpha(), (0, 0))
    screen.blit(background, (0, 0))
    pg.display.flip()

    all_sprites = pg.sprite.RenderUpdates()

    Player.containers = all_sprites
    Life.containers = all_sprites
    Tomato.containers = all_sprites

    Angle.containers = all_sprites
    Fuel.containers = all_sprites

    player1 = Player(screen.get_rect(), world.level.players.get(1), 1)
    player2 = Player(screen.get_rect(), world.level.players.get(2), -1)

    life1 = Life(screen.get_rect(), world.level.players.get(1))
    life2 = Life(screen.get_rect(), world.level.players.get(2))

    angle_gui = Angle()
    fuel_gui = Fuel()

    player = {
        1: [player1, life1],
        2: [player2, life2],
    }

    if pg.font:
        all_sprites.add(angle_gui)
        all_sprites.add(fuel_gui)

    while player.get(turn)[0].alive():
        pg.display.set_caption(f"Tank! - fps:{round(clock.get_fps())}")
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return

        keystate = pg.key.get_pressed()
        all_sprites.clear(screen, background)
        all_sprites.update()

        if player.get(turn)[0].fuel > 0:
            direction = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
            player.get(turn)[0].move(direction)
            player.get(turn)[1].move(direction, player.get(turn)[0].life)
            fuel_gui.fuel = player.get(turn)[0].fuel

        if not player.get(turn)[0].is_shooting:
            player.get(turn)[0].rotate(keystate[pg.K_UP] - keystate[pg.K_DOWN])
            angle_gui.angle = player.get(turn)[0].angle

            if keystate[pg.K_SPACE]:
                player.get(turn)[0].is_shooting = True
                tomato = Tomato(
                    screen.get_rect(),
                    170, *player.get(turn)[0].get_pos(),
                    player.get(turn)[0].facing,
                    player.get(turn)[0].angle,
                    player.get(turn % 2 + 1)[0].get_pos()
                )
                tomato.update()

        floor = all_sprites.draw(screen)
        pg.display.update(floor)

        clock.tick(20)

    pg.time.wait(1000)
    pg.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pg.quit()
        quit()
