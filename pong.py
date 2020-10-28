import pygame


class Ball:
    RADIUS = 12

    HIDE = pygame.Color("black")  # color to hide the ball with background
    SHOW = pygame.Color("white")  # color tho show the ball

    def __init__(self, x, y, vx, vy, screen):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

        self.hitbox = (self.x - self.RADIUS, self.y - self.RADIUS, 30, 30)

        self.screen = screen

    def show(self, color):
        pygame.draw.circle(self.screen, color, (self.x, self.y), self.RADIUS)
        pygame.draw.rect(self.screen, color, self.hitbox, 2)

    def move(self, player1_pos, player2_pos):
        """
            moves the ball
        """
        global BORDER

        new_pos_x = self.x + self.vx
        new_pos_y = self.y + self.vy

        hitbox = (new_pos_x - self.RADIUS, new_pos_y - self.RADIUS, 25, 25)

        if self.crashed(player1_pos, player2_pos, hitbox):
            self.vx *= -1
        elif new_pos_y < BORDER + self.RADIUS or new_pos_y > HEIGHT - BORDER - self.RADIUS:
            self.vy *= -1

        else:
            self.show(self.HIDE)

            # update position of ball
            self.x = new_pos_x
            self.y = new_pos_y

            # update position of its hitbox
            self.hitbox = (self.x - self.RADIUS, self.y - self.RADIUS, 25, 25)

            self.show(self.SHOW)

    def crashed(self, player1_pos, player2_pos, hitbox):
        """
            Check if the ball has crashed with a player to bounce
        """
        global WIDTH

        if hitbox[0] + hitbox[2] >= WIDTH - player1_pos[2] and hitbox[0] + hitbox[2] < WIDTH:
            if hitbox[1] <= player1_pos[0] and hitbox[1] + hitbox[3] >= player1_pos[0] - player1_pos[1]:
                print("hey")
                return True
        elif hitbox[0] <= player2_pos[2] and hitbox[0] > 0:
            if hitbox[1] <= player2_pos[0] and hitbox[1] + hitbox[3] >= player2_pos[0] - player2_pos[1]:
                print("hey2")
                return True
        else:
            return False


class Player:
    WIDTH = 15
    HEIGHT = 100

    HIDE = pygame.Color("black")  # color to hide the player with background
    SHOW = pygame.Color("white")  # color tho show the player

    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

    def show(self, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(
            self.x - self.WIDTH, self.y - self.HEIGHT // 2, self.WIDTH, self.HEIGHT))

    def move_down(self):
        """
            Moves the player down
        """
        global BORDER
        global HEIGHT

        # the amount of pixels the player moves

        move = 6

        new_pos = self.y + move

        # check if the player is gonna pass the borders of the game
        if new_pos > HEIGHT - BORDER - (self.HEIGHT // 2):
            move = 0

        self.show(self.HIDE)
        self.y += move
        self.show(self.SHOW)

    def move_up(self):
        """
            moves the player up
        """
        global BORDER
        global HEIGHT

        # the amount of pixels the player moves
        move = -10

        new_pos = self.y + move

        # check if the player is gonna pass the borders of the game
        if new_pos < BORDER + (self.HEIGHT // 2):
            move = 0

        self.show(self.HIDE)
        self.y += move
        self.show(self.SHOW)

    def get_position(self):
        return self.y, self.HEIGHT, self.WIDTH


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

    # speed for ball
    ball_vx = 5
    ball_vy = 5

    # dictionary to update player movements
    pressed_keys = {"w": False, "s": False, "down": False, "up": False}

    # create the ball
    ball = Ball(WIDTH // 2, HEIGHT // 2, ball_vx, ball_vy, screen)

    # crate the players
    player1 = Player(WIDTH, HEIGHT // 2, screen)
    player2 = Player(15, HEIGHT // 2, screen)

    draw_background(screen)

    ball.show(fgColor)

    player1.show(fgColor)
    player2.show(fgColor)

    while True:
        event = pygame.event.poll()

        # check if the window was closed
        if event.type == pygame.QUIT:
            break

        move(event, player1, player2, pressed_keys)
        ball.move(player1.get_position(), player2.get_position())

        pygame.display.flip()
        clock.tick(FRAMERATE)

    pygame.quit()


if __name__ == "__main__":
    main()
