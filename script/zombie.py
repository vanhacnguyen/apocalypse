import pygame
import random
from health_bar import Health_bar
from item_box import ItemBox
from colors import *
from pygame import mixer

mixer.init()

class Zombie():
    def __init__(self, x, y, data, hp = 100, damage = 10, speed = 1, score = 1):
        self.size = data['frame_size']
        self.image_scale = data['scale']
        self.offset_list = data['offsets']
        self.animations = {}
        self.frame_index = 0
        self.vel_y = 0 # velocity y - how fast player moving up and down
        self.action = 'idle'
        self.image = None # keep track of what frame im in
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 37, 85) # hit box
        self.score_value = score # point worth of this zombie
        self.given_score = False # track if score is counted
        self.health = hp
        self.max_health = hp
        self.health_bar = Health_bar(x, y - 20, 60, 10, self.health, self.max_health)
        self.walking = False
        self.running = False
        self.hurt = False
        self.dead = False
        self.attack_damage = damage
        self.attacking = False
        self.attack_cooldown = 0
        self.vision = pygame.Rect(0, 0, 400, 100) # how far zombie can look

        # movement variables
        self.move_direction = 1  # 1 for right, -1 for left
        self.move_counter = 0
        self.patrol_distance = 100  # how far the zombie will walk before turning around
        self.speed = speed  # movement speed
        self.idling = False
        self.idling_counter = 0

    def load_animation(self, action_name, sprite_sheet_path, frame_count):
        # load a specific animation from its sprite_sheet
        sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        frames = []
        for x in range(frame_count):
            frame = sheet.subsurface(x * self.size, 0, self.size, self.size)
            scaled_frame = pygame.transform.scale(frame, (self.size * self.image_scale, self.size * self.image_scale))
            frames.append(scaled_frame)
        self.animations[action_name] = frames # store complete animation in a list under its action name in a dictionary
    
    def ai(self, screen_width, screen_height, target, screen):
        if not self.dead and not target.dead:
            self.move(screen_width, screen_height, target, screen)


    def move(self, screen_width, screen_height, target, screen):
        SPEED = self.speed
        GRAVITY = 2
        GROUND_LEVEL = screen_height - 40
        dx = 0
        dy = 0
        self.walking = False
        self.running = False
        
        if not self.dead and not self.hurt:
            if self.idling == False and random.randint(1, 200) == 1: # patroling and then stop
                self.idling = True
                self.idling_counter = 60
            
            # check if the zombie is near the player
            if self.vision.colliderect(target.rect):
                # stop and running to the player
                self.running = True
                attack_range = 50  # distance to start attacking
                
                # calculate distance to player
                distance_to_player = target.rect.centerx - self.rect.centerx
                # face the player
                self.move_direction = 1 if distance_to_player > 0 else -1

                # if close enough to attack
                if abs(distance_to_player) < attack_range:
                    self.attack(target)
                else:
                    # chase the player
                    self.running = True
                    dx = self.move_direction * (SPEED + 3)  # faster speed when chasing

            else:
                if self.idling == False: 
                    dx = self.move_direction * SPEED
                    self.walking = True
                    # track how far zombie move in current direction
                    self.move_counter += abs(dx)
                    
                    # update vision as zombie moves
                    self.vision.center = (self.rect.centerx + 200 * self.move_direction, self.rect.centery)
                    pygame.draw.rect(screen, (255, 0, 0), self.vision)

                    # if moved over the patrol distance, turn around
                    if self.move_counter > self.patrol_distance:
                        self.move_direction *= -1  # reverse direction
                        self.move_counter = 0  # reset counter
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        
        # apply gravity
        if self.rect.bottom + dy < GROUND_LEVEL:
            self.rect.y += dy
        else:
            self.rect.bottom = GROUND_LEVEL

        #ensure zombie stays on screen
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

        # update zombie position
        self.rect.x += dx
        self.rect.y += dy

    def update(self, item_box_group, player, score_system):
        # check what action zombie is performing
        if self.health <= 0:
            if not self.dead:
                self.drop_item(item_box_group, player)
            if not self.given_score:
                score_system.add_score(self.score_value)
                self.given_score = True
            self.health = 0
            self.dead = True
            new_action = 'dead'
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
                if self.action == 'attack':
                    self.attacking = False
                    self.attack_cooldown = 30
                if self.action == 'hurt':
                    self.hurt = False

    def is_collidable(self):
        return not self.dead

    def attack(self, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attack_range = 50
            attack_x = self.rect.left - attack_range if self.move_direction < 0 else self.rect.right
            attacking_rect = pygame.Rect(attack_x, self.rect.y, attack_range, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= self.attack_damage 
                target.hurt = True  # Assuming your player class has a hurt state      
            self.attack_cooldown = 30

    def drop_item(self, item_box_group, player):
        # randomly drop item when zombie dies
        if random.random() < 0.8:
            item_type = random.choice(['health', 'ammo'])
            item_box = ItemBox(item_type, self.rect.centerx, self.rect.centery + 10, player)
            item_box_group.add(item_box)
            

    def draw(self, surface):
        pygame.draw.rect(surface, blue, self.rect)
        current_offset = self.offset_list
        self.health_bar.x = self.rect.x
        self.health_bar.y = self.rect.y - 15
        self.health_bar.hp = self.health

        if self.move_direction < 0:  # if moving left (negative direction)
            image_to_draw = pygame.transform.flip(self.image, True, False)  # flip horizontally
        else:  
            image_to_draw = self.image  # use original
        
        if not self.dead:
            self.health_bar.draw(surface)
        
        surface.blit(image_to_draw,
            (
                self.rect.x - (current_offset[0] * self.image_scale),
                self.rect.y - (current_offset[1] * self.image_scale),
            )
        )