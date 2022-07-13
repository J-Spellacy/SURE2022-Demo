## make corners for fluid

# needs to send the current generation into simulation one at a time
# needs to save performance metrics alongside model
# either on here or on another file needs to cut down generations with gradient with respect to amount of muscle and distance from pos_i
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
RES = WIDTH, HEIGHT = 800, 800
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



def game():
    # This is the place to call more robots or test specific orientations you can change the number of nodes as well as initial position below:
    Robot_maker2.Boundaries(space, WIDTH, HEIGHT)
    rem = Robot_maker2.Robot(5, (RES[0]/2, RES[1]/2),space)
    liquid = liquid2.Liquid(RES, 25,space)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        surface.fill((255, 255, 255))
        # for every robot you have to draw it in this section this also allows the robot to move
        rem.draw()
        liquid.draw()
        liquid.drawsprings()
        pg.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

game()
pg.quit()
