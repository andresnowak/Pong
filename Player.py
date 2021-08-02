import pygame


class Player:
    WIDTH = 15
    screen_height = 100
    points = 0

    HIDE = pygame.Color("black")  # color to hide the player with background
    SHOW = pygame.Color("white")  # color tho show the player

    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

        self.player = pygame.Rect(
            self.x - self.WIDTH, self.y - self.screen_height // 2, self.WIDTH, self.screen_height)

    def show(self, color):
        pygame.draw.rect(self.screen, color, self.player)

    def move(self, movement, screen_height, screen_border):
        """
            Moves the player
        """

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
        if self.player.bottom >= screen_height - screen_border:
            self.player.bottom = screen_height - screen_border
        if self.player.top <= screen_border:
            self.player.top = screen_border

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
        self.player.y = y - self.screen_height // 2

        # show player
        self.show(self.SHOW)

    def get_points(self):
        return self.points

    def reset_points(self):
        self.points = 0
