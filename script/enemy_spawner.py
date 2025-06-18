import pygame
import random
from zombie import Zombie

class EnemySpawner:
    def __init__(self, zombie_types):
        self.zombie_types = zombie_types
        self.spawn_timer = 0
        self.spawn_interval = 4000  # 5 seconds in milliseconds
        self.last_spawn_time = pygame.time.get_ticks()
    
    def update(self, current_time, all_zombies, item_box_group, player, score_system, window_width, window_height):
        # check if it's time to spawn new enemies
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.spawn_enemy(all_zombies, item_box_group, player, score_system, window_width, window_height)
            self.last_spawn_time = current_time
    
    def spawn_enemy(self, all_zombies, item_box_group, player, score_system, window_width, window_height):
        # randomly choose which side to spawn from (0 = left, 1 = right)
        spawn_side = random.randint(0, 1)
        
        # choose random zombie type
        zombie_type_name = random.choice(list(self.zombie_types.keys()))
        zombie_type = self.zombie_types[zombie_type_name]

        # set spawn position based on side
        if spawn_side == 0:  # left
            x = -50  # start at off-screen left
        else:  
            x = window_width + 50  # start at off-screen right

        zombie_data = { 
            'frame_size': 96,
            'scale': 1.35,
            'offsets': [35, 32]
        }
        # create zombie
        new_zombie = Zombie(x, window_height - 125, zombie_data, **zombie_type)

        # load animation
        if zombie_type_name == 'normal':
            new_zombie.load_animation('idle', 'zombie_man_animation/Idle.png', 8)
            new_zombie.load_animation('walk', 'zombie_man_animation/Walk.png', 8)
            new_zombie.load_animation('run', 'zombie_man_animation/Run.png', 7)
            new_zombie.load_animation('attack', 'zombie_man_animation/Attack_2.png', 4)
            new_zombie.load_animation('hurt', 'zombie_man_animation/Hurt.png', 3)
            new_zombie.load_animation('dead', 'zombie_man_animation/Dead.png', 5)
        else:
            new_zombie.load_animation('idle', 'wild_zombie_animation/Idle.png', 9)
            new_zombie.load_animation('walk', 'wild_zombie_animation/Walk.png', 10)
            new_zombie.load_animation('run', 'wild_zombie_animation/Run.png', 8)
            new_zombie.load_animation('attack', 'wild_zombie_animation/Attack_2.png', 4)
            new_zombie.load_animation('hurt', 'wild_zombie_animation/Hurt.png', 5)
            new_zombie.load_animation('dead', 'wild_zombie_animation/Dead.png', 5)
        
        all_zombies.append(new_zombie)