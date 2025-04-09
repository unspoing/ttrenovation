
import pygame


def store():  # open store
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
        screen.fill("black")
        screen.blit(background, (0, 0))
        screen.blit(backimg, (125, 500))
        screen.blit(money, (150, 90))

        storelist = []
        storeinfo = open("imagesandsuch/storeinfo.txt", "r")
        pos = pygame.mouse.get_pos()

        for line in storeinfo:
            storelist.append(line[:-1])
        storeinfo.close()

        if backbutton.collidepoint(pos):  # detect click on play
            if click:
                running = False
        if sakurabutton.collidepoint(pos):
            if click:
                if storelist[3] == "0":
                    if int(storelist[0]) >= 0:
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
            text = font.render("Buy:100", storefont, [0, 0, 0])
            screen.blit(text, (70, 400))
        if storelist[3] == "1" and storelist[4] == "1":
            text = font.render("unequip", storefont, [0, 0, 0])
            screen.blit(text, (70, 400))
        if storelist[3] == "1" and storelist[4] == "0":
            text = font.render("equip", storefont, [0, 0, 0])
            screen.blit(text, (70, 400))

        timetext = font.render("owned:" + storelist[1], storefont, [0, 0, 0])
        losttext = font.render("owned:" + storelist[2], storefont, [0, 0, 0])
        moneycount = font.render(storelist[0], storefont, [0, 0, 0])

        screen.blit(losttext, (160, 225))
        screen.blit(timetext, (65, 225))
        screen.blit(moneycount, (180, 105))

        draw_text("Buy:8", font, (0, 0, 0), screen, 65, 240)
        draw_text("Buy:12", font, (0, 0, 0), screen, 160, 240)

        storeedit = open("imagesandsuch/storeinfo.txt", "w")
        for val in storelist:
            storeedit.write(val + "\n")
        storeedit.close()

        pygame.display.update()
        clock.tick(60)
