import pygame
from colors import *

class Zombie():
    def __init__(self, x, y, data):
        self.size = data['frame_size']
        self.image_scale = data['scale']
        self.offset_list = data['offsets']
        self.animations = {}
        self.frame_index = 0
        self.image = None # keep track of what frame im in
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 40, 85)
        self.health = 100
        self.max_health = 100
        self.hurt = False
    
    def load_animation(self, action_name, sprite_sheet_path, frame_count):
        # load a specific animation from its sprite_sheet
        sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        frames = []
        for x in range(frame_count):
            frame = sheet.subsurface(x * self.size, 0, self.size, self.size)
            scaled_frame = pygame.transform.scale(frame, (self.size * self.image_scale, self.size * self.image_scale))
            frames.append(scaled_frame)
        self.animations[action_name] = frames # store complete animation in a list under its action
    
    def draw(self, surface):
        pygame.draw.rect(surface, blue, self.rect)

        # draw health bar above zombie
        health_bar_width = 60
        health_ratio = self.health / self.max_health
        pygame.draw.rect(surface, red, (self.rect.x + 10, self.rect.y - 15, health_bar_width, 10))
        pygame.draw.rect(surface, green, (self.rect.x + 10, self.rect.y - 15, health_bar_width * health_ratio, 10))