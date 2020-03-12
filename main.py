import sys
import pygame
from player import Player
import game_objects

screen_width = 960
screen_height = 640

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Python Programming Project")

win_font = pygame.font.SysFont(None, 72)
win_msg = win_font.render('Fuck Yeah!', True, (0, 128, 0))

game_objects.init(screen)

player = Player(screen)

clock = pygame.time.Clock()

# main loop
run = True
win = False
while run:
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if not(player.jumping):
            player.jumping = True
            player.on_obstacle = False

    if keys[pygame.K_LEFT]:
        player.moving_left = True
        player.moving_right = False

    elif keys[pygame.K_RIGHT]:
        player.moving_left = False
        player.moving_right = True

    else:
        player.moving_left = False
        player.moving_right = False

    player.move()

    if win:
        win = False # reset win

    if player.on_obstacle and player.obstacle == 6:
        win = True

    screen.fill((0,0,0))

    for game_object in game_objects.obstacles:
        game_object.draw()
    player.draw()

    if win:
        screen.blit(win_msg, (screen_width // 2, screen_height // 2))
    pygame.display.update()

pygame.quit()
sys.exit()