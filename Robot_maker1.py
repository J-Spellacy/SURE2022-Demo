# Please Ignore This
# Robot_maker2 is a better prototype and functions, this doesn't


import pygame as pg
import pymunk.pygame_util
import random
import math

pymunk.pygame_util.positive_y_is_up = False

pg.init()
RES = WIDTH, HEIGHT = 500, 500
FPS = 60
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)
space = pymunk.Space()
space.gravity = 0, 20

node_radius, base_mass, muscle_mass, base_elasticity, muscle_elasticity, base_friction, muscle_friction, pos_i = 15, 10, 20, 0.5, 0.7, 0.5, 0.5, (200, 200)
node_pos_list, lines = [], []
class robot():
    def __init__(self, space, size, pos_i):
        num_node = range(0, size)
        angles, distances = [], []
        for i in num_node:
            node_type = random.randrange(0, 2)
            position = [random.randrange(pos_i[0]-90, pos_i[0]+90), random.randrange(pos_i[1]-90, pos_i[1]+90)]
            node_pos_list.append(position)
            bodies = []
            for i in node_pos_list:
                for a in node_pos_list:
                    line = [a, i]
                    lines.append(line)
                    #draw(space, surface, draw_options, line)
                    #if calc_distance(i, a) <= 2* node_radius:
                        #position = [position[0] + 2*node_radius, position[1] + 2*node_radius]
            if node_type == 0:
                node_moment = pymunk.moment_for_circle(base_mass, 0, node_radius)
                node_body = pymunk.Body(base_mass, node_moment)
                node_body.position = position
                node_shape = pymunk.Circle(node_body, node_radius)
                node_shape.elasticity = base_elasticity
                node_shape.friction = base_friction
                space.add(node_body, node_shape)
                bodies.append(node_body)
            if node_type == 1:
                node_moment = pymunk.moment_for_circle(muscle_mass, 0, node_radius)
                node_body = pymunk.Body(muscle_mass, node_moment)
                node_body.position = position
                node_shape = pymunk.Circle(node_body, node_radius)
                node_shape.elasticity = muscle_elasticity
                node_shape.friction = muscle_friction
                space.add(node_body, node_shape)
                bodies.append(node_body)
                node_shape.color = (255, 0, 0, 100)
            a = calc_angle(node_pos_list[0], position)
            angles.append(a)
            d = calc_distance(node_pos_list[0], position)
            distances.append(d)
            for i in bodies:
                for a in bodies:
                    #if a != i:
                    joints(a.body, i.body)
                    print(a, i)

class joints():
    def __init__(self, body_a, body_b):
        #self.body_a = body_a
        #self.body_b = body_b
        joint = pymunk.PinJoint(body_a, body_b)
        space.add(joint)

# make a new function to calculate distance between all nodes so you can make if statement to check distance is more than diameter

    #print(node_pos_list)
    #print(angles, distances)
def calc_distance(p1, p2):
    distance = math.sqrt((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)
    return distance

def draw(space, surface, draw_options, line):
    pg.draw.line(surface, "black", line[0], line[1], 3)
    space.debug_draw(draw_options)


def calc_angle(p1, p2):
    #gives radians of angle assume p2 is origin
    angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    return angle

def create_boundaries(space, width, height):
    rects = [
        [(width/2, height), (width, 1)],
        [(width / 2, 0), (width, 1)],
        [(0, height/2), (1, height)],
        [(width, height/2), (1, height)],
    ]
    for position, size in rects:
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = position
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.9
        shape.friction = 0.4
        space.add(body, shape)
create_boundaries(space, WIDTH, HEIGHT)

robot(space, 5, pos_i)
while True:
    surface.fill(pg.Color("white"))
    for line in lines:
        draw(space, surface, draw_options, line)
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
    space.step(1/FPS)
    space.debug_draw(draw_options)

    pg.display.update()
    clock.tick(FPS)
