import pygame as pg
from enum import Enum
from hero_sprites import WormSegment, Worm
from text import DebugPanel


class GameMode(Enum):
    START_SCREEN = 0
    STANDARD_PLAY = 1
    END_SCREEN = 10

debug = True

game_mode = GameMode(GameMode.STANDARD_PLAY)
pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()

running = True

debug = DebugPanel(screen)

#allsprites = pg.sprite.RenderPlain(worm_sprite)

worm = Worm()

def update_standard_play(dt):
    # Update worm sprite group
    worm.update(dt)

    screen.fill("black")

    worm.draw(screen)

    # screen.blit(worm_sprite.image,worm_sprite.pos)




def game_end():
    pass


def load_level():
    pass

def show_debug():
    mess_list = []
    for s in worm.sprites():
        mess_list.append(f'{s.target_position} | {s.direction}')

    debug.set_message_list(mess_list)
    debug.render()

dt = 1
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if game_mode == GameMode.START_SCREEN:
        pass        # TODO: Add start screen stuff
    elif game_mode == GameMode.STANDARD_PLAY:
        update_standard_play(dt)

    if debug:
        show_debug()

    pg.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000




