import random
import sys
import math

import pygame

import pymunk
from pymunk import Vec2d
from pymunk.pygame_util import DrawOptions

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


iblocks = []  # lists of sprites
lblocks = []
jblocks = []
sblocks = []
zblocks = []
oblocks= []
tblocks = []


def block1(
    space, position, rotation
):  # no letter for dynamic, k at the end for kinematic
    body = pymunk.Body(1, 500, body_type=pymunk.Body.DYNAMIC)
    body.position = position
    print(position)
    body.angle = rotation * 1.5708
    shape = pymunk.Poly.create_box(body, (60, 15))
    shape.collision_type = collision_types["block"]
    shape.friction = 0.6
    shape.elasticity = 0
    shape.color = pygame.Color("red")
    space.add(body, shape)
    iblocks.append(shape)


def block1k(space, position):
    body = pymunk.Body(1, 500, body_type=pymunk.Body.KINEMATIC)
    body.position = position
    shape = pymunk.Poly.create_box(body, (60, 15))
    shape.collision_type = collision_types["mblock"]
    shape.friction = 0.6
    shape.elasticity = 0
    shape.color = pygame.Color("red")
    iblocks.append(shape)
    return (body, shape)


def block2(space, position, rotation):
    body = pymunk.Body(1, 1000, body_type=pymunk.Body.DYNAMIC)
    body.position = position
    shape = pymunk.Poly.create_box(body, (30, 30))
    shape.collision_type = collision_types["block"]
    shape.friction = 0.6
    shape.color = pygame.Color("blue")
    oblocks.append(shape)
    space.add(body, shape)


def block2k(space, position):
    body = pymunk.Body(1, 1000, body_type=pymunk.Body.KINEMATIC)
    body.position = position
    shape = pymunk.Poly.create_box(body, (30, 30))
    shape.collision_type = collision_types["mblock"]
    shape.friction = 0.6
    shape.color = pygame.Color("blue")
    oblocks.append(shape)
    return (body, shape)


def block3(space, pos, rotation):
    body = pymunk.Body(1, 500, body_type=pymunk.Body.DYNAMIC)
    body.position = ((pos[0]), (pos[1]))
    shape = pymunk.Poly(
        body, [(-11.25, 3.75), (-11.25, -26.25), (3.75, -26.25), (3.75, 3.75)]
    )
    shape.collision_type = collision_types["block"]
    shape.friction = 0.6
    shape.elasticity = 0
    shape.color = pygame.Color("purple")
    shape2 = pymunk.Poly(
        body, [(-11.25, 3.75), (18.75, 3.75), (18.75, 18.75), (-11.25, 18.75)]
    )
    shape2.collision_type = collision_types["block"]
    shape2.friction = 0.6
    shape2.elasticity = 0
    shape2.color = pygame.Color("purple")
    body.angle = rotation * 1.5708
    space.add(body, shape, shape2)
    lblocks.append(shape)


def block3k(space, pos):
    body = pymunk.Body(1, 500, body_type=pymunk.Body.KINEMATIC)
    body.position = ((pos[0] - 3.75), (pos[1] - 3.75))
    shape = pymunk.Poly(
        body, [(-11.25, 3.75), (-11.25, -26.25), (3.75, -26.25), (3.75, 3.75)]
    )
    shape.collision_type = collision_types["mblock"]
    shape.friction = 0.6
    shape.elasticity = 0
    shape.color = pygame.Color("purple")
    shape2 = pymunk.Poly(
        body, [(-11.25, 3.75), (18.75, 3.75), (18.75, 18.75), (-11.25, 18.75)]
    )
    shape2.collision_type = collision_types["mblock"]
    shape2.friction = 0.6
    shape2.elasticity = 0
    shape2.color = pygame.Color("purple")
    lblocks.append(shape)
    return (body, shape, shape2)


def block4(space, pos, rotation):
    body = pymunk.Body(1, 500, body_type=pymunk.Body.DYNAMIC)
    body.position = ((pos[0]), (pos[1]))
    shape = pymunk.Poly(
        body, [(11.25, 3.75), (11.25, -26.25), (-3.75, -26.25), (-3.75, 3.75)]
    )
    shape.collision_type = collision_types["block"]
    shape.friction = 0.6
    shape.elasticity = 0
    shape.color = pygame.Color("yellow")
    shape2 = pymunk.Poly(
        body, [(-18.75, 3.75), (11.25, 3.75), (11.25, 18.75), (-18.75, 18.75)]
    )
    shape2.collision_type = collision_types["block"]
    shape2.friction = 0.6
    shape2.elasticity = 0
    shape2.color = pygame.Color("yellow")
    body.angle = rotation * 1.5708
    jblocks.append(shape)
    space.add(body, shape, shape2)


