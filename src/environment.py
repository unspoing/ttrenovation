

import pymunk
import pygame
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
