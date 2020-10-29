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

    def out_of_bounds(self):
        global WIDTH

        if self.ball.right <= 0:
            return True, "player1"
        elif self.ball.left >= WIDTH:
            return True, "player2"
        else:
            return False, ""

    def spawn(self, x, y):
        """
            spawns the ball to the position it gets in x and y
        """
        # hide the ball
        self.show(self.HIDE)

        self.ball.x = x
        self.ball.y = y

        # show the ball
        self.show(self.SHOW)


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

    def update_points(self):
        self.points += 1

    def spawn(self, x, y):
        """
            spawns the player to the position it gets in x and y
        """
        # hide the player
        self.show(self.HIDE)

        self.player.x = x - self.WIDTH
        self.player.y = y - self.HEIGHT // 2

        # show player
        self.show(self.SHOW)


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

    draw_middle_line(screen)


def draw_middle_line(screen):
    """
        draws the middle line of the game that tells you the space
        of each player
    """
    grey = (200, 200, 200)
    pygame.draw.aaline(screen, grey, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))


def update_score(player1, player2, ball, screen):
    """
        It checks if somebody won and if it happens, it updates the scoreboard
        and spawns the player and ball to default position
    """
    somebody_won, winner_player = ball.out_of_bounds()

    if somebody_won:
        if winner_player == "player1":
            player1.update_points()
        elif winner_player == "player2":
            player2.update_points()

        spawn(player1, player2, ball)
        update_scorboard(player1, player2, screen)

        return True
    else:
        return False


def spawn(player1, player2, ball):
    """
        spawns the ball and player to default position
    """
    player1.spawn(WIDTH, HEIGHT // 2)
    player2.spawn(15, HEIGHT // 2)

    ball.spawn(WIDTH // 2, HEIGHT // 2)


def update_scorboard(player1, player2, screen):
    """
        updates the scoreboard to the new values
    """

    # make the bar white to remove old points
    screen.fill(pygame.Color("white"), (0, 0, 150, 20))

    # we render the new points
    textsurface = myfont.render(
        f"Points: {player2.points} - {player1.points}", 1, (0, 0, 0))

    screen.blit(textsurface, (0, 0))


def make_scoreboard(player1, player2, screen):
    """
        It makes the scoreboard with the default values for start of game
    """
    textsurface = myfont.render(
        f"Points: {player2.points} - {player1.points}", 1, (0, 0, 0))

    screen.blit(textsurface, (0, 0))


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

    # create the players
    player1 = Player(WIDTH, HEIGHT // 2, screen)
    player2 = Player(15, HEIGHT // 2, screen)

    draw_background(screen)

    ball.show(fgColor)

    player1.show(fgColor)
    player2.show(fgColor)

    make_scoreboard(player1, player2, screen)

    for_pausing_game = 0

    while True:
        # check if we have to pause the game
        if for_pausing_game == 1:
            # we make a pause so players can prepare themselves
            pygame.time.wait(2000)

            for_pausing_game = 0

        # get the events
        event = pygame.event.poll()

        # check if the window was closed
        if event.type == pygame.QUIT:
            pygame.quit()
            break

        move(event, player1, player2, pressed_keys)

        ball.move(player1.get_rect(), player2.get_rect(), player1, player2)

        # we update this variable to check in the next loop if it changed to
        # make a pause in the next frame
        if update_score(player1, player2, ball, screen):
            for_pausing_game += 1

        # we draw the middle line so when the ball passes over it it resets itself
        draw_middle_line(screen)

        pygame.display.flip()
        clock.tick(FRAMERATE)


if __name__ == "__main__":
    main()
