import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, flip, bullet_img):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.damage = 50
        self.image = bullet_img
        # Create a red rectangle surface
        self.rect = self.image.get_rect()
        self.direction = -1 if flip else 1  # reverse if player is flipped
        self.image = bullet_img
        self.image = pygame.transform.scale(self.image, (20, 20))
        
        # scale bullet based on direction
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect = self.image.get_rect()
        # adjust spawn position based on direction
        if flip:
            self.rect.right = x  # spawn at left side if facing left
        else:
            self.rect.left = x    # spawn at right side if facing right
        self.rect.centery = y
    
    def update(self, zombies, screen_width):
        self.rect.x += self.speed * self.direction
        
        # check for zombie collisions
        for zombie in zombies:
            if self.rect.colliderect(zombie.rect):
                zombie.health -= self.damage
                zombie.hurt = True  # trigger hurt animation
                self.kill()  # remove bullet when hitting zombie
                break
        
        # remove bullet if off-screen
        if (self.rect.right < 0 or self.rect.left > screen_width):
            self.kill()