from enum import Enum
import pygame as pg
from better_sprite import BetterSprite


class SegmentType(Enum):
    HEAD = 0
    MIDDLE = 1
    TAIL = 2


class WormSegment(BetterSprite):

    def __init__(self, seg_type:SegmentType):

        self.seg_type = seg_type
        if seg_type == SegmentType.HEAD:
            self.image = pg.image.load('assets/characters/worm_head.png').convert_alpha()
        elif seg_type == SegmentType.MIDDLE:
            self.image = pg.image.load('assets/characters/worm_middle.png').convert_alpha()
        elif seg_type == SegmentType.TAIL:
            self.image = pg.image.load('assets/characters/worm_tail.png').convert_alpha()

            # image and rect are Required by Group to wrap rendering
        self.image = pg.transform.scale_by(self.image, (.5, .5))
        BetterSprite.__init__(self, self.image)  # call super constructor

    def update(self):


        self.rotate(10)
        self.move(1,1)


class Worm(pg.sprite.RenderPlain):
    def __init__(self):
        pg.sprite.RenderPlain.__init__(self)  # call super constructor
        # init with 3 segs
        #self.segments = [WormSegment]

        self.create_worm()



    def create_worm(self):
        # self.segments.append(WormSegment(SegmentType.HEAD))
        # self.segments.append(WormSegment(SegmentType.MIDDLE))
        # self.segments.append(WormSegment(SegmentType.TAIL))

        self.add(WormSegment(SegmentType.HEAD))

    def update(self):
        pg.sprite.RenderPlain.update(self)
