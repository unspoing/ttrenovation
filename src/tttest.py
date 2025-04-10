import random
import sys
import math

import pygame
import pymunk
import functions

from gui import GUI

from pymunk.pygame_util import DrawOptions

pygame.init()

w, h = 400, 600  # shenanigans
collision_types = {
    "block": 1,
    "mblock": 2,
    "bottom": 3,
    "top": 4,
}  # block for dynamic mblock for kinematic

game = GUI("imagesandsuch/pixelfont.ttf")

BLOCKS_ON_SCREEN = []

def setup(space):  # add ground into game
    ground = pymunk.Body(0, 0, body_type=pymunk.Body.STATIC)
    ground.position = (188), (420)
    shape = pymunk.Poly.create_box(ground, (90, 5))
    shape.collision_type = collision_types["block"]
    shape.color = pygame.Color(0, 0, 0, 0)
    shape.friction = 0.8
    shape.elasticity = 0
    groundraise = pymunk.Body(1, 1000, body_type=pymunk.Body.STATIC)
    groundraise.position = 181, 411.5
    shape2 = pymunk.Poly.create_box(groundraise, (15, 15))
    shape2.collision_type = collision_types["block"]
    bottom = pymunk.Segment(space.static_body, (-500, 800), (1000, 800), 2)
    bottom.sensor = True
    bottom.collision_type = collision_types["bottom"]
    bottom.color = pygame.Color("red")
    top = pymunk.Segment(space.static_body, (-500, 150), (1000, 150), 2)
    top.sensor = True
    top.collision_type = collision_types["top"]
    top.color = pygame.Color("red")
    space.add(ground, shape, shape2, groundraise, bottom, top)

def menu():  # creates menu
    game.screen.fill("black")

    click = False
    background = pygame.image.load(
        "imagesandsuch/background.png"
    )  # background shenanigans
    playimg = pygame.image.load("imagesandsuch/startbutton.png")  # start button image
    achievementimg = pygame.image.load(
        "imagesandsuch/achievementbutton.png"
    )  # yapyapyap
    leaderboardimg = pygame.image.load(
        "imagesandsuch/leaderboardbutton.png"
    )  # yapyapyap
    storeimg = pygame.image.load("imagesandsuch/storebutton.png")

    bg = pygame.transform.scale(background, (w, h))

    while True:
        pos = pygame.mouse.get_pos()

        playbutton = pygame.Rect(125, 295, 146, 50)
        ldbbutton = pygame.Rect(125, 350, 146, 50)
        achievbutton = pygame.Rect(125, 405, 146, 50)
        storebutton = pygame.Rect(125, 460, 146, 50)

        pygame.draw.rect(game.screen, (255, 0, 0), playbutton)
        pygame.draw.rect(game.screen, (255, 0, 0), ldbbutton)
        pygame.draw.rect(game.screen, (255, 0, 0), achievbutton)
        pygame.draw.rect(game.screen, (255, 0, 0), storebutton)

        game.screen.blit(bg, (0, 0))
        game.screen.blit(achievementimg, (125, 405))
        game.screen.blit(playimg, (125, 295))
        game.screen.blit(leaderboardimg, (125, 350))
        game.screen.blit(storeimg, (125, 460))

        if playbutton.collidepoint(pos):
            if click:
                main()

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