def block4k(space, position):
    body = pymunk.Body(1, 500, body_type=pymunk.Body.KINEMATIC)
    body.position = ((position[0] + 3.75), (position[1] - 3.75))
    shape = pymunk.Poly(
        body, [(11.25, 3.75), (11.25, -26.25), (-3.75, -26.25), (-3.75, 3.75)]
    )
    shape.collision_type = collision_types["mblock"]
    shape.friction = 0.6
    shape.elasticity = 0
    shape.color = pygame.Color("yellow")
    shape2 = pymunk.Poly(
        body, [(-18.75, 3.75), (11.25, 3.75), (11.25, 18.75), (-18.75, 18.75)]
    )
    shape2.collision_type = collision_types["mblock"]
    shape2.friction = 0.6
    shape2.elasticity = 0
    shape2.color = pygame.Color("yellow")
    jblocks.append(shape)
    return (body, shape, shape2)


def block5(space, pos, rotation):
    body = pymunk.Body(1, 500, body_type=pymunk.Body.DYNAMIC)
    body.position = ((pos[0]), (pos[1]))
    shape = pymunk.Poly(body, [(-22.5, 0), (-22.5, -15), (+7.5, 0), (+7.5, -15)])
    shape.collision_type = collision_types["block"]
    shape.friction = 0.6
    shape.elasticity = 0
    shape.color = pygame.Color("green")
    shape2 = pymunk.Poly(body, [(22.5, 0), (22.5, +15), (-7.5, 0), (-7.5, +15)])
    shape2.collision_type = collision_types["block"]
    shape2.friction = 0.6
    shape2.elasticity = 0
    shape2.color = pygame.Color("green")
    body.angle = rotation * 1.5708
    zblocks.append(shape)
    space.add(body, shape, shape2)


def block5k(space, position):
    body = pymunk.Body(1, 500, body_type=pymunk.Body.KINEMATIC)
    body.position = ((position[0]), (position[1]))
    shape = pymunk.Poly(body, [(-22.5, 0), (-22.5, -15), (+7.5, 0), (+7.5, -15)])
    shape.collision_type = collision_types["mblock"]
    shape.friction = 0.6
    shape.elasticity = 0
    shape.color = pygame.Color("green")
    shape2 = pymunk.Poly(body, [(22.5, 0), (22.5, +15), (-7.5, 0), (-7.5, +15)])
    shape2.collision_type = collision_types["mblock"]
    shape2.friction = 0.6
    shape2.elasticity = 0
    shape2.color = pygame.Color("green")
    zblocks.append(shape)
    return (body, shape, shape2)


def block6(space, pos, rotation):
    body = pymunk.Body(1, 500, body_type=pymunk.Body.DYNAMIC)
    body.position = ((pos[0]), (pos[1]))
    shape = pymunk.Poly(body, [(-7.5, 0), (-7.5, -15), (+22.5, -15), (+22.5, 0)])
    shape.collision_type = collision_types["block"]
    shape.friction = 0.6
    shape.elasticity = 0
    shape.color = pygame.Color("orange")
    shape2 = pymunk.Poly(body, [(-22.5, 0), (-22.5, +15), (+7.5, 0), (+7.5, +15)])
    shape2.collision_type = collision_types["block"]
    shape2.friction = 0.6
    shape2.elasticity = 0
    shape2.color = pygame.Color("orange")
    body.angle = rotation * 1.5708
    space.add(body, shape, shape2)
    sblocks.append(shape)


def block6k(space, position):
    body = pymunk.Body(1, 500, body_type=pymunk.Body.KINEMATIC)
    body.position = ((position[0]), (position[1]))
    shape = pymunk.Poly(body, [(-7.5, 0), (-7.5, -15), (+22.5, -15), (+22.5, 0)])
    shape.collision_type = collision_types["mblock"]
    shape.friction = 0.6
    shape.elasticity = 0
    shape.color = pygame.Color("orange")
    shape2 = pymunk.Poly(body, [(-22.5, 0), (-22.5, +15), (+7.5, 0), (+7.5, +15)])
    shape2.collision_type = collision_types["mblock"]
    shape2.friction = 0.6
    shape2.elasticity = 0
    shape2.color = pygame.Color("orange")
    sblocks.append(shape)
    return (body, shape, shape2)


