import pygame
from pygame import mixer
from player import Player
from zombie import Zombie
from colors import *

pygame.init()
mixer.init()
# load music and sound
pygame.mixer.music.load('music_and_sound/apocalyptic_forest.mp3')
pygame.mixer.music.set_volume(0.25)
# pygame.mixer.music.play(-1, 0.0, 4000)


WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
forest_bg = pygame.image.load("forest_bg.jpg").convert_alpha()
forest_bg = pygame.transform.scale(forest_bg, (800, 600))
game_over_img = pygame.image.load("game_over.png").convert_alpha()
game_over_img = pygame.transform.scale(game_over_img, (300, 200))

start_img = pygame.image.load('start_btn.png').convert_alpha()

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self):
        action = False
        # get mouse position
        position = pygame.mouse.get_pos()
        
        # check mouseover and clicked conditions
        if self.rect.collidepoint(position): # if mouse cursor touch the button
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0: # if not click
            self.clicked = False

        # draw button on screen
        window.blit(self.image, (self.rect.x, self.rect.y))
        return action

# create button instance
start_button = Button(325, 325, start_img, 0.5)

pygame.font.init()
#define font
font = pygame.font.Font('Minecraft.ttf', 25)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    window.blit(img, (x, y))

# load collectible items image
health_box_img = pygame.image.load("health_box.png").convert_alpha()
ammo_box_img = pygame.image.load("ammo.png").convert_alpha()
item_boxes = {
    'health': health_box_img,
    'ammo': ammo_box_img
}

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y, scale = 1.25):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[item_type]
        # new dimensions
        width = int(self.image.get_width() * scale)
        height = int(self.image.get_height() * scale)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + width // 2, y)
    def update(self):
        # check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            # check what kind of box it was
            if self.item_type == 'health':
                player.health += 25
                if player.health > player.max_health: # only keeps max_health as 100
                    player.health = player.max_health
            elif self.item_type == 'ammo':
                player.max_ammo += 15
            
            # delete the item box
            self.kill()

# create sprite group
item_box_group = pygame.sprite.Group()

#temporary - create item boxes
item_box = ItemBox('health', 100, 525)
item_box_group.add(item_box)
item_box = ItemBox('ammo', 400, 525)
item_box_group.add(item_box)

# define player variables
PLAYER_DATA = {
    'frame_size': 128,
    'scale': 1.35,
    'offsets': [45, 65]
}
player = Player(10, 470, PLAYER_DATA)
player.load_animation('idle', 'player_animation/Idle.png', 7)
player.load_animation('walk', 'player_animation/Walk.png', 7)
player.load_animation('run', 'player_animation/Run.png', 8)
player.load_animation('attack', 'player_animation/Attack.png', 3)
player.load_animation('shoot', 'player_animation/Shot_2.png', 4)
player.load_animation('recharge', 'player_animation/Recharge.png', 13)
player.load_animation('hurt', 'player_animation/Hurt.png', 3)
player.load_animation('dead', 'player_animation/Dead.png', 4)

# set initial image
player.image = player.animations['idle'][0] # first frame of idle

#load spritesheets
ZOMBIE_MAN_DATA = { 
    'frame_size': 96,
    'scale': 1.35,
    'offsets': [35, 32]
}

zombie_man = Zombie(500, 475, ZOMBIE_MAN_DATA)
zombie_man.load_animation('idle', 'zombie_man_animation/Idle.png', 8)
zombie_man.load_animation('walk', 'zombie_man_animation/Walk.png', 8)
zombie_man.load_animation('run', 'zombie_man_animation/Run.png', 7)
zombie_man.load_animation('attack', 'zombie_man_animation/Attack_2.png', 4)
zombie_man.load_animation('hurt', 'zombie_man_animation/Hurt.png', 3)
zombie_man.load_animation('dead', 'zombie_man_animation/Dead.png', 5)



if __name__ == "__main__":
    pygame.display.set_caption("Apocalypse")

    # set frame rates
    clock = pygame.time.Clock()
    frames_per_sec = 60

    running = True
    while running:
        clock.tick(frames_per_sec)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        
        # update background
        window.blit(forest_bg, (0,0))
        # show ammo
        draw_text(f'AMMO: {player.ammo}/{player.max_ammo}', font, white, 40, 75)
        player.move(WINDOW_WIDTH, WINDOW_HEIGHT, zombie_man)
        zombie_man.ai(WINDOW_WIDTH, WINDOW_HEIGHT, player, window)
        
        #update everything
        player.update()
        zombie_man.update()
        player.bullet_group.update([zombie_man], WINDOW_WIDTH)  # Update bullets with required parameters # pass zombie for collision checking
        item_box_group.update()

        #draw player and zombie
        player.draw(window)
        zombie_man.draw(window)
        item_box_group.draw(window)

        # draw bullet groups
        player.bullet_group.draw(window)
        if player.dead:
            # display game over
            window.blit(game_over_img, (250, 150))
            start_button.draw()
            
        pygame.display.update()
    pygame.quit()

