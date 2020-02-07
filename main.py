import pygame
from world import World


def format_time(time: int) -> str:
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)

    return f"{h}h {m}m {s}s"


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    r, g, b = 220, 208, 255

    world = World()
    world.load_map('1')

    screen = pygame.display.set_mode(world.screen_size())
    screen.fill((r, g, b))

    is_running = True
    timer = 0

    pos = [[0, 0], [0, 0]]

    try:
        while is_running:
            screen = world.display_map(screen, pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        pos[0][0] += 1
                    if event.key == pygame.K_DOWN:
                        pos[0][0] -= 1

                    if event.key == pygame.K_RIGHT:
                        pos[0][1] += 1
                    if event.key == pygame.K_LEFT:
                        pos[0][1] -= 1

            if pygame.time.get_ticks() - timer > 1000:
                timer = pygame.time.get_ticks()
                pygame.display.set_caption(
                    f"Tank! "
                    f"fps:{round(clock.get_fps())}, "
                    f"started {format_time(pygame.time.get_ticks()//1000)} ago"
                )
            world.move_player(screen, pos)
            clock.tick(60)

    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()
