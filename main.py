import pygame
from pygame import mixer
from player import Player
from zombie import Zombie
from colors import *

mixer.init()
# load music and sound
pygame.mixer.music.load('music_and_sound/apocalyptic_forest.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 4000)

# walking_grass = pygame.mixer.Sound('music_and_sound/walking_grass.mp3')
# walking_grass.set_volume(0.75)


class health_bar():
    def __init__(self, x, y, width, height, max_hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp= max_hp
        self.max_hp= max_hp

    def draw(self, surface):
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, red, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, green, (self.x, self.y, self.width * ratio, self.height))


WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
forest_bg = pygame.image.load("forest_bg.jpg")
forest_bg = pygame.transform.scale(forest_bg, (800, 600))



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
player.load_animation('hurt', 'player_animation/Hurt.png', 3)
player.load_animation('dead', 'player_animation/Dead.png', 4)

# set initial image
player.image = player.animations['idle'][0] # firsr frame of idle

hp_bar = health_bar(40, 40, 300, 20, 100)

#hide mouse cursor
pygame.mouse.set_visible(False)

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
zombie_man.load_animation('hurt', 'zombie_man_animation/Hurt.png', 3)
zombie_man.load_animation('dead', 'zombie_man_animation/Dead.png', 5)


if __name__ == "__main__":
    pygame.init()
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
        
        #update background
        window.blit(forest_bg, (0,0))
        player.move(WINDOW_WIDTH, WINDOW_HEIGHT, zombie_man)
        zombie_man.ai(WINDOW_WIDTH, WINDOW_HEIGHT, player)
        #update player
        player.update()
        zombie_man.update()
        player.bullet_group.update([zombie_man], WINDOW_WIDTH)  # Update bullets with required parameters # pass zombie for collision checking

        #draw player and zombie
        player.draw(window)
        zombie_man.draw(window)

        # update and draw bullet groups
        player.bullet_group.draw(window)

        #if want to drop hp, assign hp_bar.hp = 50
        hp_bar.draw(window)
        pygame.display.update()
    pygame.quit()

