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
