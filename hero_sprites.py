from enum import Enum
import pygame as pg
from better_sprite import BetterSprite
import math



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
        head.set_position(300,300)
        self.add(head)

        seg = WormSegment(WormSegment.SegmentType.MIDDLE)
        seg.set_position(head.rect.x-head.rect.width, 300)
        seg.set_new_target({"x": head.rect.x,"y":head.rect.y}, WormDirection.LEFT)
        self.add(seg)

        # tail = WormSegment(WormSegment.SegmentType.TAIL)
        # tail.set_position(seg.rect.x-head.rect.width, 300)
        # tail.set_new_target({"x": seg.rect.x, "y": seg.rect.y}, WormDirection.LEFT)
        # self.add(tail)

    def update(self, dt):
        self.update_move(dt)

        pg.sprite.RenderPlain.update(self, dt)

    def update_move(self, dt):

        # Move head. See if direction changed
        head: WormSegment = self.sprites()[0]

        did_move, dir_change = self.move_head(dt)

        self.move_segs(dt)

    def move_head(self, dt):
        keys = pg.key.get_pressed()

        head: WormSegment = self.sprites()[0]
        did_move = False
        prev_direction = head.direction

        if keys[pg.K_w]:
            head.set_rotate(90)
            head.move(0, -self.speed * dt)
            head.direction = WormDirection.UP
            did_move = True
        elif keys[pg.K_s]:
            head.set_rotate(270)
            head.move(0, self.speed * dt)
            head.direction = WormDirection.DOWN
            did_move = True
        elif keys[pg.K_a]:
            head.set_rotate(0)
            head.flip_x()
            head.move(-self.speed * dt, 0)
            head.direction = WormDirection.LEFT
            did_move = True
        elif keys[pg.K_d]:
            head.set_rotate(0)

            head.move(self.speed * dt, 0)
            head.direction = WormDirection.RIGHT
            did_move = True

        # Return bool to indicate if direction changed
        return did_move, (head.direction != prev_direction)

    def move_segs(self, dt):
        i = 0
        for seg in self.sprites()[1:]:
            seg: WormSegment = seg
            prev_seg:WormSegment = self.sprites()[i]

            # Calcuate angle to previous seg
            y_diff = prev_seg.y() - seg.y()
            x_diff = prev_seg.x() - seg.x()

            # Get angle from head to seg
            angle = math.atan2(y_diff, x_diff)
            angle_deg = math.degrees(angle)

            # set rotation to point at previous seg
            seg.set_rotate(-angle_deg)

            # # Snap position to edge of previous seg
            new_x = prev_seg.x() - (58 * math.cos(angle))
            new_y = prev_seg.y() + (58 * math.sin(angle))

            seg.set_position(new_x, new_y, center=True)

            i += 1





