import pygame

class CustomSurface:
    ''' Třída pro surface pozadi hry'''
    def __init__(self, width, height, position):
        self.surface = pygame.Surface((width, height))
        self.surface.fill((255, 0, 0))
        self.position = position

    #   nacteni obrazku
        self.image = pygame.image.load("media/grass.jpg")
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, target_surface):
        self.surface.blit(self.image, (0, 0))
        target_surface.blit(self.surface, self.position)
