import pygame
from pygame import *

SCREEN = pygame.Rect((0, 0, 960, 640))
LEVEL = pygame.Rect((0, 0, 1600, 1600))

class Camera(object):
    def __init__(self, level_size):
        self.state = level_size

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        l = target.rect.left
        t = target.rect.top
        self.state = pygame.Rect((SCREEN.centerx-l, SCREEN.centery-t, self.state.width, self.state.height))

class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_file, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.blit(pygame.image.load(image_file).convert(), [0,0])
        self.rect = pygame.Rect((pos), (20, 20))

    def update(self):
        pass

class Tile(GameObject):
    def __init__(self, pos):
        super().__init__("tile.png", pos)

class Goal(GameObject):
    def __init__(self, pos):
        super().__init__("goal.png", pos) # GET GOAL IMAGE

class Player(pygame.sprite.Sprite):
    def __init__(self, image_file, tiles, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 255, 255))
        #self.image.blit(pygame.image.load(image_file).convert(), [0,0])
        self.rect = self.image.get_rect(topleft=pos)
        #self.tiles = tiles
        self.speed = 0
        self.vert = 0
        self.moving_left = False
        self.moving_right = False
        self.jumping = False
        self.grounded = False
        self.life_counter = 700

    def move(self, left, right, space, tiles):
        # Process key input results:
        # Moving left or right
        if left:
            self.speed = -5
            print("left")
        elif right:
            self.speed = 5
            print("right")
        # Jumping
        if space:
            if self.grounded:
                self.vert -= 8
                print("jump")
        # Falling
        if not self.grounded:
            self.vert += 1
        if not left and not right:
            self.speed = 0

        # Update position
        self.rect.left += self.speed
        self.collision(self.speed, 0, tiles)

        self.rect.top += self.vert
        self.grounded = False
        self.collision(0, self.vert, tiles)


    def collision(self, speed, vert, tiles):
        for tile in tiles:
            if pygame.sprite.collide_rect(self, tile):
                # Reached goal object
                if isinstance(tile, Goal):
                    print("Reached Goal")
                # Left and right collisions
                if speed < 0:
                    self.rect.left = tile.rect.right
                if speed > 0:
                    self.rect.right = tile.rect.left
                # Top and bottom collisions
                if vert < 0:
                    self.rect.top = tile.rect.bottom
                if vert > 0:
                    self.rect.bottom = tile.rect.top
                    self.vert = 0
                    self.grounded = True

'''
class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_file, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((20, 20))
        self.image.blit(pygame.image.load(image_file).convert(), [0,0])
        self.rect = pygame.Rect((pos), (20, 20))

class Tile(GameObject):
    def __init__(self, pos, *groups):
        super().__init__("tile.png", pos, *groups)

class Goal(GameObject):
    def __init__(self, pos, *groups):
        super().__init__("goal.png", pos, *groups) # GET GOAL IMAGE

class Player(pygame.sprite.Sprite):
    def __init__(self, image_file, tiles, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 255, 255))
        #self.image.blit(pygame.image.load(image_file).convert(), [0,0])
        self.rect = self.image.get_rect(topleft=pos)
        #elf.tiles = tiles
        self.speed = 0
        self.vert = 0
        self.moving_left = False
        self.moving_right = False
        self.jumping = False
        self.grounded = False
        self.life_counter = 700

    def move(self, left, right, space, tiles):
        # Process key input results:
        # Moving left or right
        if left:
            self.speed = -5
        elif right:
            self.speed = 5
        # Jumping
        if space:
            if self.grounded:
                self.vert -= 8
        # Falling
        if not self.grounded:
            self.vert += 1
        if not left and not right:
            self.speed = 0

        # Update position
        self.rect.left += self.speed
        self.rect.top += self.vert
        self.grounded = False
        
        self.collision(tiles)


    def collision(self, tiles):
        for tile in tiles:
            if pygame.sprite.collide_rect(self, tile):
                # Reached goal object
                if isinstance(tile, Goal):
                    print("Reached Goal")
                # Left and right collisions
                if self.speed < 0:
                    self.rect.left = tile.rect.right
                if self.speed > 0:
                    self.rect.right = tile.rect.left
                # Top and bottom collisions
                if self.vert < 0:
                    self.rect.top = tile.rect.bottom
                if self.vert > 0:
                    self.rect.bottom = tile.rect.top
                    self.vert = 0
                    self.grounded = True
                '''

        
