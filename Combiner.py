import pygame as pg
import pymunk.pygame_util
import random
import math
import pymunk.constraints
import pickle
import Robot_maker2
import liquid2

pymunk.pygame_util.positive_y_is_up = False
pg.init()
RES = WIDTH, HEIGHT = 700, 700
FPS = 60
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)
space = pymunk.Space()
space.gravity = 0, 20
node_radius = 7
base_density, base_elasticity, base_friction = 1, 0.4, 0.9
muscle_density, muscle_elasticity, muscle_friction = 1, 0.5, 0.5
liquid_mass, liquid_radius = 10, 6

class Robot_combine():
    def __init__(self,a,b,position,split,mut):
        positionsa,positionsb,typesa,typesb,n_sample,types = [],[],[],[],[],[]
        if a.gen >= b.gen:
            gen = a.gen + 1
        elif b.gen > a.gen:
            gen = b.gen + 1
        if len(a.nodes) >  len(b.nodes):
            length = len(a.nodes)
        elif len(b.nodes) >= len(a.nodes):
            length = len(b.nodes)
        num = split
        rest = length - num
        anodes = random.sample(a.nodes, k=num)
        bnodes = random.sample(b.nodes, k=rest)
        for i in anodes:
            t = i.type
            an1 = i.body.position[0] - a.i_pos[0]
            an2 = i.body.position[1] - a.i_pos[1]
            norm_pos = (an1+position[0],an2+position[1])
            in_sample = False
            for j in a.sample:
                if i == j:
                    in_sample = True
            positionsa.append([norm_pos, t, in_sample])
            #typesa.append(t)
            #for j in a.sample:
            #    if i == j:
            #        n_sample.append(i)
        for i in bnodes:
            t = i.type
            bn1 = i.body.position[0] - b.i_pos[0]
            bn2 = i.body.position[1] - b.i_pos[1]
            norm_pos = (bn1 + position[0],bn2+ position[1])
            in_sample = False
            for j in b.sample:
                if i == j:
                    in_sample = True
            positionsb.append([norm_pos, t, in_sample])
            #typesb.append(t)
            #for j in b.sample:
            #    if i == j:
            #        n_sample.append(i)
        pos = positionsb + positionsa
        #types = typesa + typesb
        #pos = list(dict.fromkeys(pos))
        mutation_chance = random.randint(0,mut)
        if mutation_chance == 0:
            pos.pop(random.randrange(len(pos)))
            pos.append([(random.randrange(position[0]-100, position[0]+100),random.randrange(position[1]-100, position[1]+100)),random.randint(0,1),bool(random.getrandbits(1))])
            print("mutated")
        if len(pos) < length:
            pos.append([(random.randrange(position[0]-100, position[0]+100),random.randrange(position[1]-100, position[1]+100)),random.randint(0,1),bool(random.getrandbits(1))])
            print("special mutate")
        self.Child = Robot_maker2.Robot(length,position,space,gen,pos)

robot1 = Robot_maker2.Robot(5,(110,110),space,1,[])
robot2 = Robot_maker2.Robot(5,(590,110),space,1,[])
robot3 = Robot_combine(robot1,robot2,(110,390),4,10)
robot4 = Robot_combine(robot1,robot2,(590,390),4,10)
robot5 = Robot_combine(robot3.Child,robot4.Child,(300,490),4,5)
robot1.Add_to_space(space)
robot2.Add_to_space(space)
robot3.Child.Add_to_space(space)
robot4.Child.Add_to_space(space)
robot5.Child.Add_to_space(space)



def game():
    # This is the place to call more robots or test specific orientations you can change the number of nodes as well as initial position below:
    Robot_maker2.Boundaries(space, WIDTH, HEIGHT)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        surface.fill((255, 255, 255))
        # for every robot you have to draw it in this section this also allows the robot to move
        robot1.draw()
        robot2.draw()
        robot3.Child.draw()
        robot4.Child.draw()
        robot5.Child.draw()
        #liquid.drawsprings()
        pg.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

game()
pg.quit()