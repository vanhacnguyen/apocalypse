import pygame
from colors import *

WINDOW_WIDTH, WINDOW_HEIGHT = 640, 640

class Block(pygame.sprite.Sprite):
    def __init__(self, color = blue, width = 64, height = 64):
        super(Block, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_image(self, filename = None):
        if filename != None:
            self.image = pygame.image.load(filename)
            self.rect = self.image.get_rect()

if __name__ == "__main__":
    pygame.init()
    window_size = WINDOW_WIDTH, WINDOW_HEIGHT
    window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
    pygame.display.set_caption("Apocalypse")

    clock = pygame.time.Clock()
    frames_per_sec = 60

    block_group = pygame.sprite.Group()
    a_block = Block()
    a_block.set_position(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    a_block.set_image("wood_block.png")

    block_group.add(a_block)
    block_group.draw(window)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(frames_per_sec)
        pygame.display.update()
    pygame.quit()