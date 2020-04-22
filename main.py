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

pygame.font.init()
win_font = pygame.font.SysFont(None, 72)
win_msg = win_font.render('Win!', True, (0, 128, 0))

def run_human_player():

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
    results = p.run(eval_genomes, num_generations)

    # show stats
    print(results)

if __name__ == "__main__":

    # run_human_player()

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-neat.txt')
    run(config_path)
