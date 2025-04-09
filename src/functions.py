import random
import math
import pygame

from blocks import Block

collision_types = {
    "block": 1,
    "mblock": 2,
    "bottom": 3,
    "top": 4,
}  # block for dynamic mblock for kinematic

def create_block(position):  # pick a kinematic block to spawn
    type = random.randint(0,6)
    block = Block(position, 0 , type)  # set rotation to 0 by default
    return block

def convtomin(time):  # convert time into minute:seconds format
    minutes = time // 60
    seconds = time % 60
    if seconds < 10:
        return str(minutes) + ":0" + (str(seconds))
    else:
        return str(minutes) + ":" + (str(seconds))

def draw_text(text, font, color, surface, x, y):  # draw text
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def startwindevent():
    num = random.randint(1, 3000)
    if num == 827:
        return True
    else:
        return False
    
def convtorad(angle):  # convert degrees to radians and changes sign
    radians = (0 - angle) * (math.pi / 180)
    return radians

def calcscore(time, bl):  # calculate score from time and blocks lost
    score = int(1000 * (4 ** (-(0.02 + (0.0005 * bl)) * time)))
    return str(score)

def calcmoragain(time, bl):
    score = int(1000 * (4 ** (-(0.02 + (0.0005 * bl)) * time)))
    return int(score / 100)

def drop_block(block, space):
    if len(block.shape) == 1:
        space.remove(block.body, block.shape[0])
        block.change_body_type(block.get_position(), block.get_angle(), 'DYNAMIC')
        space.add(block.body, block.shape[0])
    else:
        space.remove(block.body, block.shape[0], block.shape[1])
        block.change_body_type(block.get_position(), block.get_angle(), 'DYNAMIC')
        space.add(block.body, block.shape[0], block.shape[1])

def blocklost(arbiter, space, data):
    global bl
    if len(arbiter.shapes) < 3:
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


def handle_movement(event, block, placed, down):
    if not placed:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:  # move right
            pos = block.get_position()
            block.set_position((pos[0] + 7.5, pos[1]))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:  # move down
            block.set_velocity((0, 100))
            down = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:  # stop moving down
            block.set_velocity((0, 0))
            down = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:  # move left
            pos = block.get_position()
            block.set_position((pos[0] - 7.5, pos[1]))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # rotate
            angle = block.get_angle()
            block.set_angle(angle + 1.5708)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:  # rotate
            angle = block.get_angle()
            block.set_angle(angle - 1.5708)
    return down


def handle_spawning(event, block, placed, win, space, BLOCKS_ON_SCREEN, bd, blockhandler):
    """Handles spawning and despawning of blocks."""
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        # If no block is currently in control:
        if placed and not win:
            block = create_block((196, 50))  # create block
            blockhandler.begin = block.collide  # start collision handler for block
            # Add to screen and space
            if len(block.shape) == 1:
                BLOCKS_ON_SCREEN.append(block)
                space.add(block.body, block.shape[0])
            else:
                BLOCKS_ON_SCREEN.append(block)
                space.add(block.body, block.shape[0], block.shape[1])
            placed = False
        # If block is currently in control:
        elif not placed:
            drop_block(block, space)
            placed = True
            bd += 1
    return block, placed, bd