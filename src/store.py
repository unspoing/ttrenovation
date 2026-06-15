import pygame
import sys

from functions import draw_text, read_storelist, write_storelist


def store(game):  # open store
    running = True
    background = pygame.image.load(
        "imagesandsuch/storeui.png"
    )  # background shenanigans
    mora = pygame.image.load("imagesandsuch/money.webp")
    backimg = pygame.image.load("imagesandsuch/backbutton.png")
    click = False
    money = pygame.transform.scale(mora, (30, 30))
    backbutton = pygame.Rect(125, 500, 120, 50)
    sakurabutton = pygame.Rect(70, 325, 60, 60)
    timebutton = pygame.Rect(70, 165, 50, 50)
    lostbutton = pygame.Rect(150, 165, 80, 50)

    while running:
        game.screen.fill("black")
        game.screen.blit(background, (0, 0))
        game.screen.blit(backimg, (125, 500))
        game.screen.blit(money, (150, 90))

        storelist = read_storelist()
        pos = pygame.mouse.get_pos()

        # make purchases
        if backbutton.collidepoint(pos):
            if click:
                running = False
        if sakurabutton.collidepoint(pos):
            if click:
                if storelist[3] == "0":
                    if int(storelist[0]) >= 100:
                        storelist[3] = "1"
                        storelist[0] = str(int(storelist[0]) - 100)
                if storelist[3] == "1" and storelist[4] == "1":
                    storelist[4] = "0"
                else:
                    storelist[4] = "1"
        if timebutton.collidepoint(pos):
            if click:
                if int(storelist[0]) >= 8:
                    storelist[0] = str(int(storelist[0]) - 8)
                    storelist[1] = str(int(storelist[1]) + 1)
        if lostbutton.collidepoint(pos):
            if click:
                if int(storelist[0]) >= 12:
                    storelist[0] = str(int(storelist[0]) - 12)
                    storelist[2] = str(int(storelist[2]) + 1)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if storelist[3] == "0":
            text = game.font.render("Buy:100", game.storefont, [0, 0, 0])
            game.screen.blit(text, (70, 400))
        if storelist[3] == "1" and storelist[4] == "1":
            text = game.font.render("unequip", game.storefont, [0, 0, 0])
            game.screen.blit(text, (70, 400))
        if storelist[3] == "1" and storelist[4] == "0":
            text = game.font.render("equip", game.storefont, [0, 0, 0])
            game.screen.blit(text, (70, 400))

        timetext = game.font.render("owned:" + storelist[1], game.storefont, [0, 0, 0])
        losttext = game.font.render("owned:" + storelist[2], game.storefont, [0, 0, 0])
        moneycount = game.font.render(storelist[0], game.storefont, [0, 0, 0])

        game.screen.blit(losttext, (160, 225))
        game.screen.blit(timetext, (65, 225))
        game.screen.blit(moneycount, (180, 105))

        draw_text("Buy:8", game.font, (0, 0, 0), game.screen, 65, 240)
        draw_text("Buy:12", game.font, (0, 0, 0), game.screen, 160, 240)

        write_storelist(storelist)

        pygame.display.update()
        game.clock.tick(60)
