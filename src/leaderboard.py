
import pygame


def leaderboard():  # creates leaderboard
    running = True
    backbutton = pygame.Rect(125, 520, 120, 50)
    click = False
    backimg = pygame.image.load("imagesandsuch/backbutton.png")
    bgimg = pygame.image.load("imagesandsuch/bg2.png")
    highscore = open("imagesandsuch/highscores.txt", "r")
    score = open("imagesandsuch/scores.txt", "r")

    screen.fill("black")
    screen.blit(bgimg, (0, 0))
    screen.blit(backimg, (125, 520))

    x = 0
    for line in highscore:
        draw_text(line[:-1], font, (0, 0, 0), screen, 95, 40 + (50 * x))
        x = x + 1

    x = 0
    for line in score:
        draw_text(line[:-1], font, (0, 0, 0), screen, 175, 40 + (50 * x))
        x = x + 1

    while running:
        pos = pygame.mouse.get_pos()

        if backbutton.collidepoint(pos):  # detect click on play
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
        clock.tick(60)
