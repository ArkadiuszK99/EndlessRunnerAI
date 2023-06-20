import pygame
import os
import neat
import random

from obstacle import Obstacle
from character import Character
from enemy import Enemy

pygame.font.init()

WIN_WIDTH = 1000
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Endless runner")

bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","test.jpg")).convert_alpha(), (1000, 800))

gen = 0

def draw_window(win, characters, obstacles, score, gen, obstacle_ind):

    if gen == 0:
        gen = 1
    win.blit(bg_img, (0,0))

    for obstacle in obstacles:
        obstacle.draw(win)

    for character in characters:
        character.draw(win)
        for bullet in character.bullets:
            bullet.draw(win)

    # score
    score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    # generations
    score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))
    win.blit(score_label, (10, 10))

    # alive
    score_label = STAT_FONT.render("Alive: " + str(len(characters)),1,(255,255,255))
    win.blit(score_label, (10, 50))

    pygame.display.update()


def eval_genomes(genomes, config):
    global WIN, gen
    win = WIN
    gen += 1
    nets = []
    characters = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        characters.append(Character())
        ge.append(genome)

    obstacles = [Enemy(WIN_WIDTH, 600)]
    score = 0
    bullets = []
    clock = pygame.time.Clock()
    i = 0
    run = True
    while run and len(characters) > 0:
        clock.tick(30)
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        obstacle_ind = 0
        if len(characters) > 0:
            if len(obstacles) > 1 and characters[0].x > obstacles[0].x + obstacles[0].img.get_width():
                obstacle_ind = 1                                                                

        for x, character in enumerate(characters):
            ge[x].fitness += 0.1
            character.move()

            if(character.y == 630):
                distance = (obstacles[obstacle_ind].x - character.x)
                # obstacle on the ground
                obstacle_postion = 0
                # obstacle in the air
                if obstacles[obstacle_ind].height == 500:
                    obstacle_postion = 1
                output = nets[characters.index(character)].activate((distance, obstacle_postion, obstacles[obstacle_ind].isEnemy))
                choice = output.index(max(output))
                if choice == 0:
                    pass
                elif choice == 1:
                    character.jump()
                    ge[x].fitness -= 2
                elif choice == 2:
                    character.crouch()
                    ge[x].fitness -= 2
                elif choice == 3:
                    ge[x].fitness -= 2
                    character.shot()


        rem = []
        add_obstacle = False
        for obstacle in obstacles:
            obstacle.move()
            # check for collision
            for character in characters:
                if len(character.bullets) < 1:
                    if random.uniform(0, 1) < 0.5:
                        bullets.append(character.shot())
                
                for bullet in character.bullets:
                    bullet.move()

                    if obstacle.collide(bullet, win):
                        if obstacle.isEnemy == True:
                            ge[characters.index(character)].fitness += 1
                            character.bullets.pop(character.bullets.index(bullet))
                            if obstacle.removed == False:
                                obstacle.removed == True
                                obstacle.killed = True
                                rem.append(obstacle)

                    
                    if bullet.x > 1000:
                        if bullet in character.bullets:
                            character.bullets.remove(bullet)

                if obstacle.collide(character, win):
                        ge[characters.index(character)].fitness -= 1
                        nets.pop(characters.index(character))
                        ge.pop(characters.index(character))
                        characters.pop(characters.index(character))

            if obstacle.isEnemy:
                if obstacle.killed:
                    score += 1

            if obstacle.x + obstacle.img.get_width() < 0:
                if obstacle.removed == False:
                    obstacle.removed == True
                    rem.append(obstacle)

            if not obstacle.passed and obstacle.x < character.x:
                obstacle.passed = True
                score += 1
                # add_obstacle = True

            if obstacle.x == 500:
                add_obstacle = True

        if add_obstacle:
            #  more reward for passing obstacle
            for genome in ge:
                genome.fitness += 7
            
            if random.uniform(0, 1) < 0.5:
                obstacles.append(Obstacle(WIN_WIDTH, 0))
            else:
                obstacles.append(Enemy(WIN_WIDTH, 0))

        for r in rem:
            if r in obstacles:
                obstacles.remove(r)

        if len(obstacles) == 0:
            if random.uniform(0, 1) < 0.5:
                obstacles.append(Obstacle(WIN_WIDTH, 0))
            else:
                obstacles.append(Enemy(WIN_WIDTH, 0))            

        draw_window(WIN, characters, obstacles, score, gen, obstacle_ind)


def run(config_file):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 100)
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
