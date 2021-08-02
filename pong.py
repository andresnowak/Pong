import pygame
from Ball import Ball
from Player import Player
from Controller import Controller


WIDTH = 1200
HEIGHT = 640
BORDER = 40

fgColor = pygame.Color("white")

FRAMERATE = 60


def move(event, player1, player2):
    """
        moves the player depending on what key was pressed
    """

    player1.move(event, HEIGHT, BORDER)
    player2.move(event, HEIGHT, BORDER)


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
    somebody_won, winner_player = ball.out_of_bounds(WIDTH)

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


def game_ended(player1, player2):
    """
        Checks if the game has ended
    """
    if player1.get_points() == 11 or player2.get_points() == 11:
        return True
    else:
        return False


def restart_game(player1, player2, ball, screen):
    reset_scoreboard(player1, player2, screen)

    spawn(player1, player2, ball)


def reset_scoreboard(player1, player2, screen):
    """
        resets the scoreboard to 0
    """
    player1.reset_points()
    player2.reset_points()

    update_scorboard(player1, player2, screen)


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
    WIDTH_OF_SCOREBOARD = 300
    screen.fill(pygame.Color("white"), (0, 0, WIDTH_OF_SCOREBOARD, BORDER))

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
    BALL_VX = 6
    BALL_VY = 6

    # create the ball
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_VX, BALL_VY, screen)

    # create the players and controller
    controller = Controller(up=pygame.K_UP, down=pygame.K_DOWN)
    player1 = Player(WIDTH, HEIGHT // 2, screen, controller)

    controller = Controller(up=pygame.K_w, down=pygame.K_s)
    player2 = Player(15, HEIGHT // 2, screen, controller)

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

        # check if if game has ended
        if game_ended(player1, player2):
            restart_game(player1, player2, ball, screen)

        # get the events
        event = pygame.event.poll()

        # check if the window was closed
        if event.type == pygame.QUIT:
            pygame.quit()
            break

        move(event, player1, player2)

        ball.move(player1.get_rect(), player2.get_rect(),
                  player1, player2, HEIGHT, BORDER)

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
