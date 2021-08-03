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

        self.ball = pygame.Rect(x - self.RADIUS // 2, y,
                                self.RADIUS, self.RADIUS)

        self.screen = screen

    def show(self, color):
        pygame.draw.ellipse(self.screen, color, self.ball)

    def move(self, player1Rect, player2Rect, player1, player2, screen_height, screen_border):
        """
            moves the ball
        """

        new_pos_x = self.ball.x + self.vx
        new_pos_y = self.ball.y + self.vy

        self.show(self.HIDE)

        # update position of ball
        self.ball.x = new_pos_x
        self.ball.y = new_pos_y

        # check if ball has crashed and make it bounce if true
        self.crashed_wall(screen_border, screen_height)
        self.crashed_player(player1Rect, player2Rect)

        self.show(self.SHOW)

    def stop_ball_going_out_of_bounds(self, screen_border, screen_height):
        if self.ball.top <= screen_border:
            self.ball.top = screen_border
        elif self.ball.bottom >= screen_height - screen_border:
            self.ball.bottom = screen_height - screen_border

    def crashed_player(self, player1, player2):
        """
            Check if the ball has crashed with a player and bounce it
        """

        if self.ball.colliderect(player1) or self.ball.colliderect(player2):
            self.vx *= -1

        if self.ball.colliderect(player1):
            self.ball.right = player1.left
        elif self.ball.colliderect(player2):
            self.ball.left = player2.right

    def crashed_wall(self, screen_border, screen_height):
        if self.ball.top <= screen_border or self.ball.bottom >= screen_height - screen_border:
            self.vy *= -1

    def out_of_bounds(self, screen_width_bounds):
        if self.ball.right <= 0:
            return True, "player1"
        elif self.ball.left >= screen_width_bounds:
            return True, "player2"
        else:
            return False, ""

    def spawn(self, x, y):
        """
            spawns the ball to the position it gets in x and y
        """
        # hide the ball
        self.show(self.HIDE)

        self.ball.x = x - self.RADIUS // 2
        self.ball.y = y

        # show the ball
        self.show(self.SHOW)
