import sys
import os
import pygame
import neat
from player import Player
import game_objects

screen_width = 960
screen_height = 640

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Python Programming Project")

# set fonts for the different uses in game
pygame.font.init()
win_font = pygame.font.SysFont(None, 65)
menu_font = pygame.font.SysFont(None, 100)
button_font = pygame.font.SysFont(None, 50)
win_msg = win_font.render('Win!', True, (0, 128, 0))
info_font = pygame.font.SysFont(None, 30)


# set path and load images for menu icons
script_dir = os.path.dirname(__file__)
human_img_path = os.path.join(script_dir, 'user.png')
ai_img_path = os.path.join(script_dir, 'bot.png')
human_img = pygame.image.load(human_img_path)
ai_img = pygame.image.load(ai_img_path)

# set some simple colors for use later on with buttons and whatnot
red = (200, 0, 25)
lightred = (255, 0, 50)
green = (0, 128, 0)
lightgreen = (0, 175, 0)
blue = (0, 0, 125)
lightblue = (0,0,200)
white = (255, 255, 255)


# code block to build a scoreboard
player_score = 0
ai_score = 0
score_font = pygame.font.SysFont(None, 30)
# list to hold multiple lines for the scoreboard
scoreboard = []



def run_human_player():

    game_objects.init(screen)

    player = Player(screen)

    '''     THIS WILL BE THE SCOREBOARD SECTION BUT I HAVEN'T DECIDED WHAT THAT'LL LOOK LIKE YET
    player_score = 0
    ai_score = 0



    score_out = '|   ' + str(player_score) + '                      ' + str(ai_score) + '   |'
    scoreblock = ['          SCORE',
                  '-----------------------------',
                  '|Human    Computer|',
                  score_out,
                  '-----------------------------']

    for line in scoreblock:
        scoreboard.append(score_font.render(str(line), True, (32, 100, 128)))
    for line in range(5):
        screen.blit(scoreboard[line], (0, 10 + (line * 15)))

    pygame.display.update()

    '''
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

        make_button("Menu", button_font, green, red, lightred, screen_width - 100, 0, 100, 50, "menu")


        for game_object in game_objects.obstacles:
            game_object.draw()

        player.draw()

        if win:
            screen.blit(win_msg, (screen_width // 2, screen_height // 2))
            player_score += 1
        else:
            pygame.display.update()

    pygame.quit()
    sys.exit()


'''Run A.I. simulation of the game'''
def eval_genomes(genomes, config):

    # lists to hold the players, the genomes, and the neural net associated with that genome
    neural_nets = []
    genome = []
    players = []

    # initialize neural nets and genomes
    for _, g in genomes:
        g.fitness = 0
        nn = neat.nn.FeedForwardNetwork.create(g, config)
        neural_nets.append(nn)
        players.append(Player(screen))
        genome.append(g)

    # initialize the game
    game_objects.init(screen)

    clock = pygame.time.Clock()

    run_simulation = True
    while run_simulation and len(players) > 0:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_simulation = False
                pygame.quit()
                sys.exit()

        obstacles = game_objects.obstacles
        winning_path = [0, 1, 2, 3, 4]
        goal = 4
        cur_goal = 0
        for i, p in enumerate(players):
            x, y, obst = p.get_position()
            if obst != goal:
                cur_goal = obst + 1
            else: # stay where we are for right now (on top of the goal block)
                cur_goal = goal
            from_goal = obstacles[cur_goal].x - x
            output = neural_nets[players.index(p)].activate((x, from_goal))

            if output[1] < 0.5:
                if not p.jumping:
                    p.jumping = True
                    p.on_obstacle = False

            if output[0] > 0:
                p.moving_left = False
                p.moving_right = True
            else:
                p.moving_left = True
                p.moving_right = False


            prev_obst = obst
            prev_x = x

            p.move()

            x, y, obst = p.get_position()

            # find if we backtracked from our cur_goal
            if obst < prev_obst:
                genome[i].fitness -= 1

            # see if we are any closer to our goal
            if obst > prev_obst:
                genome[i].fitness += 1

            if obst != goal:
                new_from_goal = abs(obstacles[(obst + 1)].x - x)
            else:
                new_from_goal = goal

            if new_from_goal < abs(from_goal):
                genome[i].fitness += 0.1
            else:
                genome[i].fitness -= 0.1

            # standing or jumping in place?
            if prev_x == x and obst != goal:
                genome[i].fitness -= 5

            # did we achieve the goal?
            if obst == goal:
                genome[i].fitness += 5
                ai_score += 1
            else:
                # decrease exist counter for this player
                p.life_counter -= 1

            if p.life_counter < 0:
                # remove this player and neural net
                genome[players.index(p)].fitness -= 5
                neural_nets.pop(players.index(p))
                genome.pop(players.index(p))
                players.pop(players.index(p))


        screen.fill((0, 0, 0))

        for game_object in game_objects.obstacles:
            game_object.draw()

        for p in players:
            p.draw()

        pygame.display.update()


def run(config_file):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # creates the population to run the top-level simulation
    p = neat.Population(config)

    # output statistics to console
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # run the simulation
    num_generations = 100

    # eventually change this to be called in main -- the menu will launch the rest
    game_menu()
    results = p.run(eval_genomes, num_generations)

    # show stats
    print(results)


def game_info():

    info = True

    while info:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((0,0,0))

        text_surf, text_rect = text_objects('Man vs Machine', menu_font, lightblue)
        text_rect.center = (int(screen_width / 2), 50)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('Man vs Machine is a small-scale platforming game', info_font, white)
        text_rect.center = (int(screen_width / 3), 125)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('It has been developed to implement and test basic AI', info_font, white)
        text_rect.center = (int(screen_width / 3) + 10, 150)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('How it works:', win_font, lightred)
        text_rect.center = (int(screen_width / 4.7) + 10, 210)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('The AI get a headstart of sorts and run through the program a few preliminary times', info_font, white)
        text_rect.center = (int(screen_width / 2.05) + 10, 250)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('Users then choose a level of difficulty: easy, medium, or hard', info_font, white)
        text_rect.center = (int(screen_width / 2.45) + 10, 275)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('The difficulty level corresponds to a set number of AIs the player will be up against', info_font, white)
        text_rect.center = (int(screen_width / 1.925) + 10, 300)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('Essentially, the more AI trying to win, the tougher it will be for you', info_font, white)
        text_rect.center = (int(screen_width / 2.49) + 10, 325)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('If you reach the finish before the AI, you win!', info_font, white)
        text_rect.center = (int(screen_width / 3.43) + 10, 350)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('If any of the AI beat you there, you lose!', info_font, white)
        text_rect.center = (int(screen_width / 3.77) + 10, 375)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('As soon as you finish a level, you\'ll continue on to a new, randomly generated one', info_font, white)
        text_rect.center = (int(screen_width / 2.099) + 10, 400)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('Good luck!', win_font, lightred)
        text_rect.center = (int(screen_width / 2) + 10, 500)
        screen.blit(text_surf, text_rect)


        make_button('Back', score_font, lightblue, green, lightgreen, screen_width - 200, screen_height - 100, 100, 50, "menu")

        pygame.display.update()


def game_menu():

    intro = True

    screen.fill((0, 0, 0))

    screen.blit(human_img, (screen_width/3, screen_height/5))
    text_surf, text_rect = text_objects('VS', button_font, white)
    text_rect.center = (int(screen_width / 2), int(screen_height / 3.5))
    screen.blit(text_surf, text_rect)
    screen.blit(ai_img, (screen_width*2/3 -80, screen_height/5))

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        text_surf, text_rect = text_objects('Welcome to Man vs Machine', menu_font, lightblue)
        text_rect.center = (int(screen_width / 2), int(screen_height / 2))
        screen.blit(text_surf, text_rect)

        make_button('Start', button_font, green, red, lightred, 150, screen_height - 200, 200, 100, "sett")
        make_button('Quit', button_font, green, red, lightred, screen_width - 100, screen_height-50, 100, 50, "quit")
        make_button('Info', button_font, green, red, lightred, screen_width - 200 - 150, screen_height - 200, 200, 100, "info")

        pygame.display.update()


def game_settings():

    sett = True

    while sett:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((0,0,0))

        text_surf, text_rect = text_objects('Man vs Machine', menu_font, lightblue)
        text_rect.center = (int(screen_width / 2), 50)
        screen.blit(text_surf, text_rect)

        text_surf, text_rect = text_objects('Difficulty', win_font, lightred)
        text_rect.center = (int(screen_width / 2) + 10, 125)
        screen.blit(text_surf, text_rect)

        make_button('Easy', button_font, white, green, lightgreen, screen_width/4 - 100, screen_height/2, 200, 100, "easy")
        make_button('Medium', button_font, white, blue, lightblue, screen_width/2 - 100, screen_height/2, 200, 100, "med")
        make_button('Hard', button_font, white, red, lightred, screen_width*3/4 - 100, screen_height/2, 200, 100, "hard")

        pygame.display.update()


def make_button (text, font, textcolor, color_off, color_on, x_pos, y_pos, width, height, action = None):
    mouse = pygame.mouse.get_pos()

    click = pygame.mouse.get_pressed()

    if x_pos + width > mouse[0] > x_pos and y_pos + height > mouse[1] > y_pos:
        pygame.draw.rect(screen, color_on, (x_pos, y_pos, width, height))
        if click[0] == 1 and action != None:
            if action == 'sett':
                #start game action
                game_settings()
            elif action == 'quit':
                pygame.quit()
                quit()
            elif action == 'menu':
                game_menu()
            elif action == 'info':
                game_info()
            elif action == 'easy':
                run_human_player()
            elif action == 'med':
                run_human_player()
            elif action == 'hard':
                run_human_player()
    else:
        pygame.draw.rect(screen, color_off, (x_pos, y_pos, width, height))

    text_surf, text_rect = text_objects(text, font, textcolor)
    text_rect.center = ( (x_pos + int(width/2), y_pos + int(height/2)) )

    screen.blit(text_surf, text_rect)


def text_objects(text, font, color):

    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


if __name__ == "__main__":

    # run_human_player()

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-neat.txt')
    run(config_path)
