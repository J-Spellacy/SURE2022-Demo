import pygame as pg
import pymunk.pygame_util
import random
import math
import pymunk.constraints
import pickle
import Robot_maker2
import liquid2
#import Combiner
#import Main

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


def save_R(object):
    file_to_store = open("stored_robot.pickle", "wb")
    pickle.dump(object, file_to_store)
    file_to_store.close()

def load_R():
    file_to_read = open("stored_robot.pickle", "rb")
    loaded_robot = pickle.load(file_to_read)
    file_to_read.close()
    return loaded_robot

def save_L(object):
    file_to_store = open("stored_object.pickle", "wb")
    pickle.dump(object, file_to_store)
    file_to_store.close()

def load_L():
    file_to_read = open("stored_object.pickle", "rb")
    loaded_object = pickle.load(file_to_read)
    file_to_read.close()
    return loaded_object