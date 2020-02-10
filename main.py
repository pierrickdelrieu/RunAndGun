from objects.constants import *
from objects.player import Player, Cannon, Fuel
from objects.world import World


def main():
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()

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

    background = World()
    background.load_map(1)
    background.save_map()

    background = pg.Surface(SCREENRECT.size)
    background.blit(pg.image.load(f"resources/levels/1.png").convert_alpha(), (0, 0))
    screen.blit(background, (0, 0))
    pg.display.flip()

    all_sprites = pg.sprite.RenderUpdates()
    clock = pg.time.Clock()

    Player.containers = all_sprites
    Cannon.containers = all_sprites
    Fuel.containers = all_sprites

    player = Player(screen.get_rect())
    cannon = Cannon(screen.get_rect())
    fuel = Fuel(screen.get_rect())

    while player.alive():
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                return

        keystate = pg.key.get_pressed()
        all_sprites.clear(screen, background)
        all_sprites.update()

        if player.fuel > 0:
            direction = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
            player.move(direction)
            fuel.move(direction, player.fuel)
            cannon.move(direction)

        cannon.rotate(keystate[pg.K_UP] - keystate[pg.K_DOWN])

        floor = all_sprites.draw(screen)
        pg.display.update(floor)

        pg.display.set_caption(f"Tank! - fps:{round(clock.get_fps())}")

        clock.tick(30)

    pg.time.wait(1000)
    pg.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pg.quit()
        quit()
