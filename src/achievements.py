
import pygame


def achievements():  # creates leaderboard
    running = True
    completeimg = pygame.image.load("imagesandsuch/completed.png")
    incompleteimg = pygame.image.load("imagesandsuch/incomplete.png")
    background = pygame.image.load("imagesandsuch/achievementui.png")
    achievementfile = open("imagesandsuch/achievementlist.txt", "r")
    backimg = pygame.image.load("imagesandsuch/backbutton.png")
    click = False
    complete = pygame.transform.scale(completeimg, (30, 30))
    incomplete = pygame.transform.scale(incompleteimg, (30, 30))
    backbutton = pygame.Rect(125, 500, 120, 50)

    screen.fill("black")
    screen.blit(background, (0, 0))
    screen.blit(backimg, (125, 500))

    x = 0
    for line in achievementfile:
        if (line[:-1]) == "0":
            screen.blit(incomplete, (300, 100 + (65 * x)))
            x = x + 1
        else:
            screen.blit(complete, (300, 100 + (65 * x)))
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
