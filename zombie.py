import pygame
from colors import *

class Zombie():
    def __init__(self, x, y, data):
        self.size = data['frame_size']
        self.image_scale = data['scale']
        self.offset_list = data['offsets']
        self.animations = {}
        self.frame_index = 0
        self.action = 'idle'
        self.image = None # keep track of what frame im in
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 37, 85) # hit box
        self.health = 100
        self.max_health = 100
        self.flip = True
        self.walking = False
        self.running = False
        self.hurt = False
        self.dead = False
    
        # movement variables
        self.move_direction = 1  # 1 for right, -1 for left
        self.move_counter = 0
        self.patrol_distance = 100  # how far the zombie will walk before turning around
        self.speed = 2  # movement speed

    def load_animation(self, action_name, sprite_sheet_path, frame_count):
        # load a specific animation from its sprite_sheet
        sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        frames = []
        for x in range(frame_count):
            frame = sheet.subsurface(x * self.size, 0, self.size, self.size)
            scaled_frame = pygame.transform.scale(frame, (self.size * self.image_scale, self.size * self.image_scale))
            frames.append(scaled_frame)
        self.animations[action_name] = frames # store complete animation in a list under its action
    
    def ai(self, screen_width, screen_height, target):
        if not self.dead and not target.dead:
            self.move(screen_width, screen_height)
        


    def move(self, screen_width, screen_height):
        SPEED = self.speed
        GRAVITY = 2
        GROUND_LEVEL = screen_height - 40
        dx = 0
        dy = 0
        self.walking = False
        self.running = False
        
        if not self.dead and not self.hurt:
            dx -= self.move_direction * SPEED
            self.walking = True
            # track how far zombie move in current direction
            self.move_counter += abs(dx)
            
            # if moved over the patrol distance, turn around
            if self.move_counter > self.patrol_distance:
                self.move_direction *= -1  # reverse direction
                self.move_counter = 0  # reset counter
                self.flip = not self.flip  # flip the sprite
        
        # apply gravity
        if self.rect.bottom + dy < GROUND_LEVEL:
            self.rect.y += dy
        else:
            self.rect.bottom = GROUND_LEVEL

        # update zombie position
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        # check what action zombie is performing
        if self.health <= 0:
            self.health = 0
            self.dead = True
            new_action = 'dead'
        elif self.hurt:
            new_action = 'hurt'
        elif self.walking:
            new_action = 'walk'
        else:
            new_action = 'idle'

        # change animation if needed
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0

        animation_cooldown = 100 # milisecond
        # update image
        self.image = self.animations[self.action][self.frame_index]
        
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        
        # check if animation has finished
        if self.frame_index >= len(self.animations[self.action]):
            # if the zombie is dead, end the animation
            if self.dead == True:
                self.frame_index = len(self.animations[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 'hurt':
                    self.hurt = False

    def draw(self, surface):
        pygame.draw.rect(surface, blue, self.rect)
        current_offset = self.offset_list
        if self.flip:
            image_to_draw = pygame.transform.flip(self.image, True, False)  # flip horizontally
        else:
            image_to_draw = self.image  # use original

        surface.blit(image_to_draw,
            (
                self.rect.x - (current_offset[0] * self.image_scale),
                self.rect.y - (current_offset[1] * self.image_scale),
            )
        )
        # draw health bar above zombie
        health_bar_width = 60
        health_ratio = self.health / self.max_health
        pygame.draw.rect(surface, red, (self.rect.x, self.rect.y - 15, health_bar_width, 10))
        pygame.draw.rect(surface, green, (self.rect.x, self.rect.y - 15, health_bar_width * health_ratio, 10))