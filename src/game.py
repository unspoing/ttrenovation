import random
import sys
import math

import pygame
import pymunk

import functions

from achievements import achievements, completeachievement
from blocks import COLLISION_TYPES
from environment import setup
from gui import GUI
from leaderboard import leaderboard
from store import store

pygame.init()

W, H = 400, 600

game = GUI("font/pixelfont.ttf", W, H)
pygame.display.set_caption("tricky towers knockoff")


def menu():
    # show main menu
    game.screen.fill("black")

    click = False
    # load everything
    background = pygame.image.load("imagesandsuch/background.png")
    playimg = pygame.image.load("imagesandsuch/startbutton.png")
    achievementimg = pygame.image.load("imagesandsuch/achievementbutton.png")
    leaderboardimg = pygame.image.load("imagesandsuch/leaderboardbutton.png")
    storeimg = pygame.image.load("imagesandsuch/storebutton.png")

    bg = pygame.transform.scale(background, (W, H))

    # start game
    while True:
        pos = pygame.mouse.get_pos()
        # draw everything
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
                completeachievement(1)
                main()
        if ldbbutton.collidepoint(pos):
            if click:
                leaderboard(game)
        if achievbutton.collidepoint(pos):
            if click:
                achievements(game)
        if storebutton.collidepoint(pos):
            if click:
                store(game)

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
    global touch, bl

    functions.touch = False
    functions.bl = 0
    touch = False
    bl = 0

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
    click = False
    windevent = False
    down = False

    blocks_on_screen = []

    space = pymunk.Space()
    space.gravity = (0, 900)

    background = pygame.image.load("imagesandsuch/gamebg.png")
    finishline = pygame.image.load("imagesandsuch/finishline.png")
    backbutton = pygame.image.load("imagesandsuch/backbutton.png")
    windimg = pygame.image.load("imagesandsuch/wind.png")

    bg = pygame.transform.scale(background, (W, H))

    storelist = functions.read_storelist()
    
    # play music if one desires
    if storelist[4] == "0":
        pygame.mixer.music.load("imagesandsuch/un_sospiro.mp3")
    else:
        pygame.mixer.music.load("imagesandsuch/liebestraum.mp3")

    block_images = functions.load_block_images(storelist[4] != "0")
    pygame.mixer.music.play(loops=1000000, start=5.0, fade_ms=2000)

    blockhandler = space.add_collision_handler(
        COLLISION_TYPES["mblock"], COLLISION_TYPES["block"]
    )

    voidhandler = space.add_collision_handler(
        COLLISION_TYPES["bottom"], COLLISION_TYPES["block"]
    )
    voidhandler.data["blocks_on_screen"] = blocks_on_screen
    voidhandler.begin = functions.blocklost

    voidhandler2 = space.add_collision_handler(
        COLLISION_TYPES["bottom"], COLLISION_TYPES["mblock"]
    )
    voidhandler2.data["blocks_on_screen"] = blocks_on_screen
    voidhandler2.begin = functions.blocklost

    winhandler = space.add_collision_handler(
        COLLISION_TYPES["top"], COLLISION_TYPES["block"]
    )
    winhandler.begin = functions.starttimer
    winhandler.separate = functions.stoptimer

    setup(space)

    block = functions.create_block((196, 50))
    blockhandler.begin = block.collide
    blocks_on_screen.append(block)
    functions.add_block_to_space(space, block)
    placed = False

    while running:
        storelist = functions.read_storelist()
        mpos = pygame.mouse.get_pos()

        timetext = game.font.render(storelist[1], game.storefont, (0, 0, 0))
        losttext = game.font.render(storelist[2], game.storefont, [0, 0, 0])

        game.screen.blit(losttext, (40, 57))
        game.screen.blit(timetext, (25, 37))

        for event in pygame.event.get():
            mpos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            timercooldown, timer = functions.handle_time_skip(
                event, storelist, timercooldown, timer
            )

            block = functions.handle_skip_block(
                event, block, placed, win, space, blocks_on_screen, blockhandler
            )

            block, placed, bd = functions.handle_spawning(
                event, block, placed, win, space, blocks_on_screen, bd, blockhandler
            )

            down = functions.handle_movement(event, block, placed, down)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if music:
                    pygame.mixer.music.pause()
                    music = False
                else:
                    pygame.mixer.music.unpause()
                    music = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        touch = functions.touch
        bl = functions.bl

        if not win:
            if windtimer == 0:
                windevent = False
                if not placed and not down:
                    block.set_velocity((0, 0))
                if functions.startwindevent():
                    windtimer = 600
                    windevent = True
            if windtimer > 0:
                if windtimer % 30 == 0:
                    if not placed:
                        block.set_velocity((random.randint(-80, 80), 0))
                windtimer = windtimer - 1

        if timercooldown > 0:
            timercooldown = timercooldown - 1

        if not placed:
            timer += 1
            pos = block.get_position()
            block.set_position((pos[0], pos[1] + 0.35))

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
        functions.draw_text(
            ("Blocks Lost: " + lost), game.font, (0, 0, 0), game.screen, 0, 18
        )
        functions.draw_text(
            ("Time: " + functions.convtomin(int((timer / 60)))),
            game.font,
            (0, 0, 0),
            game.screen,
            270,
            0,
        )

        for screen_block in blocks_on_screen:
            functions.draw_sprite(screen_block, game.screen, block_images)

        if touch:
            wintick = wintick + 1

            if (int(wintick / 60)) == 1:
                functions.draw_text(
                    ("3"), game.menufont, (0, 0, 0), game.screen, 170, 300
                )
            if (int(wintick / 60)) == 2:
                functions.draw_text(
                    ("2"), game.menufont, (0, 0, 0), game.screen, 170, 300
                )
            if (int(wintick / 60)) == 3:
                functions.draw_text(
                    ("1"), game.menufont, (0, 0, 0), game.screen, 170, 300
                )
            if (int(wintick / 60)) == 4:
                win = True

        if not touch:
            wintick = 0

        for screen_block in list(blocks_on_screen):
            if screen_block.get_position()[1] > 700:
                functions.remove_block_from_space(space, screen_block)
                blocks_on_screen.remove(screen_block)

        if win:
            completeachievement(2)

            if bl == 0:
                completeachievement(4)
            if (timer / 60) < 15:
                completeachievement(5)
                completeachievement(0)
            if (timer / 60) < 60:
                completeachievement(0)

            coingain = functions.calcmoragain(timer / 60, bl)
            escbutton = pygame.Rect(120, 265, 146, 50)
            functions.draw_text(
                ("you win!"), game.menufont, (0, 0, 0), game.screen, 10, 200
            )
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

            if escbutton.collidepoint(mpos):
                if click:
                    running = False

            click = False

        time_icon = pygame.image.load("imagesandsuch/timeicon.png")
        skip = pygame.image.load("imagesandsuch/skipicon.png")

        timeicon = pygame.transform.scale(time_icon, (20, 20))
        skipicon = pygame.transform.scale(skip, (40, 20))

        game.screen.blit(timeicon, (0, 30))
        game.screen.blit(skipicon, (0, 50))

        functions.write_storelist(storelist)

        pygame.display.flip()

    blocks_on_screen.clear()
    functions.createleaderboard(
        functions.calcscore(timer / 60, bl)
        + " Time:"
        + functions.convtomin(int((timer / 60)))
        + "\n"
    )
    pygame.mixer.music.stop()


if __name__ == "__main__":
    sys.exit(menu())
