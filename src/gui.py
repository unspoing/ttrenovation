
import pygame

class GUI:
    def __init__(self, font, width = 400, height = 600, title = "tricky towers knockoff"):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font(font, 9)
        self.menufont = pygame.font.Font(font, 50)
        self.winfont = pygame.font.Font(font, 30)
        self.storefont = pygame.font.Font(font, 15)
        self.clock = pygame.time.Clock()
    def show_image(self,image, location):
        self.screen.blit(image, location)

    def make_button(self, size, location):
        button = pygame.Rect(location)
        pygame.draw.rect(self.screen, (255, 0, 0), button)
    