def main():
    ### SETUP ###
    touch = False
    timercooldown = 600
    windtimer = 0
    running = True

    placed = True
    gainedcoins = False
    timer = 0
    wintick = 0
    win = False

    bd = 0
    bl = 0

    click = False
    windevent = False
    down = False
    space = pymunk.Space()  # create space and gravity
    space.gravity = (0, 900)

    background = pygame.image.load("imagesandsuch/gamebg.png")
    finishline = pygame.image.load("imagesandsuch/finishline.png")
    backbutton = pygame.image.load("imagesandsuch/backbutton.png")
    windimg = pygame.image.load("imagesandsuch/wind.png")

    bg = pygame.transform.scale(background, (w, h))

    storelist = []
    storeinfo = open("imagesandsuch/storeinfo.txt", "r")

    for line in storeinfo:
        storelist.append(line[:-1])
    storeinfo.close()

    if storelist[4] == "0":
        # pygame.mixer.music.load("imagesandsuch/un_sospiro.mp3")
        iblock = pygame.image.load("imagesandsuch/iblock.png")
        iblock.set_colorkey(0)
        lblock = pygame.image.load("imagesandsuch/lblock.png")
        lblock.set_colorkey(0)
        oblock = pygame.image.load("imagesandsuch/oblock.png")
        oblock.set_colorkey(0)
        jblock = pygame.image.load("imagesandsuch/jblock.png")
        jblock.set_colorkey(0)
        zblock = pygame.image.load("imagesandsuch/zblock.png")
        zblock.set_colorkey(0)
        sblock = pygame.image.load("imagesandsuch/sblock.png")
        sblock.set_colorkey(0)
        tblock = pygame.image.load("imagesandsuch/tblock.png")
        tblock.set_colorkey(0)
    else:
        # pygame.mixer.music.load("imagesandsuch/liebestraum.mp3")
        iblock = pygame.image.load("imagesandsuch/iblocksakura.png")
        iblock.set_colorkey(0)
        lblock = pygame.image.load("imagesandsuch/lblocksakura.png")
        lblock.set_colorkey(0)
        oblock = pygame.image.load("imagesandsuch/oblocksakura.png")
        oblock.set_colorkey(0)
        jblock = pygame.image.load("imagesandsuch/jblocksakura.png")
        jblock.set_colorkey(0)
        zblock = pygame.image.load("imagesandsuch/zblocksakura.png")
        zblock.set_colorkey(0)
        sblock = pygame.image.load("imagesandsuch/sblocksakura.png")
        sblock.set_colorkey(0)
        tblock = pygame.image.load("imagesandsuch/tblocksakura.png")
        tblock.set_colorkey(0)

    blockImages = {
        "iblock": iblock,
        "jblock": jblock,
        "oblock": oblock,
        "zblock": zblock,
        "sblock": sblock,
        "tblock": tblock,
        "lblock": lblock,
    }

    blockhandler = space.add_collision_handler(
        collision_types["mblock"], collision_types["block"]
    )

    winhandler = space.add_collision_handler(
        collision_types["top"], collision_types["block"]
    )
    winhandler.begin = functions.starttimer
    winhandler.separate = functions.stoptimer

    setup(space)  # create ground

    # create first block
    block = functions.create_block((196, 50))
    blockhandler.begin = block.collide 
    if len(block.shape) == 1:
        BLOCKS_ON_SCREEN.append(block)
        space.add(block.body, block.shape[0])
    else:
        BLOCKS_ON_SCREEN.append(block)
        space.add(block.body, block.shape[0], block.shape[1])
    placed = False


    ### RUN GAME ###
    while running:

        storelist = []
        storeinfo = open("imagesandsuch/storeinfo.txt", "r")

        for line in storeinfo:
            storelist.append(line[:-1])
        storeinfo.close()

        timetext = game.font.render(storelist[1], game.storefont, (0, 0, 0))
        losttext = game.font.render(storelist[2], game.storefont, [0, 0, 0])

        game.screen.blit(losttext, (40, 57))
        game.screen.blit(timetext, (25, 37))
        
        for event in pygame.event.get():
            mpos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:  # exit
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # exit
                running = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            # handle spawning/despawning
            block, placed, bd = functions.handle_spawning(event, block, placed, win, space, BLOCKS_ON_SCREEN, bd, blockhandler)

            # handle movement
            down = functions.handle_movement(event, block, placed, down)

        ### CHECK FOR WINS, COLLISIONS, AND SHIFT CURRENT BLOCK DOWN ###
        if not win:
            if windtimer == 0:
                windevent = False
                if not placed and not down:
                    block.set_velocity((0, 0))
                if functions.startwindevent():
                    windtimer = 600
                    windevent = True
                    print("wind")
            if windtimer > 0:
                if windtimer % 30 == 0:
                    if not placed:
                        block.set_velocity((random.randint(-80, 80), 0))
                windtimer = windtimer - 1
        if timercooldown > 0:
            timercooldown = timercooldown - 1

        if not placed:  # moves pieces down as timer
            timer +=1
            pos = block.get_position()
            block.set_position(((pos[0]), (pos[1] + 0.35)))

        if block.collision:
            functions.drop_block(block, space)
            placed = True
            block.collision = False
            bd = bd + 1


        fps = 60.0
        dt = 1.0 / fps
        space.step(dt)
        game.clock.tick(fps)
        lost = str(math.trunc(bl))
        timetext = game.font.render(storelist[1], game.storefont, (0, 0, 0))
        losttext = game.font.render(storelist[2], game.storefont, [0, 0, 0])

        game.screen.blit(bg, (0, 0))
        game.screen.blit(finishline, (0, 126))
        game.screen.blit(timetext, (25, 37))
        game.screen.blit(losttext, (40, 57))
        if windevent:
            game.screen.blit(windimg, (0, 0))

        functions.draw_text(
            ("Blocks Dropped: " + str(bd)), game.font, (0, 0, 0), game.screen, 0, 0
        )
        functions.draw_text(("Blocks Lost: " + lost), game.font, (0, 0, 0), game.screen, 0, 18)
        functions.draw_text(
            ("Time: " + functions.convtomin(int((timer / 60)))),
            game.font,
            (0, 0, 0),
            game.screen,
            270,
            0,
        )

        for block in BLOCKS_ON_SCREEN:
            functions.draw_sprite(block, game.screen, blockImages)
            #print(BLOCKS_ON_SCREEN)


        if touch:
            wintick = wintick + 1

            if (int(wintick / 60)) == 1:
                functions.draw_text(("3"), game.menufont, (0, 0, 0), game.screen, 170, 300)
            if (int(wintick / 60)) == 2:
                functions.draw_text(("2"), game.menufont, (0, 0, 0), game.screen, 170, 300)
            if (int(wintick / 60)) == 3:
                functions.draw_text(("1"), game.menufont, (0, 0, 0), game.screen, 170, 300)
            if (int(wintick / 60)) == 4:
                win = True
        for block in BLOCKS_ON_SCREEN:
            height = block.get_position()[1]
            if height > 700:
                print(block.body.body_type)
                if block.body.body_type == 1:
                    print('MEOW')
                    functions.handle_spawning(event, block, placed, win, space, BLOCKS_ON_SCREEN, bd, blockhandler)
                    bd +=1
                    placed = True
                bl +=1
                BLOCKS_ON_SCREEN.remove(block)
                print(BLOCKS_ON_SCREEN)

                if len(block.shape) == 1:
                    space.remove(block.body, block.shape[0])
                else:
                    space.remove(block.body, block.shape[0], block.shape[1])

        if not touch:
            wintick = 0
        if win:
            coingain = functions.calcmoragain(timer / 60, bl)
            # leaderboardscore = str('Score:'+ calcscore(timer/60,bl) + 'Time: '+ convtomin(int((timer/60))))
            escbutton = pygame.Rect(120, 265, 146, 50)
            functions.draw_text(("you win!"), game.menufont, (0, 0, 0), game.screen, 10, 200)
            functions.draw_text(
                ("Time: " + functions.convtomin(int((timer / 60)))),
                game.winfont,
                (0, 0, 0),
                game.screen,
                50,
                320,
            )
            functions.draw_text(
                ("Score: " + functions.calcscore(timer / 60, bl)),
                game.winfont,
                (0, 0, 0),
                game.screen,
                50,
                370,
            )
            functions.draw_text(
                ("Coins gained: " + str(coingain)),
                game.storefont,
                (255, 255, 0),
                game.screen,
                50,
                420,
            )
            if not gainedcoins:
                storelist[0] = str(int(storelist[0]) + coingain)
                gainedcoins = True

            game.screen.blit(backbutton, (120, 265))

            if escbutton.collidepoint(mpos):  # detect click on play
                if click:
                    running = False

            click = False

        time = pygame.image.load("imagesandsuch/timeicon.png")
        skip = pygame.image.load("imagesandsuch/skipicon.png")

        timeicon = pygame.transform.scale(time, (20, 20))
        skipicon = pygame.transform.scale(skip, (40, 20))

        space.debug_draw(DrawOptions(game.screen))
        
        game.screen.blit(timeicon, (0, 30))
        game.screen.blit(skipicon, (0, 50))

        storeedit = open("imagesandsuch/storeinfo.txt", "w")
        for val in storelist:
            storeedit.write(val + "\n")
        
        storeedit.close()

        pygame.display.flip()

    # clear blocks list and show leaderboard
    BLOCKS_ON_SCREEN.clear()
    functions.createleaderboard(
        functions.calcscore(timer / 60, bl)
        + " Time:"
        + functions.convtomin(int((timer / 60)))
        + "\n"
    )

if __name__ == "__main__":
    sys.exit(menu())
