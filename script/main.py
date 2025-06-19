import pygame
from pygame import mixer
from player import Player
from zombie import Zombie
from item_box import ItemBox
from score_system import ScoreSystem
from enemy_spawner import EnemySpawner
from colors import *

pygame.init()
mixer.init()

# load music and sound
pygame.mixer.music.load('music_and_sound/apocalyptic_forest.mp3')
game_over_sound = pygame.mixer.Sound('music_and_sound/game_over_sound.mp3')
victory_sound = pygame.mixer.Sound('music_and_sound/victory_sound.mp3')
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1, 0.0, 4000)


WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
forest_bg = pygame.image.load("assets/forest_bg.jpg").convert_alpha()
forest_bg = pygame.transform.scale(forest_bg, (800, 600))
win_bg = pygame.image.load("assets/winning.jpg").convert_alpha()
win_bg = pygame.transform.scale(win_bg, (800, 600))
game_over_img = pygame.image.load("assets/game_over_logo.png").convert_alpha()
game_over_img = pygame.transform.scale(game_over_img, (350, 250))
restart_img = pygame.image.load('assets/restart_btn.png').convert_alpha()
player_score = 0

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
start_button = Button(275, 440, restart_img, 0.4)

pygame.font.init()
#define font
font = pygame.font.Font('assets/Minecraft.ttf', 25)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    score = font.render(text, True, text_color)
    window.blit(img, (x, y))
    window.blit(score, (x, y))

def reset_game():
    global player, all_zombies, item_box_group, score_system, enemy_spawner
    
    player.reset(10, 470, PLAYER_DATA)
    all_zombies.clear()
    item_box_group.empty()
    score_system.score = 0
    enemy_spawner.last_spawn_time = pygame.time.get_ticks()
    
    zombie_man = Zombie(500, 475, ZOMBIE_MAN_DATA, **ZOMBIE_TYPES['normal'])
    zombie_man.load_animation('idle', 'zombie_man_animation/Idle.png', 8)
    zombie_man.load_animation('walk', 'zombie_man_animation/Walk.png', 8)
    zombie_man.load_animation('run', 'zombie_man_animation/Run.png', 7)
    zombie_man.load_animation('attack', 'zombie_man_animation/Attack_2.png', 4)
    zombie_man.load_animation('hurt', 'zombie_man_animation/Hurt.png', 3)
    zombie_man.load_animation('dead', 'zombie_man_animation/Dead.png', 5)
    
    wild_zombie = Zombie(100, 475, ZOMBIE_MAN_DATA, **ZOMBIE_TYPES['wild'])
    wild_zombie.load_animation('idle', 'wild_zombie_animation/Idle.png', 9)
    wild_zombie.load_animation('walk', 'wild_zombie_animation/Walk.png', 10)
    wild_zombie.load_animation('run', 'wild_zombie_animation/Run.png', 8)
    wild_zombie.load_animation('attack', 'wild_zombie_animation/Attack_2.png', 4)
    wild_zombie.load_animation('hurt', 'wild_zombie_animation/Hurt.png', 5)
    wild_zombie.load_animation('dead', 'wild_zombie_animation/Dead.png', 5)
    
    all_zombies.extend([zombie_man, wild_zombie])

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

# create sprite group
item_box_group = pygame.sprite.Group()

#temporary - create item boxes
item_box = ItemBox('health', -100, -100, player)
item_box_group.add(item_box)
item_box = ItemBox('ammo', -100, -100, player)
item_box_group.add(item_box)  

#load spritesheets
ZOMBIE_MAN_DATA = { 
    'frame_size': 96,
    'scale': 1.35,
    'offsets': [35, 32]
}

ZOMBIE_TYPES = {
    'normal': {
        'hp': 100,
        'damage': 5,
        'speed': 1,
        'score': 1
    },
    'wild': {
        'hp': 110,
        'damage': 10,
        'speed': 1.5,
        'score': 2
    }
}
enemy_spawner = EnemySpawner(ZOMBIE_TYPES)

