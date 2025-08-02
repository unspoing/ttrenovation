import pymunk
COLLISION_TYPES = {
    "block": 1,  # regular placed block
    "mblock": 2,  # moving block (in control)
    "bottom": 3,  # bottom "void"
    "top": 4,  # top
}

BLOCK_SHAPES = {
    "iblock": (60, 15),
    "lblock": [
        [(-11.25, 3.75), (-11.25, -26.25), (3.75, -26.25), (3.75, 3.75)],
        [(-11.25, 3.75), (18.75, 3.75), (18.75, 18.75), (-11.25, 18.75)],
    ],
    "jblock": [
        [(11.25, 3.75), (11.25, -26.25), (-3.75, -26.25), (-3.75, 3.75)],
        [(-18.75, 3.75), (11.25, 3.75), (11.25, 18.75), (-18.75, 18.75)],
    ],
    "sblock": [
        [(-7.5, 0), (-7.5, -15), (22.5, -15), (22.5, 0)],
        [(-22.5, 0), (-22.5, 15), (7.5, 0), (7.5, 15)],
    ],
    "zblock": [
        [(-22.5, 0), (-22.5, -15), (7.5, 0), (7.5, -15)],
        [(22.5, 0), (22.5, 15), (-7.5, 0), (-7.5, 15)],
    ],
    "oblock": (30, 30),
    "tblock": [
        [(-3.75, -3.75), (-3.75, -18.75), (11.25, -3.75), (11.25, -18.75)],
        [(-18.75, -3.75), (-18.75, +11.25), (26.25, -3.75), (26.25, +11.25)],
    ],
}

NORMAL_BLOCKS = ["iblock", "oblock"]  # blocks that only require 1 shape per body


class Block:
    """
    an object in this class represents a block
    """

    def __init__(self, position, rotation, type):
        """
        creates a block object
        position - position to create the block
        rotation - number of 90 degree rotations the block has gone through
        type - a number from 1-7, representing a type of block
        """
        # create body and its position and rotation
        block_name = list(BLOCK_SHAPES.keys())[type]  # change type to block name
        body = pymunk.Body(1, 500, body_type=pymunk.Body.KINEMATIC)
        body.position = position
        body.angle = rotation * 1.5708

        self.type = type
        self.angle = rotation * 1.5708
        self.body = body
        self.name = block_name
        self.collision = False

        # if block is normal, create 1 shape for body
        if block_name in NORMAL_BLOCKS:
            shape = pymunk.Poly.create_box(body, BLOCK_SHAPES[block_name])
            shape.collision_type = COLLISION_TYPES["mblock"]
            shape.friction = 0.6
            shape.elasticity = 0

            self.shape = [shape]
        # if block is not normal, create 2 shapes for body
        else:
            shape1 = pymunk.Poly(body, BLOCK_SHAPES[block_name][0])
            shape1.collision_type = COLLISION_TYPES["mblock"]
            shape1.friction = 0.6
            shape1.elasticity = 0
            shape2 = pymunk.Poly(body, BLOCK_SHAPES[block_name][1])
            shape2.collision_type = COLLISION_TYPES["mblock"]
            shape2.friction = 0.6
            shape2.elasticity = 0

            self.shape = [shape1, shape2]
    
    def change_body_type(self, position, rotation, type):
        """
        change body type
        position - position of current body
        rotation - rotation of current body
        type - type to change body to
        """
        if type == "DYNAMIC":
            new_body = pymunk.Body(
                1, 500, body_type=pymunk.Body.DYNAMIC
            )  # create new body

            for shape in self.shape:
                shape.collision_type = COLLISION_TYPES[
                    "block"
                ]  # change collision type to placed/free block

                shape.body = new_body  # attach shape to new body
        elif type == "KINEMATIC":
            new_body = pymunk.Body(
                1, 500, body_type=pymunk.Body.KINEMATIC
            )  # create new body

            for shape in self.shape:
                shape.collision_type = COLLISION_TYPES[
                    "mblock"
                ]  # change collision type to unplaced/controlled block

                shape.body = new_body  # attach shape to new body
        else:
            new_body = pymunk.Body(
                1, 500, body_type=pymunk.Body.STATIC
            )  # create new body

            for shape in self.shape:
                shape.collision_type = COLLISION_TYPES[
                    "block"
                ]  # change collision type to placed/free block
                
                shape.body = new_body  # attach shape to new body

        new_body.position = position
        new_body.angle = rotation

        self.body = new_body

    def get_angle(self):
        """
        gets block angle
        """
        return self.body.angle

    def get_position(self):
        """
        gets block position
        """
        return self.body.position

    def get_velocity(self):
        """
        gets block velocity
        """
        return self.body.velocity

    def set_angle(self, angle):
        """
        sets block angle
        angle - angle in radians to set
        """
        self.body.angle = angle

    def set_position(self, pos):
        """
        sets block position
        pos - tuple to set block coordinates to
        """
        self.body.position = pos

    def set_velocity(self, vel):
        """
        sets block velocity
        vel - tuple to set block velocity to
        """
        self.body.velocity = vel

    def collide(self, arbiter, space, data):
        self.collision = True
        return True
    
    def void_block(self, arbiter, space, data):
        self.lost = True
        return True
    
    


def main():
    """
    testing
    """
    block = Block((0, 0), 0, 0)
    print(block.shape[0].collision_type)
    block2 = Block((0, 0), 0, 1)
    print(block2.shape[0].collision_type)
    print(block.body.position)
    block.set_position((5, 6))
    print(block.body.position)


if __name__ == "__main__":
    main()