def block7(space, pos, rotation):
    body = pymunk.Body(1, 500, body_type=pymunk.Body.DYNAMIC)
    body.position = ((pos[0]), (pos[1]))
    shape = pymunk.Poly(
        body, [(-3.75, -3.75), (-3.75, -18.75), (11.25, -3.75), (11.25, -18.75)]
    )
    shape.collision_type = collision_types["block"]
    shape.friction = 0.6
    shape.elasticity = 0
    shape.color = pygame.Color("pink")
    shape2 = pymunk.Poly(
        body, [(-18.75, -3.75), (-18.75, +11.25), (26.25, -3.75), (26.25, +11.25)]
    )
    shape2.collision_type = collision_types["block"]
    shape2.friction = 0.6
    shape2.elasticity = 0
    shape2.color = pygame.Color("pink")
    body.angle = rotation * 1.5708
    space.add(body, shape, shape2)
    tblocks.append(shape)


def block7k(space, position):
    body = pymunk.Body(1, 500, body_type=pymunk.Body.KINEMATIC)
    body.position = ((position[0] + 3.75), (position[1] + 3.75))
    shape = pymunk.Poly(
        body, [(-3.75, -3.75), (-3.75, -18.75), (11.25, -3.75), (11.25, -18.75)]
    )
    shape.collision_type = collision_types["mblock"]
    shape.friction = 0.6
    shape.elasticity = 0
    shape.color = pygame.Color("pink")
    shape2 = pymunk.Poly(
        body, [(-18.75, -3.75), (-18.75, +11.25), (26.25, -3.75), (26.25, +11.25)]
    )
    shape2.collision_type = collision_types["mblock"]
    shape2.friction = 0.6
    shape2.elasticity = 0
    shape2.color = pygame.Color("pink")
    tblocks.append(shape)
    return (body, shape, shape2)


def spawn_block(space, position):  # pick a kinematic block to spawn
    global blocknum  # global variable but who really cares
    blocknum = random.randint(1, 7)
    if blocknum == 1:
        dets = block1k(space, position)
    if blocknum == 2:
        dets = block2k(space, position)
    if blocknum == 3:
        dets = block3k(space, position)
    if blocknum == 4:
        dets = block4k(space, position)
    if blocknum == 5:
        dets = block5k(space, position)
    if blocknum == 6:
        dets = block6k(space, position)
    if blocknum == 7:
        dets = block7k(space, position)
    return dets


def spawnrealblock(
    space, pos, rotation
):  # spawn a dynamic block based on what kinematic block is present
    if blocknum == 1:
        block1(space, pos, rotation)
    if blocknum == 2:
        block2(space, pos, rotation)
    if blocknum == 3:
        block3(space, pos, rotation)
    if blocknum == 4:
        block4(space, pos, rotation)
    if blocknum == 5:
        block5(space, pos, rotation)
    if blocknum == 6:
        block6(space, pos, rotation)
    if blocknum == 7:
        block7(space, pos, rotation)


def convtomin(time):  # convert time into minute:seconds format
    minutes = time // 60
    seconds = time % 60
    if seconds < 10:
        return str(minutes) + ":0" + (str(seconds))
    else:
        return str(minutes) + ":" + (str(seconds))


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


def draw_text(text, font, color, surface, x, y):  # draw text
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def createleaderboard(newscore):  # creates leaderboard
    scores = []
    leaderboard = open("imagesandsuch/scores.txt", "r")
    for score in leaderboard:
        scores.append(score)
    scores.append(newscore)
    scores.sort(reverse=True)
    if len(scores) == 11:
        scores.pop()
    leaderboard.close()

    leaderboard = open("imagesandsuch/scores.txt", "w")
    for score in scores:
        leaderboard.write(score)
    leaderboard.close()


def completeachievement(num):  # completes achievement
    achievementschecklist = []
    achievementlist = open("imagesandsuch/achievementlist.txt", "r")
    for line in achievementlist:
        achievementschecklist.append(line)
    achievementlist.close()
    achievementschecklist[num] = "1\n"

    achievementlist = open("imagesandsuch/achievementlist.txt", "w")
    for ach in achievementschecklist:
        achievementlist.write(ach)
    achievementlist.close()


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
                completeachievement(1)
                main()
        if ldbbutton.collidepoint(pos):
            if click:
                leaderboard()
        if achievbutton.collidepoint(pos):
            if click:
                achievements()
        if storebutton.collidepoint(pos):
            if click:
                store()

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


