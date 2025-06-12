import pygame as pg
from better_sprite import BetterSprite

def update_ship(ship):
    keys = pg.key.get_pressed()

    if keys[pg.K_a]:
        ship.rotate(10)
    elif keys[pg.K_d]:
        ship.rotate(-10)
########################################################
pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()

ship = BetterSprite("assets/ship.gif")
ship.set_position(200,200)

dt = 1
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Update
    update_ship(ship)

    # Draw background (to write over previous render)
    screen.fill("black")

    # Draw ship
    ship.render(screen)

    # Update display
    pg.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

