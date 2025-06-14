import pygame
from bullet import Bullet
from health_bar import Health_bar
from colors import *
from pygame import mixer

mixer.init()

class Player():
    def __init__(self, x, y, data):
        # store image and animation frames
        self.size = data['frame_size']
        self.image_scale = data['scale']
        self.offset_list = data['offsets']
        self.animations = {} # store all animation frames
        self.action = 'idle' # keep track of what the player doing (running, attacking, walking, etc.)
        self.frame_index = 0
        self.image = None # keep track of what frame im in
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 40, 85) # Hit box
        
        # animation movement
        self.vel_y = 0 # velocity y - how fast player moving up and down
        self.flip = False
        self.walking = False
        self.running = False
        self.jump = False
        self.attacking = False
        self.ammo = 30
        self.max_ammo = 30
        self.recharge_gun = False
        self.shot = False
        self.shoot_cooldown = 0
        self.bullet_img = pygame.image.load('bullet.png').convert_alpha()
        self.bullet_group = pygame.sprite.Group()  # create group of bullets here
        self.hurt = False
        self.attack_cooldown = 0
        self.shoot_cooldown = 0
        self.dead = False
        self.health = 100
        self.max_health = 100
        self.health_bar = Health_bar(40, 40, 300, 20, self.health, self.max_health)

        # sound
        self.is_sound_playing = False
        self.walking_sound = pygame.mixer.Sound('music_and_sound/walking_grass.mp3')
        self.reloading_sound = pygame.mixer.Sound('music_and_sound/gun_reload_sound.mp3')
        self.shooting_sound = pygame.mixer.Sound('music_and_sound/gun_shot_sound.mp3')
        self.shooting_sound.set_volume(0.1)
        self.swinging_sound = pygame.mixer.Sound('music_and_sound/swinging_sound.mp3')
    
    def load_animation(self, action_name, sprite_sheet_path, frame_count):
        # load a specific animation from its sprite_sheet
        sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        frames = []
        for x in range(frame_count):
            frame = sheet.subsurface(x * self.size, 0, self.size, self.size)
            scaled_frame = pygame.transform.scale(frame, (self.size * self.image_scale, self.size * self.image_scale))
            frames.append(scaled_frame)
        self.animations[action_name] = frames # store complete animation in a list under its action
    
    def move(self, screen_width, screen_height, target):
        SPEED = 4
        GRAVITY = 2
        GROUND_LEVEL = screen_height - 40
        dx = 0
        dy = 0
        self.walking = False
        self.running = False
        keys = pygame.key.get_pressed()

        # check if player starting to move to play the sound
        if (keys[pygame.K_a] or keys[pygame.K_d]) and not self.is_sound_playing:
            self.walking_sound.play(loops=-1)  # -1 for infinite looping
            self.is_sound_playing = True
            self.walking = True
        elif not (keys[pygame.K_a] or keys[pygame.K_d]) and self.is_sound_playing:
            self.walking_sound.stop()
            self.is_sound_playing = False
            self.walking = False
        
        # can only perform other actions if not attacking or shooting
        if self.attacking == False and self.shot == False and self.recharge_gun == False:
            # walk left/right
            if keys[pygame.K_a]:
                dx -= SPEED
                self.walking = True
                self.flip = True
            if keys[pygame.K_d]:
                dx += SPEED
                self.flip = False
                self.walking = True
            
            # run
            if keys[pygame.K_LSHIFT]:
                if keys[pygame.K_a]:
                    dx -= SPEED
                    self.running = True
                    self.flip = True
                if keys[pygame.K_d]:
                    dx += SPEED
                    self.flip = False
                    self.running = True

            # jump
            if keys[pygame.K_w] and self.jump == False: # if player isn't jumping, they can jump (prevent double jump)
                self.vel_y = -25
                self.jump = True
            # attack 
            if keys[pygame.K_q]:
                self.attack(target)
            # shoot
            elif keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
                self.shoot()
            #recharge
            elif keys[pygame.K_r]:
                self.recharge()

        # apply gravity
        self.vel_y += GRAVITY # bring the player down after jumping
        dy += self.vel_y

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
        if self.health <= 0:
            self.health = 0
            self.dead = True
            new_action = 'dead'
        elif self.hurt:
            new_action = 'hurt'
        elif self.shot:
            new_action = 'shoot'
        elif self.recharge_gun:
            new_action = 'recharge'
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
                self.frame_index = len(self.animations[self.action]) - 1
            else:
                self.frame_index = 0
                # check if an attack, shoot, hurt and recharge were executed
                if self.action == 'attack':
                    self.attacking = False
                    self.attack_cooldown = 30
                if self.action == 'hurt':
                    self.hurt = False
                if self.action == 'shoot':
                    self.shot = False
                if self.action == 'recharge':
                    self.recharge_gun = False
    
    def attack(self, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.swinging_sound.play()
            # adjust attack based on flip
            attack_x = self.rect.left - 25 if self.flip else self.rect.right
            attacking_rect = pygame.Rect(attack_x, self.rect.y, self.rect.width - 10, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 25

    def shoot(self):
        if self.ammo > 0:
            self.shot = True
            # create bullet at gun position (adjust offsets as needed)
            bullet_x = self.rect.left if self.flip else self.rect.right
            bullet_y = self.rect.centery - 25  # adjust for gun height
            
            # add to sprite group
            new_bullet = Bullet(bullet_x, bullet_y, self.flip, self.bullet_img)
            self.bullet_group.add(new_bullet)
            self.shooting_sound.play()
            # reduce ammo
            self.ammo -= 1
    
    def recharge(self):
        if self.max_ammo > 0 and self.ammo < 30:
            self.recharge_gun = True
            needed = 30 - self.ammo
            can_take = min(needed, self.max_ammo)
            if can_take > 0:  # if actually transferring
                self.reloading_sound.play()
                self.ammo += can_take
                self.max_ammo -= can_take
                
    def draw(self, surface):
        current_offset = self.offset_list
        self.health_bar.hp = self.health

        if self.flip:
            image_to_draw = pygame.transform.flip(self.image, True, False)  # flip horizontally
        else:
            image_to_draw = self.image  # use original
        
        self.health_bar.draw(surface)
        surface.blit(image_to_draw,
            (
                self.rect.x - (current_offset[0] * self.image_scale),
                self.rect.y - (current_offset[1] * self.image_scale),
            )
        )