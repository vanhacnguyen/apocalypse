import pygame


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y, player, scale = 1.25):
        pygame.sprite.Sprite.__init__(self)
        health_box_img = pygame.image.load("assets/health_box.png").convert_alpha()
        ammo_box_img = pygame.image.load("assets/ammo.png").convert_alpha()
        item_boxes = {
            'health': health_box_img,
            'ammo': ammo_box_img
        }

        self.item_type = item_type
        self.player = player
        self.image = item_boxes[item_type]
        # new dimensions
        width = int(self.image.get_width() * scale)
        height = int(self.image.get_height() * scale)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + width // 2, y)
    def update(self):
        # check if the player has picked up the box
        if pygame.sprite.collide_rect(self, self.player):
            # check what kind of box it was
            if self.item_type == 'health':
                self.player.health += 25
                if self.player.health > self.player.max_health: # only keeps max_health as 100
                    self.player.health = self.player.max_health
            elif self.item_type == 'ammo':
                self.player.max_ammo += 15
            
            # delete the item box
            self.kill()