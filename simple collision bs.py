# First try at a fluid simulation needs revamping for use

import pygame
import pygame as pg
import pymunk.pygame_util
pymunk.pygame_util.positive_y_is_up = False
RES = WIDTH, HEIGHT = 500, 500
FPS = 60
ball_m, ball_radius = 1, 6
pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)
space = pymunk.Space()
space.gravity = 0, 0

def create_ball(space, pos, ball_mass):
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    ball_body = pymunk.Body(ball_mass, ball_moment)
    ball_body.position = pos
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    ball_shape.elasticity = 0.9
    ball_shape.friction = 0.1
    space.add(ball_body, ball_shape)

def positions(size, num):
    plist = []
    for i in range(num):
        x = (size - (size // num)*i) - ball_radius*2
        for i in range(num):
            y = (size -(size // num)*i) - ball_radius*2
            plist.append([x, y])
    return plist
pos = positions(500, 35)
for i in pos:
    x = i[0]
    y = i[1]
    create_ball(space, (x, y), ball_m)

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

class Body():
    def __init__(self,space, size, posi):
        body_size, body_mass = size, 100
        body_moment = pymunk.moment_for_box(body_mass, body_size)
        self.body = pymunk.Body(body_mass, body_moment)
        self.body.position = posi
        shape = pymunk.Poly.create_box(self.body, size)
        shape.elasticity = 0.6
        shape.friction = 0.5
        space.add(self.body, shape)
body = Body(space, (30, 30), (250, 250))
while True:
    surface.fill(pg.Color("white"))

    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
        if i.type == pg.MOUSEBUTTONDOWN:
            create_ball(space, i.pos, 40)
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_LEFT:
                body.body.apply_impulse_at_local_point((-1000, 0), (0, 0))
            if i.key == pygame.K_RIGHT:
                body.body.apply_impulse_at_local_point((1000, 0), (0, 0))
            if i.key == pygame.K_UP:
                body.body.apply_impulse_at_local_point((0, -1000), (0, 0))
            if i.key == pygame.K_DOWN:
                body.body.apply_impulse_at_local_point((0, 1000), (0, 0))

    space.step(1/FPS)
    space.debug_draw(draw_options)

    pg.display.flip()
    clock.tick(FPS)
