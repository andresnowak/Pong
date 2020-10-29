import pygame


class Ball:
    RADIUS = 20

    HIDE = pygame.Color("black")  # color to hide the ball with background
    SHOW = pygame.Color("white")  # color tho show the ball

    def __init__(self, x, y, vx, vy, screen):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

        self.ball = pygame.Rect(x, y, self.RADIUS, self.RADIUS)

        self.screen = screen

    def show(self, color):
        pygame.draw.ellipse(self.screen, color, self.ball)

    def move(self, player1Rect, player2Rect, player1, player2):
        """
            moves the ball
        """
        global BORDER
        global HEIGHT
        global WIDTH

        new_pos_x = self.ball.x + self.vx
        new_pos_y = self.ball.y + self.vy

        self.show(self.HIDE)

        # update position of ball
        self.ball.x = new_pos_x
        self.ball.y = new_pos_y

        if self.ball.top <= BORDER or self.ball.bottom >= HEIGHT - BORDER:
            self.vy *= -1

        if self.ball.top <= BORDER:
            self.ball.top = BORDER
        elif self.ball.bottom >= HEIGHT - BORDER:
            self.ball.bottom = HEIGHT - BORDER

        if self.ball.right > WIDTH:
            self.ball.x = WIDTH // 2
            self.ball.y = HEIGHT // 2
            player1.points += 1
        elif self.ball.left < 0:
            self.ball.x = WIDTH // 2
            self.ball.y = HEIGHT // 2
            player2.points += 1

        self.crashed(player1Rect, player2Rect)

        self.show(self.SHOW)

    def crashed(self, player1, player2):
        """
            Check if the ball has crashed with a player to bounce
        """

        if self.ball.colliderect(player1) or self.ball.colliderect(player2):
            self.vx *= -1

        if self.ball.colliderect(player1):
            self.ball.right = player1.left
        elif self.ball.colliderect(player2):
            self.ball.left = player2.right


class Player:
    WIDTH = 15
    HEIGHT = 100
    points = 0

    HIDE = pygame.Color("black")  # color to hide the player with background
    SHOW = pygame.Color("white")  # color tho show the player

    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

        self.player = pygame.Rect(
            self.x - self.WIDTH, self.y - self.HEIGHT // 2, self.WIDTH, self.HEIGHT)

    def show(self, color):
        pygame.draw.rect(self.screen, color, self.player)

    def move(self, movement):
        """
            Moves the player
        """
        global BORDER
        global HEIGHT

        # the amount of pixels the player moves
        move = 4

        # the amount of pixels the player moves
        if movement == "up":
            move *= -1
        elif movement == "down":
            move *= 1

        # hide the player
        self.show(self.HIDE)

        # move it
        self.player.y += move

        # check if the player is gonna pass the borders of the game
        if self.player.bottom >= HEIGHT - BORDER:
            self.player.bottom = HEIGHT - BORDER
        if self.player.top <= BORDER:
            self.player.top = BORDER

        # show player
        self.show(self.SHOW)

    def get_rect(self):
        return self.player


WIDTH = 1200
HEIGHT = 600
BORDER = 20

fgColor = pygame.Color("white")

FRAMERATE = 60


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
        player1.move("up")
    if controls["down"]:
        player1.move("down")
    if controls["s"]:
        player2.move("down")
    if controls["w"]:
        player2.move("up")


def draw_background(screen):
    """
        Draws the background for the game
    """
    pygame.draw.rect(screen, fgColor, pygame.Rect(0, 0, WIDTH, BORDER))
    pygame.draw.rect(screen, fgColor, pygame.Rect(0, 0, HEIGHT, BORDER))
    pygame.draw.rect(screen, fgColor, pygame.Rect(
        0, HEIGHT - BORDER, WIDTH, BORDER))

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

def main():
    # start the game screen
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    pygame.display.set_caption("Pong")

    # speed for ball
    ball_vx = 6
    ball_vy = 6

    # dictionary to update player movements
    pressed_keys = {"w": False, "s": False, "down": False, "up": False}

    # create the ball
    ball = Ball(WIDTH // 2, HEIGHT // 2, ball_vx, ball_vy, screen)

    # crate the players
    player1 = Player(WIDTH, HEIGHT // 2, screen)
    player2 = Player(15, HEIGHT // 2, screen)

    draw_background(screen)

    ball.show(fgColor)
    starts = True
    player1.show(fgColor)
    player2.show(fgColor)

    while True:
        event = pygame.event.poll()

        # check if the window was closed
        if event.type == pygame.QUIT:
            pygame.quit()
            break

        move(event, player1, player2, pressed_keys)

        ball.move(player1.get_rect(), player2.get_rect(), player1, player2)

        if starts:
            textsurface = myfont.render("Points: " + str(player1.points) + " - " + str(player2.points), 1, (0, 0, 0))
            screen.blit(textsurface, (0, 0))
            tempPoints1 = player1.points
            tempPoints2 = player2.points
            starts = False
        elif tempPoints1 != player1.points or tempPoints2 != player2.points:
            screen.fill(pygame.Color("white"), (0, 0, 150, 20))
            textsurface = myfont.render("Points: " + str(tempPoints1) + " - " + str(tempPoints2), 1, (255, 255, 255))
            screen.blit(textsurface, (0, 0))
            textsurface = myfont.render("Points: " + str(player1.points) + " - " + str(player2.points), 1, (0, 0, 0))
            screen.blit(textsurface, (0, 0))
            tempPoints1 = player1.points
            tempPoints2 = player2.points

        pygame.display.flip()
        clock.tick(FRAMERATE)


if __name__ == "__main__":
    main()
