import pygame
import sys


def completeachievement(num):  # completes achievement
    achievementschecklist = []
    with open("imagesandsuch/achievementlist.txt", "r") as achievementlist:
        for line in achievementlist:
            achievementschecklist.append(line)
    achievementschecklist[num] = "1\n"

    with open("imagesandsuch/achievementlist.txt", "w") as achievementlist:
        for ach in achievementschecklist:
            achievementlist.write(ach)


def achievements(game):  # creates achievements screen
    running = True
    completeimg = pygame.image.load("imagesandsuch/completed.png")
    incompleteimg = pygame.image.load("imagesandsuch/incomplete.png")
    background = pygame.image.load("imagesandsuch/achievementui.png")
    backimg = pygame.image.load("imagesandsuch/backbutton.png")
    click = False
    complete = pygame.transform.scale(completeimg, (30, 30))
    incomplete = pygame.transform.scale(incompleteimg, (30, 30))
    backbutton = pygame.Rect(125, 500, 120, 50)

    game.screen.fill("black")
    game.screen.blit(background, (0, 0))
    game.screen.blit(backimg, (125, 500))

    with open("imagesandsuch/achievementlist.txt", "r") as achievementfile:
        x = 0
        for line in achievementfile:
            if (line[:-1]) == "0":
                game.screen.blit(incomplete, (300, 100 + (65 * x)))
            else:
                game.screen.blit(complete, (300, 100 + (65 * x)))
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
