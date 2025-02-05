import pygame

class Tuile(pygame.sprite.Sprite):
    def __init__(self, size: int, image, sprite_group=None):
        super().__init__()
        self.image = image
        self.image = pygame.transform.scale(image, (size, size))
        self.rect = image.get_rect()
    
    def update(self):
        pass