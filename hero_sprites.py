from enum import Enum
import pygame as pg
from better_sprite import BetterSprite




class WormDirection(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


class WormSegment(BetterSprite):

    class SegmentType(Enum):
        HEAD = 0
        MIDDLE = 1
        TAIL = 2

    def __init__(self, seg_type:SegmentType, target_position=None, direction: WormDirection = WormDirection.LEFT):

        self.seg_type = seg_type
        if seg_type == self.SegmentType.HEAD:
            self.image = pg.image.load('assets/characters/worm_head.png').convert_alpha()
        elif seg_type == self.SegmentType.MIDDLE:
            self.image = pg.image.load('assets/characters/worm_middle.png').convert_alpha()
        elif seg_type == self.SegmentType.TAIL:
            self.image = pg.image.load('assets/characters/worm_tail.png').convert_alpha()

        # image and rect are Required by Group to wrap rendering
        self.image = pg.transform.scale_by(self.image, (.5, .5))
        BetterSprite.__init__(self, self.image)  # call super constructor

        self.target_position = target_position
        self.direction = direction

    def set_new_target(self, target_position, direction):
        self.target_position = target_position
        self.direction = direction

    def update(self, dt):
        pass
        #### Test
        # self.rotate(10)
        # self.move(1,1)

        # if self.seg_type == SegmentType.HEAD:
        #     self.move_head(dt)


class Worm(pg.sprite.RenderPlain):

    def __init__(self):
        pg.sprite.RenderPlain.__init__(self)  # call super constructor

        self.speed = 300

        self.create_worm()

    def create_worm(self):

        ### init with head, segment, and tail

        head = WormSegment(WormSegment.SegmentType.HEAD)
        head.move(300,300)
        self.add(head)

        seg = WormSegment(WormSegment.SegmentType.MIDDLE)
        seg.move(head.rect.x+head.rect.width, 300)
        seg.set_new_target({"x": head.rect.x,"y":head.rect.y}, WormDirection.LEFT)
        self.add(seg)

        tail = WormSegment(WormSegment.SegmentType.TAIL)
        tail.move(seg.rect.x + head.rect.width, 300)
        tail.set_new_target({"x": seg.rect.x, "y": seg.rect.y}, WormDirection.LEFT)
        self.add(tail)

    def update(self, dt):
        self.update_move(dt)

        pg.sprite.RenderPlain.update(self, dt)

    def update_move(self, dt):

        # Move head. See if direction changed
        head: WormSegment = self.sprites()[0]
        did_move, dir_change = self.move_head(dt)

        # If head has changed direction, update first segment target if exists
        if dir_change and len(self.sprites()) > 1:
            self.sprites()[1].set_new_target({"x": head.rect.x,"y":head.rect.y}, head.direction)

        if did_move:
            self.move_segs(dt)

    def move_head(self, dt):
        keys = pg.key.get_pressed()

        head: WormSegment = self.sprites()[0]
        did_move = False
        prev_direction = head.direction

        if keys[pg.K_w]:
            head.set_rotate(270)
            head.move(0, -self.speed * dt)
            head.direction = WormDirection.UP
            did_move = True
        elif keys[pg.K_s]:
            head.set_rotate(90)
            head.move(0, self.speed * dt)
            head.direction = WormDirection.DOWN
            did_move = True
        elif keys[pg.K_a]:
            head.set_rotate(0)
            head.move(-self.speed * dt, 0)
            head.direction = WormDirection.LEFT
            did_move = True
        elif keys[pg.K_d]:
            head.set_rotate(0)
            head.flip_x()
            head.move(self.speed * dt, 0)
            head.direction = WormDirection.RIGHT
            did_move = True

        # Return bool to indicate if direction changed
        return did_move, (head.direction != prev_direction)

    def move_segs(self, dt):
        for s in self.sprites()[1:]:
            if s.direction == WormDirection.UP:
                if s.rect.y <= s.target_position['y']:
                    s.move(0, -self.speed * dt)
                # else:





