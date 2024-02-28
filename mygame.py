import pygame
import sys

pygame.init()
clock = pygame.time.Clock()
WIDTH = 400
HEIGHT = 400
window = pygame.display.set_mode((WIDTH,HEIGHT))


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        # give access to methods and properties of a parent class
        pacman_image = pygame.image.load(image)
        self.image = pygame.transform.scale(pacman_image,(20,20))
        self.rect = pygame.Rect(x,y,20,20)
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.speed = 4

    def process_input(self, event: pygame.event.Event):
        # To resolve the issue where holding down. moves down. down-up tap left causes jutter to left and stop
        # use booleans to record current movement
        """Booleans remember direction we are moving"""
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.move_left = False
            elif event.key == pygame.K_w:
                self.move_up = False
            elif event.key == pygame.K_s:
                self.move_down = False
            elif event.key == pygame.K_d:
                self.move_right = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.move_left = True
            elif event.key == pygame.K_w:
                self.move_up = True
            elif event.key == pygame.K_d:
                self.move_right = True
            elif event.key == pygame.K_s:
                self.move_down = True

    def update(self, obstacles):
        """The if-elif statements ensure movement in only one direction occurs"""
        old_rect = self.rect.copy()
        w, h = pygame.display.get_surface().get_size()
        if self.move_left and self.rect.centerx > 20:
            self.rect.centerx -= self.speed
        elif self.move_right and self.rect.centerx < (w - 20):
            self.rect.centerx += self.speed
        elif self.move_up and self.rect.centery > 20:
            self.rect.centery -= self.speed
        elif self.move_down and self.rect.centery < (h - 20):
            self.rect.centery += self.speed

        #Return a list containing all Sprites in a Group that intersect with another Sprite
        collisions = pygame.sprite.spritecollide(self,obstacles,False)
        if collisions:
            self.rect = old_rect

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, dim):
        super().__init__()
        # Create an image of the block, and fill it with a color.
        self.image = pygame.Surface(dim)
        self.image.fill((255,255,255))
        #Returns a new rectangle covering the entire surface
        self.rect = pygame.Rect(x,y,20,20)


all_sprites_list = pygame.sprite.Group()
obstacles_list = pygame.sprite.Group()
#A container class to hold and manage multiple Sprite objects.
player = PlayerSprite("pacman.png",200,200)
obstacle = Obstacle(250,150,[20,20])
all_sprites_list.add(player)
obstacles_list.add(obstacle)

BLACK = (0,0,0)
running = True
while running:
    window.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        player.process_input(event)
    all_sprites_list.update(obstacles_list)
    obstacles_list.update()
    #Calls the update() method of all sprites in the group.
    all_sprites_list.draw(window)
    obstacles_list.draw(window)
    pygame.display.update()
    clock.tick(60)
    # It will compute how many milliseconds have passed since the previous call
