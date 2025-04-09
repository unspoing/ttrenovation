import random
import sys
import math

import pygame
import pymunk
import functions

from pymunk import Vec2d

pygame.init()

w, h = 400, 600  # shenanigans
collision_types = {
    "block": 1,
    "mblock": 2,
    "bottom": 3,
    "top": 4,
}  # block for dynamic mblock for kinematic
screen = pygame.display.set_mode((w, h))
font = pygame.font.Font("imagesandsuch/pixelfont.ttf", 9)
menufont = pygame.font.Font("imagesandsuch/pixelfont.ttf", 50)
winfont = pygame.font.Font("imagesandsuch/pixelfont.ttf", 30)
storefont = pygame.font.Font("imagesandsuch/pixelfont.ttf", 15)
clock = pygame.time.Clock()
pygame.display.set_caption("tricky towers knockoff")
leaderboardscore = " "

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
    screen.fill("black")

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

        pygame.draw.rect(screen, (255, 0, 0), playbutton)
        pygame.draw.rect(screen, (255, 0, 0), ldbbutton)
        pygame.draw.rect(screen, (255, 0, 0), achievbutton)
        pygame.draw.rect(screen, (255, 0, 0), storebutton)

        screen.blit(bg, (0, 0))
        screen.blit(achievementimg, (125, 405))
        screen.blit(playimg, (125, 295))
        screen.blit(leaderboardimg, (125, 350))
        screen.blit(storeimg, (125, 460))

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
        clock.tick(60)

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
    music = True

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
    voidhandler = space.add_collision_handler(
        collision_types["bottom"], collision_types["block"]
    )
    voidhandler.begin = functions.blocklost  # detect when a block falls off

    voidhandler2 = space.add_collision_handler(
        collision_types["bottom"], collision_types["mblock"]
    )
    voidhandler2.begin = functions.blocklost  # detect when a non-placed block isnt placed (you gotta be trash to let that happen bruh)

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

        timetext = font.render(storelist[1], storefont, (0, 0, 0))
        losttext = font.render(storelist[2], storefont, [0, 0, 0])

        screen.blit(losttext, (40, 57))
        screen.blit(timetext, (25, 37))
        
        for event in pygame.event.get():
            mpos = pygame.mouse.get_pos()


            ### INPUTS ###
            if event.type == pygame.QUIT:  # exit
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # exit
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # spawning/dropping block
                # if no block is currently in control:
                if placed and not win:
                    block = functions.create_block((196, 50))  # create block
                    blockhandler.begin = block.collide  # start collision handler for block
                    # add to screen and space
                    if len(block.shape) == 1:
                        BLOCKS_ON_SCREEN.append(block)
                        space.add(block.body, block.shape[0])
                    else:
                        BLOCKS_ON_SCREEN.append(block)
                        space.add(block.body, block.shape[0], block.shape[1])
                    placed = False
                    continue
                # if block is currently in control:
                if not placed:
                    functions.drop_block(block, space)
                    placed = True
                    bd +=1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:  # move right
                if not placed:
                    pos = block.get_position()
                    block.set_position((pos[0] + 7.5, pos[1]))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:  # move down
                if not placed:
                    block.set_velocity((0, 100))
                    down = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:  # stop moving down
                if not placed:
                    block.set_velocity((0, 0))
                    down = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:  # move left
                if not placed:
                    pos = block.get_position()
                    block.set_position((pos[0] - 7.5, pos[1]))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # rotate
                if not placed:
                    angle = block.get_angle()
                    block.set_angle(angle + 1.5708)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:  # rotate
                if not placed:
                    angle = block.get_angle()
                    block.set_angle(angle - 1.5708)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:  # pause/play music
                if music:
                    pygame.mixer.music.pause()
                    music = False
                else:
                    pygame.mixer.music.unpause()
                    music = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True


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
        clock.tick(fps)
        lost = str(math.trunc(bl))
        timetext = font.render(storelist[1], storefont, (0, 0, 0))
        losttext = font.render(storelist[2], storefont, [0, 0, 0])

        screen.blit(bg, (0, 0))
        screen.blit(finishline, (0, 126))
        screen.blit(timetext, (25, 37))
        screen.blit(losttext, (40, 57))
        if windevent:
            screen.blit(windimg, (0, 0))

        functions.draw_text(
            ("Blocks Dropped: " + str(bd)), font, (0, 0, 0), screen, 0, 0
        )
        functions.draw_text(("Blocks Lost: " + lost), font, (0, 0, 0), screen, 0, 18)
        functions.draw_text(
            ("Time: " + functions.convtomin(int((timer / 60)))),
            font,
            (0, 0, 0),
            screen,
            270,
            0,
        )
        ### PRINT SPRITES ###
        for block in BLOCKS_ON_SCREEN:
            if (
                block.name == "lblock"
                or block.name == "jblock"
                or block.name == "tblock"
            ):
                pos = block.get_position()
                pos = Vec2d((pos.x), (pos.y))
                angle_degrees = math.degrees(-(block.get_angle()))
                rotated_block = pygame.transform.rotate(
                    blockImages[block.name], angle_degrees
                )
                transoffset = Vec2d(*rotated_block.get_size()) / 2
                angoffset = (
                    (5.3033 * math.sin((functions.convtorad(angle_degrees)) + 0.785)),
                    -(5.3033 * math.cos((functions.convtorad(angle_degrees)) + 0.785)),
                )
                pos = pos - transoffset + angoffset
                screen.blit(rotated_block, (round(pos.x), round(pos.y)))
            else:
                pos = block.body.position
                pos = Vec2d((pos.x), (pos.y))
                angle_degrees = math.degrees(-(block.body.angle))
                rotated_block = pygame.transform.rotate(
                    blockImages[block.name], angle_degrees
                )
                offset = Vec2d(*rotated_block.get_size()) / 2
                pos = pos - offset
                screen.blit(rotated_block, (round(pos.x), round(pos.y)))





        if touch:
            wintick = wintick + 1

            if (int(wintick / 60)) == 1:
                functions.draw_text(("3"), menufont, (0, 0, 0), screen, 170, 300)
            if (int(wintick / 60)) == 2:
                functions.draw_text(("2"), menufont, (0, 0, 0), screen, 170, 300)
            if (int(wintick / 60)) == 3:
                functions.draw_text(("1"), menufont, (0, 0, 0), screen, 170, 300)
            if (int(wintick / 60)) == 4:
                win = True

        if not touch:
            wintick = 0
        if win:
            coingain = functions.calcmoragain(timer / 60, bl)
            # leaderboardscore = str('Score:'+ calcscore(timer/60,bl) + 'Time: '+ convtomin(int((timer/60))))
            escbutton = pygame.Rect(120, 265, 146, 50)
            functions.draw_text(("you win!"), menufont, (0, 0, 0), screen, 10, 200)
            functions.draw_text(
                ("Time: " + functions.convtomin(int((timer / 60)))),
                winfont,
                (0, 0, 0),
                screen,
                50,
                320,
            )
            functions.draw_text(
                ("Score: " + functions.calcscore(timer / 60, bl)),
                winfont,
                (0, 0, 0),
                screen,
                50,
                370,
            )
            functions.draw_text(
                ("Coins gained: " + str(coingain)),
                storefont,
                (255, 255, 0),
                screen,
                50,
                420,
            )
            if not gainedcoins:
                storelist[0] = str(int(storelist[0]) + coingain)
                gainedcoins = True

            screen.blit(backbutton, (120, 265))

            if escbutton.collidepoint(mpos):  # detect click on play
                if click:
                    running = False

            click = False

        time = pygame.image.load("imagesandsuch/timeicon.png")
        skip = pygame.image.load("imagesandsuch/skipicon.png")

        timeicon = pygame.transform.scale(time, (20, 20))
        skipicon = pygame.transform.scale(skip, (40, 20))

        screen.blit(timeicon, (0, 30))
        screen.blit(skipicon, (0, 50))

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
