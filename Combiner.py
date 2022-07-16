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
space.gravity = 0, 0
node_radius = 7
base_density, base_elasticity, base_friction = 1, 0.4, 0.9
muscle_density, muscle_elasticity, muscle_friction = 1, 0.5, 0.5
liquid_mass, liquid_radius = 10, 6

robot1 = Robot_maker2.Robot(5,(110,110),space,1,[],[],[])
robot2 = Robot_maker2.Robot(5,(590,110),space,1,[],[],[])

class Robot_combine():
    def __init__(self,a,b,position):
        positionsa,positionsb,types,n_sample = [],[],[],[]
        if a.gen >= b.gen:
            gen = a.gen #+ 1
        elif b.gen > a.gen:
            gen = b.gen #+ 1
        if len(a.nodes) >  len(b.nodes):
            length = len(a.nodes)
        elif len(b.nodes) >= len(a.nodes):
            length = len(b.nodes)
        num = random.randint(0,length)
        rest = length - num
        anodes = random.choices(a.nodes, k=num)
        bnodes = random.choices(b.nodes, k=rest)
        for i in anodes:
            t = i.type
            an1 = i.body.position[0] - a.i_pos[0]
            an2 = i.body.position[1] - a.i_pos[1]
            norm_pos = (an1,an2)
            positionsa.append(norm_pos)
            types.append(t)
            for j in a.sample:
                if i == j:
                    n_sample.append(i)
        for i in bnodes:
            t = i.type
            bn1 = i.body.position[0] - b.i_pos[0]
            bn2 = i.body.position[1] - b.i_pos[1]
            norm_pos = (bn1,bn2)
            positionsb.append(norm_pos)
            types.append(t)
            for j in b.sample:
                if i == j:
                    n_sample.append(i)
        pos = positionsb + positionsa
        self.Child = Robot_maker2.Robot(length,position,space,gen,pos, types,n_sample)

robot3 = Robot_combine(robot1,robot2,(110,390))
robot4 = Robot_combine(robot1,robot2,(590,390))
robot5 = Robot_combine(robot3.Child,robot4.Child,(300,490))

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
        #space.step(1/FPS)

game()
pg.quit()