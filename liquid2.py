# second try at liquid simulation
import pygame as pg
import pymunk.pygame_util
import math
import pymunk.constraints

pg.init()
RESo = WIDTH, HEIGHT = 500, 500
FPS = 60
surface = pg.display.set_mode(RESo)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)
space = pymunk.Space()
space.gravity = 0, 20
node_radius = 7
base_density, base_elasticity, base_friction = 1, 0.4, 0.9
muscle_density, muscle_elasticity, muscle_friction = 1, 0.5, 0.5
liquid_mass, liquid_radius = 10, 6

class Particle():
    def __init__(self, x, y,space):
        self.moment = pymunk.moment_for_circle(liquid_mass, 0, liquid_radius)
        self.body = pymunk.Body(liquid_mass, self.moment)
        self.body.position = (x,y)
        self.shape = pymunk.Circle(self.body, liquid_radius)
        self.shape.elasticity = 0.9
        self.shape.friction = 0.1
        self.shape.color = (30, 30, 100)
        space.add(self.body, self.shape)
    def draw(self):
        pg.draw.circle(surface, self.shape.color, self.body.position, liquid_radius)

class Spring():
    def __init__(self, a, b,space):
        self.body1 = a
        self.body2 = b
        self.length = calc_distance(a.position, b.position)
        joint = pymunk.DampedSpring(self.body1, self.body2, (0, 0), (0, 0), self.length, 10000, 8)
        space.add(joint)
    def draw(self):
        pg.draw.line(surface, (140, 20, 30), self.body1.position, self.body2.position, 2)

def calc_distance(p1, p2):
    distance = math.sqrt((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)
    return distance

class Liquid():
    def __init__(self, RES, diviser,space):
        self.particles = []
        self.positions = []
        self.springs = []
        for i in range(0,diviser):
            for a in range(0,diviser):
                x = RES[0]/diviser*i + RES[0]/diviser/2
                y = RES[1]/diviser*a + RES[1]/diviser/2
                pos = (x,y)
                self.positions.append(pos)
        for i in self.positions:
            self.particle = Particle(i[0],i[1],space)
            self.particles.append(self.particle)
        for particle in self.particles:
            for particle2 in self.particles:
                if calc_distance(particle.body.position, particle2.body.position) <= (RES[0]/diviser)  and calc_distance(particle.body.position, particle2.body.position) <= (RES[1]/diviser) and particle != particle2:
                    self.spring = Spring(particle.body, particle2.body,space)
                    self.springs.append(self.spring)
        self.edges = Edge_Points(RES, diviser, space)
        print(RES)
        for bodies in self.edges.bodies:
            for i in self.particles:
                if calc_distance(bodies.position,i.body.position) <= RES[0]/diviser and calc_distance(bodies.position,i.body.position) <= RES[1]/diviser:
                    spr = Spring(bodies, i.body,space)
                    self.springs.append(spr)
    def draw(self):
        for particle in self.particles:
            particle.draw()
        #for edge_points in self.edges.bodies:
            #pg.draw.circle(surface, (0,0,0), edge_points.position, 10)
    def drawsprings(self):
        for springs in self.springs:
            springs.draw()

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
        shape.elasticity = 0.2
        shape.friction = 0.4
        space.add(body, shape)
create_boundaries(space, WIDTH, HEIGHT)

class Edge_Points():
    def __init__(self, RES, diviser, space):
        top,bottom,left,right,self.bodies = [],[],[],[],[]
        for i in range(0,diviser):
            pos1 = (0,RES[1]/diviser*i)
            left.append(pos1)
            pos2 = (RES[0],RES[1]/diviser*i)
            right.append(pos2)
            pos3 = (RES[0]/diviser*i,0)
            bottom.append(pos3)
            pos4 = (RES[0]/diviser*i,RES[1])
            top.append(pos4)
        for i in left:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = i
            self.bodies.append(body)
        for i in right:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = i
            self.bodies.append(body)
        for i in bottom:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = i
            self.bodies.append(body)
        for i in top:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = i
            self.bodies.append(body)



#Edge_Points(RES, 10, space)
#def game():
    # This is the place to call more robots or test specific orientations you can change the number of nodes as well as initial position below:
 #   liquid = Liquid(RES, 20)
  #  while True:
   #     for event in pg.event.get():
    #        if event.type == pg.QUIT:
     #           return
      #  surface.fill((255, 255, 255))
        # for every robot you have to draw it in this section this also allows the robot to move
       # liquid.draw()
        #pg.display.update()
        #clock.tick(FPS)
        #space.step(1/FPS)

#game()
#pg.quit()
