import pygame


class Ball:
    RADIUS = 12

    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

    def show(self, color):
        pygame.draw.circle(self.screen, color, (self.x, self.y), self.RADIUS)


class Player:
    WIDTH = 15
    HEIGHT = 100
    PAD = 5

    HIDE = pygame.Color("black")
    SHOW = pygame.Color("white")

    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

    def show(self, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(
            self.x - self.WIDTH - self.PAD, self.y - self.HEIGHT // 2, self.WIDTH, self.HEIGHT))

    def move_down(self):
        self.show(self.HIDE)
        self.y += 10
        self.show(self.SHOW)

    def move_up(self):
        self.show(self.HIDE)
        self.y -= 10
        self.show(self.SHOW)


WIDTH = 1200
HEIGHT = 600
BORDER = 20

fgColor = pygame.Color("white")

FRAMERATE = 30


def move(event, player1, player2, controls):
    """
        moves the player depending on what key was pressed
    """
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            controls["up"] = True
        if event.key == pygame.K_DOWN:
            controls["down"] = True
        if event.key == pygame.K_w:
            controls["w"] = True
        if event.key == pygame.K_s:
            controls["s"] = True
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
            controls["up"] = False
        if event.key == pygame.K_DOWN:
            controls["down"] = False
        if event.key == pygame.K_w:
            controls["w"] = False
        if event.key == pygame.K_s:
            controls["s"] = False

    if controls["up"]:
        player1.move_up()
    if controls["down"]:
        player1.move_down()
    if controls["s"]:
        player2.move_down()
    if controls["w"]:
        player2.move_up()


def draw_background(screen):
    """
        Draws the background for the game
    """
    pygame.draw.rect(screen, fgColor, pygame.Rect(0, 0, WIDTH, BORDER))
    pygame.draw.rect(screen, fgColor, pygame.Rect(0, 0, HEIGHT, BORDER))
    pygame.draw.rect(screen, fgColor, pygame.Rect(
        0, HEIGHT - BORDER, WIDTH, BORDER))


def main():
    # start the game screen
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # dictionary to update player movements
    pressed_keys = {"w": False, "s": False, "down": False, "up": False}

    # create the ball
    ball = Ball(WIDTH // 2, HEIGHT // 2, screen)

    # crate the players
    player1 = Player(WIDTH, HEIGHT // 2, screen)
    player2 = Player(25, HEIGHT // 2, screen)

    draw_background(screen)

    player1.show(fgColor)
    player2.show(fgColor)

    while True:
        event = pygame.event.poll()

        # check if the window was closed
        if event.type == pygame.QUIT:
            break

        move(event, player1, player2, pressed_keys)

        pygame.display.flip()
        clock.tick(FRAMERATE)

    pygame.quit()


if __name__ == "__main__":
    main()
