from objects.constants import *
from objects.player import Player, Cannon, Fuel
from objects.weapons import Tomato
from objects.world import World
from objects.gui import Angle


def main():
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    clock = pg.time.Clock()

    level = 1
    turn = 1

    screen = pg.display.set_mode(SCREENRECT.size)

    img = pg.transform.scale(
        pg.image.load(f"resources/sprites/tank.png").convert_alpha(),
        (72, (72 * 178) // 489)
    )
    Player.images = [
        pg.transform.flip(
            img,
            True, False
        ),
        img
    ]
    Player.fuel = 100

    img = pg.transform.scale(
        pg.image.load(f"resources/sprites/cannon.png").convert_alpha(),
        (72, (72 * 178) // 489)
    )
    Cannon.images = [
        pg.transform.flip(
            img,
            True, False
        ),
        img
    ]

    text = pg.font.Font(None, 20)
    text.set_italic(True)
    Fuel.fuel = 100
    Fuel.images = [
        text.render(f"Fuel: {Player.fuel}%", 0, (0, 0, 0))
    ]

    img = pg.transform.scale(
        pg.image.load(f"resources/sprites/bullets/tomato.png").convert_alpha(),
        (16, 16)
    )
    Tomato.images = [
        img
    ]
    Tomato.clock = clock

    world = World()
    world.load_map(level)
    world.save_map()

    background = pg.Surface(SCREENRECT.size)
    background.blit(pg.image.load(f"resources/levels/{level}/map.png").convert_alpha(), (0, 0))
    screen.blit(background, (0, 0))
    pg.display.flip()

    all_sprites = pg.sprite.RenderUpdates()

    Player.containers = all_sprites
    Cannon.containers = all_sprites
    Fuel.containers = all_sprites
    Tomato.containers = all_sprites

    Angle.containers = all_sprites

    player1 = Player(screen.get_rect(), world.level.players.get(1), 1)
    player2 = Player(screen.get_rect(), world.level.players.get(2), -1)

    cannon1 = Cannon(screen.get_rect(), world.level.players.get(1), 1)
    cannon2 = Cannon(screen.get_rect(), world.level.players.get(2), -1)

    fuel1 = Fuel(screen.get_rect(), world.level.players.get(1))
    fuel2 = Fuel(screen.get_rect(), world.level.players.get(2))

    angle_gui = Angle()

    player = {
        1: [player1, cannon1, fuel1],
        2: [player2, cannon2, fuel2],
    }

    if pg.font:
        all_sprites.add(angle_gui)

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
            player.get(turn)[2].move(direction, player.get(turn)[0].fuel)
            player.get(turn)[1].move(direction)

        if not player.get(turn)[0].is_shooting:
            player.get(turn)[1].rotate(keystate[pg.K_UP] - keystate[pg.K_DOWN])
            angle_gui.angle = player.get(turn)[1].angle

            if keystate[pg.K_SPACE]:
                player.get(turn)[0].is_shooting = True
                tomato = Tomato(
                    screen.get_rect(),
                    150, *player.get(turn)[1].get_pos(),
                    player.get(turn)[1].facing,
                    player.get(turn)[1].angle
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