def startwindevent():
    num = random.randint(1, 3000)
    if num == 827:
        return True
    else:
        return False


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


def convtorad(angle):  # convert degrees to radians and changes sign
    radians = (0 - angle) * (math.pi / 180)
    return radians


def calcscore(time, lost):  # calculate score from time and blocks lost
    score = int(1000 * (4 ** (-(0.02 + (0.0005 * bl)) * time)))
    return str(score)


def calcmoragain(time, lost):
    score = int(1000 * (4 ** (-(0.02 + (0.0005 * bl)) * time)))
    return int(score / 100)


def main():  # start da game!
    global collision  # yeah thats right i have a global variable and what
    global bl  # yeah thats right another one
    global touch  # MHM ANOTHA ONE (its all cuz idk how to send variables to handler functions lol)

    touch = False
    timercooldown = 600
    windtimer = 0
    collision = False  # statuses/counts
    running = True

    placed = True
    gainedcoins = False
    timer = 0
    rotation = 0
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
        #pygame.mixer.music.load("imagesandsuch/un_sospiro.mp3")
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
        #pygame.mixer.music.load("imagesandsuch/liebestraum.mp3")
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

    #pygame.mixer.music.play(loops=1000000, start=5.0, fade_ms=2000)

    def autospace(
        arbiter, space, data
    ):  # automatically drops block when piece-in-play collides with another piece
        global collision
        collision = True
        return True

    def blocklost(arbiter, space, data):
        global bl
        if blocknum < 3:
            bl = bl + 1
        else:
            bl = bl + 0.5
        return True

    def starttimer(arbiter, space, data):
        global touch
        touch = True
        return False

    def stoptimer(arbiter, space, data):
        global touch
        touch = False

    blockhandler = space.add_collision_handler(
        collision_types["mblock"], collision_types["block"]
    )
    blockhandler.begin = (
        autospace  # detect collisions between piece-in-play and other pieces
    )

    voidhandler = space.add_collision_handler(
        collision_types["bottom"], collision_types["block"]
    )
    voidhandler.begin = blocklost  # detect when a block falls off

    voidhandler2 = space.add_collision_handler(
        collision_types["bottom"], collision_types["mblock"]
    )
    voidhandler2.begin = blocklost  # detect when a non-placed block isnt placed (you gotta be trash to let that happen bruh)

    winhandler = space.add_collision_handler(
        collision_types["top"], collision_types["block"]
    )
    winhandler.begin = starttimer
    winhandler.separate = stoptimer

    setup(space)  # create ground

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
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                if int(storelist[1]) > 0 and timercooldown == 0:
                    completeachievement(3)
                    storelist[1] = str(int(storelist[1]) - 1)
                    timer = timer - 180
                    timercooldown = 600
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                if not placed:
                    if int(storelist[2]) > 0:
                        completeachievement(3)
                        storelist[2] = str(int(storelist[2]) - 1)
                        if blocknum <= 2:
                            if blocknum == 1:
                                iblocks.remove(shape)
                            else:
                                oblocks.remove(shape)

                            pos = body.position
                            space.remove(body, shape)
                        else:
                            if blocknum == 3:
                                lblocks.remove(shape)
                            if blocknum == 4:
                                jblocks.remove(shape)
                            if blocknum == 5:
                                zblocks.remove(shape)
                            if blocknum == 6:
                                sblocks.remove(shape)
                            if blocknum == 7:
                                tblocks.remove(shape)

                            pos = body.position
                            space.remove(body, shape, shape2)
                        rotation = 0
                        collision = False
                        blockchars = spawn_block(space, (196, 50))
                        if blocknum < 3:
                            body = blockchars[0]
                            shape = blockchars[1]
                            space.add(body, shape)
                        else:
                            body = blockchars[0]
                            shape = blockchars[1]
                            shape2 = blockchars[2]
                            space.add(body, shape, shape2)

            elif (
                event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
            ):  # either spawn or drop block
                if placed and not win:
                    blockchars = spawn_block(space, (196, 50))
                    if blocknum < 3:
                        body = blockchars[0]
                        shape = blockchars[1]
                        space.add(body, shape)
                    else:
                        body = blockchars[0]
                        shape = blockchars[1]
                        shape2 = blockchars[2]
                        space.add(body, shape, shape2)

                    placed = False
                    continue

                if not placed:
                    if blocknum <= 2:
                        if blocknum == 1:
                            iblocks.remove(shape)
                        else:
                            oblocks.remove(shape)

                        pos = body.position
                        space.remove(body, shape)
                        spawnrealblock(space, pos, (rotation % 4))
                    else:
                        if blocknum == 3:
                            lblocks.remove(shape)
                        if blocknum == 4:
                            jblocks.remove(shape)
                        if blocknum == 5:
                            zblocks.remove(shape)
                        if blocknum == 6:
                            sblocks.remove(shape)
                        if blocknum == 7:
                            tblocks.remove(shape)

                        pos = body.position
                        space.remove(body, shape, shape2)
                        spawnrealblock(space, pos, (rotation % 4))

                    placed = True
                    rotation = 0
                    collision = False
                    bd = bd + 1

            elif (
                event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT
            ):  # movement and rotation
                if not placed:
                    pos = body.position
                    body.position = ((pos[0] + 7.5), (pos[1]))

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if not placed:
                    body.velocity = (0, 100)
                    down = True

            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                if not placed:
                    body.velocity = (0, 0)
                    down = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if not placed:
                    body.position = ((pos[0] - 7.5), (pos[1]))

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                if not placed:
                    body.angle += 1.5708
                    rotation += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if music:
                    pygame.mixer.music.pause()
                    music = False
                else:
                    pygame.mixer.music.unpause()
                    music = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        fps = 60.0
        dt = 1.0 / fps
        space.step(dt)
        clock.tick(fps)
        space.debug_draw(DrawOptions(screen))
        if not win:
            if windtimer == 0:
                windevent = False
                if not placed and not down:
                    shape.body.velocity = (0, 0)
                if startwindevent():
                    windtimer = 600
                    windevent = True
                    print("wind")
            if windtimer > 0:
                if windtimer % 30 == 0:
                    if not placed:
                        shape.body.velocity = (random.randint(-80, 80), 0)
                windtimer = windtimer - 1
        if timercooldown > 0:
            timercooldown = timercooldown - 1

        if not placed:
            timer = timer + 1

        if not placed:  # moves pieces down as timer
            pos = body.position
            body.position = ((pos[0]), (pos[1] + 0.35))

        if collision:  # place block if collision happens
            if blocknum <= 2:
                if blocknum == 1:
                    iblocks.remove(shape)
                else:
                    oblocks.remove(shape)

                pos = body.position
                space.remove(body, shape)
                spawnrealblock(space, pos, (rotation % 4))

            else:
                if blocknum == 3:
                    lblocks.remove(shape)
                if blocknum == 4:
                    jblocks.remove(shape)
                if blocknum == 5:
                    zblocks.remove(shape)
                if blocknum == 6:
                    sblocks.remove(shape)
                if blocknum == 7:
                    tblocks.remove(shape)

                pos = body.position
                space.remove(body, shape, shape2)
                spawnrealblock(space, pos, (rotation % 4))

            placed = True
            rotation = 0
            collision = False
            bd = bd + 1

        lost = str(math.trunc(bl))
        timetext = font.render(storelist[1], storefont, (0, 0, 0))
        losttext = font.render(storelist[2], storefont, [0, 0, 0])

        screen.blit(bg, (0, 0))
        screen.blit(finishline, (0, 126))
        screen.blit(timetext, (25, 37))
        screen.blit(losttext, (40, 57))
        if windevent:
            screen.blit(windimg, (0, 0))

        draw_text(("Blocks Dropped: " + str(bd)), font, (0, 0, 0), screen, 0, 0)
        draw_text(("Blocks Lost: " + lost), font, (0, 0, 0), screen, 0, 18)
        draw_text(
            ("Time: " + convtomin(int((timer / 60)))), font, (0, 0, 0), screen, 270, 0
        )

        for block in iblocks:  # draw sprites
            p = block.body.position
            p = Vec2d(p.x, p.y)
            angle_degrees = math.degrees(-(block.body.angle))
            rotated_block = pygame.transform.rotate(iblock, angle_degrees)
            offset = Vec2d(*rotated_block.get_size()) / 2
            p = p - offset
            screen.blit(rotated_block, (round(p.x), round(p.y)))
        for block in lblocks:
            p = block.body.position
            p = Vec2d((p.x), (p.y))
            angle_degrees = math.degrees(-(block.body.angle))
            rotated_block = pygame.transform.rotate(lblock, angle_degrees)
            transoffset = Vec2d(*rotated_block.get_size()) / 2
            angoffset = (
                (5.3033 * math.sin((convtorad(angle_degrees)) + 0.785)),
                -(5.3033 * math.cos((convtorad(angle_degrees)) + 0.785)),
            )
            p = p - transoffset + angoffset
            screen.blit(rotated_block, (round(p.x), round(p.y)))
        for block in oblocks:
            p = block.body.position
            p = Vec2d((p.x), (p.y))
            angle_degrees = math.degrees(-(block.body.angle))
            rotated_block = pygame.transform.rotate(oblock, angle_degrees)
            offset = Vec2d(*rotated_block.get_size()) / 2
            p = p - offset
            screen.blit(rotated_block, (round(p.x), round(p.y)))
        for block in jblocks:
            p = block.body.position
            p = Vec2d((p.x), (p.y))
            angle_degrees = math.degrees(-(block.body.angle))
            rotated_block = pygame.transform.rotate(jblock, angle_degrees)
            transoffset = Vec2d(*rotated_block.get_size()) / 2
            angoffset = (
                -(5.3033 * math.cos((convtorad(angle_degrees)) + 0.785)),
                -(5.3033 * math.sin((convtorad(angle_degrees)) + 0.785)),
            )
            p = p - transoffset + angoffset
            screen.blit(rotated_block, (round(p.x), round(p.y)))
        for block in zblocks:
            p = block.body.position
            p = Vec2d((p.x), (p.y))
            angle_degrees = math.degrees(-(block.body.angle))
            rotated_block = pygame.transform.rotate(zblock, angle_degrees)
            transoffset = Vec2d(*rotated_block.get_size()) / 2
            p = p - transoffset
            screen.blit(rotated_block, (round(p.x), round(p.y)))
        for block in sblocks:
            p = block.body.position
            p = Vec2d((p.x), (p.y))
            angle_degrees = math.degrees(-(block.body.angle))
            rotated_block = pygame.transform.rotate(sblock, angle_degrees)
            transoffset = Vec2d(*rotated_block.get_size()) / 2
            p = p - transoffset
            screen.blit(rotated_block, (round(p.x), round(p.y)))
        for block in tblocks:
            p = block.body.position
            p = Vec2d((p.x), (p.y))
            angle_degrees = math.degrees(-(block.body.angle))
            rotated_block = pygame.transform.rotate(tblock, angle_degrees)
            transoffset = Vec2d(*rotated_block.get_size()) / 2
            angoffset = (
                (5.3033 * math.sin((convtorad(angle_degrees)) + 0.785)),
                -(5.3033 * math.cos((convtorad(angle_degrees)) + 0.785)),
            )
            p = p - transoffset + angoffset
            screen.blit(rotated_block, (round(p.x), round(p.y)))

        if touch:
            wintick = wintick + 1

            if (int(wintick / 60)) == 1:
                draw_text(("3"), menufont, (0, 0, 0), screen, 170, 300)
            if (int(wintick / 60)) == 2:
                draw_text(("2"), menufont, (0, 0, 0), screen, 170, 300)
            if (int(wintick / 60)) == 3:
                draw_text(("1"), menufont, (0, 0, 0), screen, 170, 300)
            if (int(wintick / 60)) == 4:
                win = True

        if not touch:
            wintick = 0

        if win:
            completeachievement(2)

            if bl == 0:
                completeachievement(4)
            if (timer / 60) < 15:
                completeachievement(5)
                completeachievement(0)
            if (timer / 60) < 60:
                completeachievement(0)

            coingain = calcmoragain(timer / 60, bl)
            # leaderboardscore = str('Score:'+ calcscore(timer/60,bl) + 'Time: '+ convtomin(int((timer/60))))
            escbutton = pygame.Rect(120, 265, 146, 50)
            draw_text(("you win!"), menufont, (0, 0, 0), screen, 10, 200)
            draw_text(
                ("Time: " + convtomin(int((timer / 60)))),
                winfont,
                (0, 0, 0),
                screen,
                50,
                320,
            )
            draw_text(
                ("Score: " + calcscore(timer / 60, bl)),
                winfont,
                (0, 0, 0),
                screen,
                50,
                370,
            )
            draw_text(
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
        

    iblocks.clear()
    lblocks.clear()
    jblocks.clear()
    oblocks.clear()
    sblocks.clear()
    zblocks.clear()
    tblocks.clear()

    createleaderboard(
        calcscore(timer / 60, bl) + " Time:" + convtomin(int((timer / 60))) + "\n"
    )
    pygame.mixer.music.stop()


if __name__ == "__main__":
    sys.exit(menu())
