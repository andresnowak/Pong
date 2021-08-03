import pygame
from Controller import ControllerKeyTypes


class Player:
    WIDTH = 15
    screen_height = 100
    points = 0

    HIDE = pygame.Color("black")  # color to hide the player with background
    SHOW = pygame.Color("white")  # color tho show the player

    def __init__(self, start_pos_x, start_pos_y, screen, controller):
        self.pos_x = start_pos_x
        self.pos_y = start_pos_y
        self.screen = screen
        self.controller = controller

        self.player = pygame.Rect(
            self.pos_x - self.WIDTH, self.pos_y - self.screen_height // 2, self.WIDTH, self.screen_height)

    def show(self, color):
        pygame.draw.rect(self.screen, color, self.player)

    def move(self, event, screen_height, screen_border):
        """
            Moves the player
        """

        # the amount of pixels the player moves
        move = 4

        # the amount of pixels the player moves
        player_movement_to_be_made = self.controller.action_activated(event)

        if player_movement_to_be_made.get(ControllerKeyTypes.KEY_UP):
            move *= -1
        elif player_movement_to_be_made.get(ControllerKeyTypes.KEY_DOWN):
            move *= 1
        else:
            move = 0

        # hide the player
        self.show(self.HIDE)

        # move it
        self.player.y += move

        self.stop_player_going_out_of_bounds(screen_height, screen_border)

        # show player
        self.show(self.SHOW)

    def stop_player_going_out_of_bounds(self, screen_height, screen_border):
        # check if the player is gonna pass the borders of the game
        if self.player.bottom >= screen_height - screen_border:
            self.player.bottom = screen_height - screen_border
        if self.player.top <= screen_border:
            self.player.top = screen_border

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
