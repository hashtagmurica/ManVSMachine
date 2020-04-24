import pygame
from pygame import *
import game_elements
from game_elements import *


if __name__ == "__main__":
    # Initialize window
    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)
    pygame.display.set_caption("MAN VS. MACHINE")
    clock = pygame.time.Clock()

    # Set background
    background = pygame.image.load("background.png").convert()
    screen.blit(background, [0,0])

    # Set game objects
    objects = pygame.sprite.Group()
    tiles = []
    camera = Camera(SCREEN)

    # Build world: map tile objects to level plan
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P",
        "P                                          P",
        "P                          E               P",
        "P                    PPPPPPPPPPP           P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P    PPPPPPPP                              P",
        "P                                          P",
        "P                          PPPPPPP         P",
        "P                 PPPPPP                   P",
        "P                                          P",
        "P         PPPPPPP                          P",
        "P                                          P",
        "P                     PPPPPP               P",
        "P                                          P",
        "P   PPPPPPPPPPP                            P",
        "P                                          P",
        "P                 PPPPPPPPPPP              P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
        
    x = y = 0
    for row in level:
        for col in row:
            if col == "P":
                t = Tile((x, y))
                tiles.append(t)
                objects.add(t)
            x += 20
        y += 20
        x = 0

    player = Player(None, tiles, (50, 50))
    objects.add(player)

    # GAME LOOP
    while 1:
        clock.tick(50)

        left = right = space = False
        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                space = True

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_SPACE:
                space = False
        
        screen.blit(background, [0,0])
        camera.update(player)

        player.move(left, right, space, tiles)

        for obj in objects:
            screen.blit(obj.image, camera.apply(obj))

        pygame.display.update()