import pygame
import snake
import time

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
DRAWING_WIDTH = 3
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255,165,0)
BLUE = (0, 0, 255)
REFRESH_RATE = 60
DRAWING_ANGLE = 3


def main():
    """
    Add Documentation here
    """
    snake1 = snake.Snake(50, (200, 200), GREEN, DRAWING_ANGLE)
    pygame.init()
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.mixer.init()
    pygame.display.set_caption("game, shalom")
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    finish = False
    pygame.display.flip()
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    snake1.swich_direction()
        draw_params = snake1.get_draw_params(screen)
        print draw_params
        if draw_params[3] < draw_params[4]:
            pygame.draw.arc(draw_params[0], draw_params[1], draw_params[2],
                        draw_params[3], draw_params[4], DRAWING_WIDTH)
        else:
            pygame.draw.arc(draw_params[0], draw_params[1], draw_params[2],
                            draw_params[4], draw_params[3], DRAWING_WIDTH)
        print "i drew"
        x, y = snake1.draw_update()
        print x, y
        pygame.display.flip()
        time.sleep(0.05)
        clock.tick(REFRESH_RATE)
    pygame.quit()


if __name__ == '__main__':
    main()