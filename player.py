import pygame
from colors import *

class Player():
    def __init__(self, x, y, data):
        self.size = data['frame_size']
        self.image_scale = data['scale']
        self.offset_list = data['offsets']
        self.animations = {} # store all animation frames
        # keep track of what the player doing (running, attacking, walking, etc.)
        self.action = 'idle'
        self.frame_index = 0
        self.image = None # keep track of what frame im in
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 40, 85) # Hit box
        self.vel_y = 0 # velocity y - how fast player moving up and down
        self.flip = False
        self.walking = False
        self.running = False
        self.jump = False
        self.attacking = False
        self.hurt = False
        self.attack_cooldown = 0
        self.dead = False
        self.health = 100
    
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
        pygame.draw.rect(surface, red, self.rect)
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
    
    def move(self, screen_width, screen_height, surface, target):
        SPEED = 4
        GRAVITY = 2
        GROUND_LEVEL = screen_height - 40
        dx = 0
        dy = 0
        self.walking = False
        self.running = False

        # can only perform other actions if not attacking
        if self.attacking == False:
            # walk left/right
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_RIGHT]:
                dx -= SPEED
                self.walking = True
                self.flip = True
            if keys[pygame.K_d] or keys[pygame.K_LEFT]:
                dx += SPEED
                self.flip = False
                self.walking = True
            
            # run
            if keys[pygame.K_LSHIFT]:
                if keys[pygame.K_a]:
                    dx -= SPEED + 2
                    self.running = True
                    self.flip = True
                if keys[pygame.K_d]:
                    dx += SPEED + 2
                    self.flip = False
                    self.running = True

            # jump
            if keys[pygame.K_w] and self.jump == False: # if player isn't jumping, they can jump (prevent double jump)
                self.vel_y = -25
                self.jump = True

            # apply gravity
            self.vel_y += GRAVITY # bring the player down after jumping
            dy += self.vel_y

            # attack 
            if keys[pygame.K_q]:
                self.attack(surface, target)


        #ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.left + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > GROUND_LEVEL:
            self.vel_y = 0
            self.jump = False
            dy = GROUND_LEVEL - self.rect.bottom
        # apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # update player position
        self.rect.x += dx
        self.rect.y += dy
    
    # handle animation updates
    def update(self):
        # check what action player is performing
        # Determine action based on player state
        if self.health <= 0:
            self.health = 0
            self.dead = True
            self.action = 'dead'
        elif self.hurt:
            new_action = 'hurt'
        elif self.attacking:
            new_action = 'attack'
        elif self.running:
            new_action = 'run'
        elif self.walking:
            new_action = 'walk'
        else:
            new_action = 'idle'
        
        # change animation if needed
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0

        animation_cooldown = 100 #milisecond
        # update image
        self.image = self.animations[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # check if animation has finished
        if self.frame_index >= len(self.animations[self.action]):
            # if the player is dead, end the animation
            if self.dead == True:
                self.frame_index = len(self.animations[self.action])
            else:
                self.frame_index = 0
                # check if an attack was executed
                if self.action == 'attack':
                    self.attacking = False
                    self.attack_cooldown = 30
                if self.action == 'hurt':
                    self.hurt = False

    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            # adjust attack based on flip
            attack_x = self.rect.left - 25 if self.flip else self.rect.right
            attacking_rect = pygame.Rect(attack_x, self.rect.y, self.rect.width - 10, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 25
            pygame.draw.rect(surface, green, attacking_rect)