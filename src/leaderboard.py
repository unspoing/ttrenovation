import pygame
import sys

from functions import draw_text


def leaderboard(game):  # creates leaderboard
    running = True
    backbutton = pygame.Rect(125, 520, 120, 50)
    click = False
    backimg = pygame.image.load("imagesandsuch/backbutton.png")
    bgimg = pygame.image.load("imagesandsuch/bg2.png")

    game.screen.fill("black")
    game.screen.blit(bgimg, (0, 0))
    game.screen.blit(backimg, (125, 520))

    with open("imagesandsuch/highscores.txt", "r") as highscore:
        x = 0
        for line in highscore:
            draw_text(line[:-1], game.font, (0, 0, 0), game.screen, 95, 40 + (50 * x))
            x = x + 1

    with open("imagesandsuch/scores.txt", "r") as score:
        x = 0
        for line in score:
            draw_text(line[:-1], game.font, (0, 0, 0), game.screen, 175, 40 + (50 * x))
            x = x + 1

    while running:
        pos = pygame.mouse.get_pos()

        if backbutton.collidepoint(pos):
            if click:
                running = False

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        game.clock.tick(60)
