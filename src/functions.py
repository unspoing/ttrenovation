import random
import math
import pygame
import pymunk

from blocks import Block, NORMAL_BLOCKS
from pymunk import Vec2d

# shared game state (original used globals in collision handlers)
touch = False
bl = 0


def create_block(position):  # pick a kinematic block to spawn
    block_type = random.randint(0, 6)
    block = Block(position, 0, block_type)
    return block


def add_block_to_space(space, block):
    if len(block.shape) == 1:
        space.add(block.body, block.shape[0])
    else:
        space.add(block.body, block.shape[0], block.shape[1])


def remove_block_from_space(space, block):
    if len(block.shape) == 1:
        space.remove(block.body, block.shape[0])
    else:
        space.remove(block.body, block.shape[0], block.shape[1])


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


def calcscore(time, blocks_lost):  # calculate score from time and blocks lost
    score = int(1000 * (4 ** (-(0.02 + (0.0005 * blocks_lost)) * time)))
    return str(score)


def calcmoragain(time, blocks_lost):
    score = int(1000 * (4 ** (-(0.02 + (0.0005 * blocks_lost)) * time)))
    return int(score / 100)


def drop_block(block, space):
    remove_block_from_space(space, block)
    block.change_body_type(block.get_position(), block.get_angle(), "DYNAMIC")
    add_block_to_space(space, block)


def find_block_by_body(blocks_on_screen, body):
    for block in blocks_on_screen:
        if block.body is body:
            return block
    return None


def blocklost(arbiter, space, data):
    global bl
    blocks_on_screen = data.get("blocks_on_screen", [])

    for shape in arbiter.shapes:
        if shape.body.body_type == pymunk.Body.DYNAMIC:
            block = find_block_by_body(blocks_on_screen, shape.body)
            if block and block.name in NORMAL_BLOCKS:
                bl = bl + 1
            elif block:
                bl = bl + 0.5
            break

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
        elif (
            event.type == pygame.KEYUP and event.key == pygame.K_DOWN
        ):  # stop moving down
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


def handle_spawning(
    event, block, placed, win, space, blocks_on_screen, bd, blockhandler
):
    # handle spawning blocks
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        if placed and not win:
            block = create_block((196, 50))
            blockhandler.begin = block.collide
            blocks_on_screen.append(block)
            add_block_to_space(space, block)
            placed = False
        elif not placed:
            drop_block(block, space)
            placed = True
            bd += 1

    return block, placed, bd


def handle_skip_block(event, block, placed, win, space, blocks_on_screen, blockhandler):
    # skip current block
    if event.type == pygame.KEYDOWN and event.key == pygame.K_v and not placed:
        if int(read_storelist()[2]) > 0:
            from achievements import completeachievement

            completeachievement(3)
            storelist = read_storelist()
            storelist[2] = str(int(storelist[2]) - 1)
            write_storelist(storelist)

            remove_block_from_space(space, block)
            blocks_on_screen.remove(block)

            block = create_block((196, 50))
            blockhandler.begin = block.collide
            blocks_on_screen.append(block)
            add_block_to_space(space, block)
            block.collision = False

    return block


def handle_time_skip(event, storelist, timercooldown, timer):
    # use time skip consumable
    if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
        if int(storelist[1]) > 0 and timercooldown == 0:
            from achievements import completeachievement

            completeachievement(3)
            storelist[1] = str(int(storelist[1]) - 1)
            timer = timer - 180
            timercooldown = 600

    return timercooldown, timer


def read_storelist():
    storelist = []
    with open("imagesandsuch/storeinfo.txt", "r") as storeinfo:
        for line in storeinfo:
            storelist.append(line[:-1])

    return storelist


def write_storelist(storelist):
    with open("imagesandsuch/storeinfo.txt", "w") as storeedit:
        for val in storelist:
            storeedit.write(val + "\n")


def load_block_images(sakura_equipped):
    suffix = "sakura" if sakura_equipped else ""
    prefix = "imagesandsuch/"
    names = ["iblock", "lblock", "oblock", "jblock", "zblock", "sblock", "tblock"]
    images = {}
    for name in names:
        filename = f"{name}{suffix}.png" if suffix else f"{name}.png"
        img = pygame.image.load(prefix + filename)
        img.set_colorkey(0)
        images[name] = img
        
    return images


def createleaderboard(newscore):
    scores = []
    with open("imagesandsuch/scores.txt", "r") as leaderboard:
        for score in leaderboard:
            scores.append(score)
    scores.append(newscore)
    scores.sort(reverse=True)
    if len(scores) == 11:
        scores.pop()

    with open("imagesandsuch/scores.txt", "w") as leaderboard:
        for score in scores:
            leaderboard.write(score)


def draw_sprite(block, screen, blockImages):
    # I MAY BE THE GOAT ON THE ANGLE MATH
    if block.name == "lblock" or block.name == "tblock":
        pos = block.get_position()
        pos = Vec2d((pos.x), (pos.y))
        angle_degrees = math.degrees(-(block.get_angle()))
        rotated_block = pygame.transform.rotate(blockImages[block.name], angle_degrees)
        transoffset = Vec2d(*rotated_block.get_size()) / 2
        angoffset = (
            (5.3033 * math.sin((convtorad(angle_degrees)) + 0.785)),
            -(5.3033 * math.cos((convtorad(angle_degrees)) + 0.785)),
        )
        pos = pos - transoffset + angoffset
        screen.blit(rotated_block, (round(pos.x), round(pos.y)))
    elif block.name == "jblock":
        pos = block.get_position()
        pos = Vec2d((pos.x), (pos.y))
        angle_degrees = math.degrees(-(block.get_angle()))
        rotated_block = pygame.transform.rotate(blockImages[block.name], angle_degrees)
        transoffset = Vec2d(*rotated_block.get_size()) / 2
        angoffset = (
            -(5.3033 * math.cos((convtorad(angle_degrees)) + 0.785)),
            -(5.3033 * math.sin((convtorad(angle_degrees)) + 0.785)),
        )
        pos = pos - transoffset + angoffset
        screen.blit(rotated_block, (round(pos.x), round(pos.y)))

    else:
        pos = block.body.position
        pos = Vec2d((pos.x), (pos.y))
        angle_degrees = math.degrees(-(block.body.angle))
        rotated_block = pygame.transform.rotate(blockImages[block.name], angle_degrees)
        offset = Vec2d(*rotated_block.get_size()) / 2
        pos = pos - offset
        screen.blit(rotated_block, (round(pos.x), round(pos.y)))