zombie_man = Zombie(500, 475, ZOMBIE_MAN_DATA, **ZOMBIE_TYPES['normal']) # unpacking dictionary
zombie_man.load_animation('idle', 'zombie_man_animation/Idle.png', 8)
zombie_man.load_animation('walk', 'zombie_man_animation/Walk.png', 8)
zombie_man.load_animation('run', 'zombie_man_animation/Run.png', 7)
zombie_man.load_animation('attack', 'zombie_man_animation/Attack_2.png', 4)
zombie_man.load_animation('hurt', 'zombie_man_animation/Hurt.png', 3)
zombie_man.load_animation('dead', 'zombie_man_animation/Dead.png', 5)

wild_zombie = Zombie(100, 475, ZOMBIE_MAN_DATA, **ZOMBIE_TYPES['wild'])
wild_zombie.load_animation('idle', 'wild_zombie_animation/Idle.png', 9)
wild_zombie.load_animation('walk', 'wild_zombie_animation/Walk.png', 10)
wild_zombie.load_animation('run', 'wild_zombie_animation/Run.png', 8)
wild_zombie.load_animation('attack', 'wild_zombie_animation/Attack_2.png', 4)
wild_zombie.load_animation('hurt', 'wild_zombie_animation/Hurt.png', 5)
wild_zombie.load_animation('dead', 'wild_zombie_animation/Dead.png', 5)

all_zombies = [zombie_man, wild_zombie] # hold active zombies

if __name__ == "__main__":
    pygame.display.set_caption("Apocalypse")

    # set frame rates
    clock = pygame.time.Clock()
    frames_per_sec = 60
    score_system = ScoreSystem()
    running = True
    game_state = 'playing'
    game_over_sound_played = False
    victory_sound_played = False

    while running:
        current_time = pygame.time.get_ticks()
        clock.tick(frames_per_sec)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        
        # update background
        window.blit(forest_bg, (0,0))
        # show ammo, score, and highest score
        draw_text(f'AMMO: {player.ammo}/{player.max_ammo}', font, white, 40, 75)
        draw_text(f'SCORE: {score_system.score}', font, white, 40, 110)
        draw_text(f'HIGHEST SCORE: {score_system.high_score}', font, white, 40, 140)

        player.move(WINDOW_WIDTH, WINDOW_HEIGHT, all_zombies, window)
        
        #update everything
        enemy_spawner.update(current_time, all_zombies, item_box_group, player, score_system, WINDOW_WIDTH, WINDOW_HEIGHT)
        for zombie in all_zombies[:]:  # use slice copy to allow removal during iteration
            zombie.update(item_box_group, player, score_system)
            zombie.ai(WINDOW_WIDTH, WINDOW_HEIGHT, player, window)
            
            # remove zombies that finished their death animation
            if zombie.dead and zombie.action == 'dead' and zombie.frame_index >= len(zombie.animations['dead']) - 1:
                all_zombies.remove(zombie)
            else:
                zombie.draw(window)
        
        player.update()
        player.bullet_group.update(all_zombies, WINDOW_WIDTH)  # Update bullets and pass zombies for collision checking
        item_box_group.update()

        #draw player and itembox
        player.draw(window)
        item_box_group.draw(window)

        # draw bullet groups
        player.bullet_group.draw(window)


        # result
        if game_state == 'playing' and score_system.score == 30:
            game_state = 'won'
        elif game_state == 'playing' and player.dead:
            game_state = 'lose'

        if game_state == 'won':
            pygame.mixer.music.stop()
            window.blit(win_bg, (0,0))
            if not victory_sound_played:
                victory_sound.play()
                victory_sound_played = True
            if start_button.draw():
                reset_game()
                game_state = 'playing'
                victory_sound_played = False
        
        if game_state == 'lose':
            # display game over
            window.fill(black)
            window.blit(game_over_img, (225, 200))
            pygame.mixer.music.stop()
            if not game_over_sound_played:
                game_over_sound.play()
                game_over_sound_played = True
            if start_button.draw():
                reset_game()
                game_state = 'playing'
                game_over_sound_played = False  # reset flag for next game over sound

        pygame.display.update()
    pygame.quit()

