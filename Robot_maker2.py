# Creates one randomly generated "Robot" at a time can make multiple. By running the program the robot will be generated fore-warning the robots are 99% of the time very useless.

import pygame as pg
import pymunk.pygame_util
import random
import math
import pymunk.constraints
import pickle

pymunk.pygame_util.positive_y_is_up = False

pg.init()
RES = WIDTH, HEIGHT = 500, 500
FPS = 60
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)
space = pymunk.Space()
space.gravity = 0, 100
node_radius = 7
base_density, base_elasticity, base_friction = 1, 0.4, 0.9
muscle_density, muscle_elasticity, muscle_friction = 1, 0.5, 0.5

class Node():
    def __init__(self, x, y,space,gen,type):
        self.body = pymunk.Body()
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, node_radius)
        if gen != 1:
          self.type = type
        else:
            self.type = random.randrange(0, 2)
        if self.type == 0:
            self.shape.density = base_density
            self.shape.elasticity = base_elasticity
            self.shape.friction = base_friction
            self.shape.color = (20, 169, 190, 100)
        elif self.type == 1:
            self.shape.density = muscle_density
            self.shape.elasticity = muscle_elasticity
            self.shape.friction = muscle_friction
            self.shape.color = (255, 0, 0, 100)
        space.add(self.body, self.shape)
    def draw(self):
        pg.draw.circle(surface, self.shape.color, self.body.position, node_radius)

class String():
    def __init__(self, a, b,space):
        self.body1 = a
        self.body2 = b
        joint = pymunk.PinJoint(self.body1, self.body2)
        space.add(joint)
    def draw(self):
        pos1 = self.body1.position
        pos2 = self.body2.position
        pg.draw.line(surface, (70, 60, 200), pos1, pos2, 2)

class Muscle():
    def __init__(self, a, b,space):
        self.mtype = 1
        self.body1 = a
        self.body2 = b
        self.length = calc_distance(a.position, b.position)
        joint  = pymunk.DampedSpring(self.body1, self.body2, (0,0), (0,0), self.length, 500, 0.5)
        space.add(joint)
    def contract(self):
        self.angle = calc_angle(self.body1.position, self.body2.position)
        force = self.length
        fx = math.cos(self.angle) * force
        fy = math.sin(self.angle) * force
        fxb = math.cos(-self.angle) * force
        fyb = math.sin(-self.angle) * force
        self.body1.apply_impulse_at_local_point((fx, fy), (0,0))
        self.body2.apply_impulse_at_local_point((-fxb,-fyb), (0,0))
        ##draws the line of the force and prints angle
        #pg.draw.line(surface,(0,0,0), self.body1.position, (self.body1.position[0]+fx/2,self.body1.position[1]+fy/2), 3)
        #pg.draw.line(surface, (0, 0, 0), self.body2.position,(self.body2.position[0] - fx/2, self.body2.position[1] - fy/2), 3)
        #print(self.angle)
        #print(self.length)
    def draw(self):
        pg.draw.line(surface, (140, 20, 30), self.body1.position, self.body2.position, 2)

class Mixed_Muscle():
    def __init__(self, a, b,space):
        self.mtype =  0
        self.body1 = a
        self.body2 = b
        self.length = calc_distance(a.position, b.position)
        joint  = pymunk.DampedSpring(self.body1, self.body2, (0,0), (0,0), calc_distance(self.body1.position, self.body2.position), 900, 9)
        space.add(joint)
    def contract(self):
        self.angle = calc_angle(self.body1.position, self.body2.position)
        force = self.length/1
        fx = math.cos(self.angle) * force
        fy = math.sin(self.angle) * force
        fxb = math.cos(-self.angle) * force
        fyb = math.sin(-self.angle) * force
        self.body1.apply_impulse_at_local_point((fx, fy), (0,0))
        self.body2.apply_impulse_at_local_point((-fxb,-fyb), (0,0))
    def draw(self):
        pos1 = self.body1.position
        pos2 = self.body2.position
        pg.draw.line(surface, (140, 20, 30), pos1, pos2, 2)

def calc_distance(p1, p2):
    distance = math.sqrt((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)
    return distance

def calc_angle(p1, p2):
    #gives radians of angle assume p2 is origin
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

class Robot():
    def __init__(self, size, i_pos,space,gen,n_pos,types,samp):
        self.gen = gen
        self.size = size
        self.i_pos = i_pos
        print(i_pos)
        positions, alldists = [], []
        Cangles, Cdistances = [], []
        if gen == 1:
            for i in range(0, size):
                pos = (random.randrange(i_pos[0]-100, i_pos[0]+100),random.randrange(i_pos[1]-100, i_pos[1]+100))
                positions.append(pos)
                self.positions = positions
                for a in positions:
                    for b in positions:
                        d = calc_distance(a, b)
                        alldists.append(d)
            alldists = list(dict.fromkeys(alldists))
            if 0 in alldists:
                alldists.remove(0)
            self.alldists = alldists
        else:
            positions = n_pos
        nodes = []
        if gen == 1:
            for i in positions:
                node = Node(i[0], i[1], space,gen,[])
                nodes.append(node)
                self.nodes = nodes
        elif gen != 1:
            for (i,j) in zip(positions,types):
                node = Node(i[0], i[1], space,gen,j)
                nodes.append(node)
                self.nodes = nodes
        strings, muscles = [], []
        connections_num = random.randint(2,size*(size-1)/2)
        if gen == 1:
            self.sample = random.choices(self.nodes, k = connections_num)
        else:
            self.sample =  samp
        for i in self.sample:
            for a in self.nodes:
                if i.type == 0 and a.type == 0 and a != i:
                    string = String(i.body,a.body,space)
                    strings.append(string)
                elif i.type == 1 and a.type == 1 and a != i:
                    muscle = Muscle(i.body,a.body,space)
                    muscles.append(muscle)
                elif i.type == 1 and a.type == 0 and a != i:
                    muscle = Mixed_Muscle(i.body,a.body,space)
                    muscles.append(muscle)
                elif i.type == 0 and a.type == 1 and a != i:
                    muscle = Mixed_Muscle(i.body,a.body,space)
                    muscles.append(muscle)
        self.muscles = muscles
        self.strings = strings

    def draw(self):
        for i in self.nodes:
            i.draw()
        for i in self.muscles:
            i.draw()
            i.contract()
        for i in self.strings:
            i.draw()

    def record(self):
        current_positions = [0, 0]
        for i in self.nodes:
            current_positions[0] += i.body.position[0]
            current_positions[1] += i.body.position[1]
        self.avg_position  = (current_positions[0]/self.size,current_positions[1]/self.size)
        print(self.avg_position)

class Boundaries():
        def __init__(self,space, width, height):
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
                shape.elasticity = 0.2
                shape.friction = 0.4
                space.add(body, shape)
Boundaries(space, WIDTH, HEIGHT)

#def game():
    # This is the place to call more robots or test specific orientations you can change the number of nodes as well as initial position below:
    #rem = Robot(5, (200, 200))
    #while True:
     #   for event in pg.event.get():
     #       if event.type == pg.QUIT:
     #           return
     #   surface.fill((255, 255, 255))
     #   # for every robot you have to draw it in this section this also allows the robot to move
     #   rem.draw()
     #   pg.display.update()
     #   clock.tick(FPS)
     #   space.step(1/FPS)

#game()
#pg.quit()