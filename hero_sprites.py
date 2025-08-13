from enum import Enum
import pygame as pg
from better_sprite import BetterSprite




class WormDirection(Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    NONE = -1


class WormSegment(BetterSprite):

    class SegmentType(Enum):
        HEAD = 0
        MIDDLE = 1
        TAIL = 2

    class MoveTarget:

        def __init__(self, pos:dict, direction):
            self.x: int = pos['x']
            self.y: int = pos['y']
            self.direction: WormDirection = direction

    def __init__(self, seg_type:SegmentType, target_position=None, direction: WormDirection = WormDirection.LEFT):

        self.seg_type = seg_type

        image_file = None
        if seg_type == self.SegmentType.HEAD:
            image_file = 'assets/characters/worm_head.png'
        elif seg_type == self.SegmentType.MIDDLE:
            image_file = 'assets/characters/worm_middle.png'
        elif seg_type == self.SegmentType.TAIL:
            image_file = 'assets/characters/worm_tail.png'

        BetterSprite.__init__(self, image_file, scale=.5)  # call super constructor

        self.direction = WormDirection.RIGHT
        self.target_list = []


    def add_move_target(self, target_position:dict, direction):
        self.target_list.append(self.MoveTarget(target_position, direction))

    def remove_target(self):
        self.target_list.pop(0)

    def set_direction(self, direction: WormDirection):
        self.direction = direction
        if direction == WormDirection.UP:
            self.set_rotate(90)
        elif direction == WormDirection.DOWN:
            self.set_rotate(270)
        elif direction == WormDirection.LEFT:
            self.set_rotate(0)
            self.flip_x()
        elif direction == WormDirection.RIGHT:
            self.set_rotate(0)


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
        seg.move(head.rect.x-head.rect.width, 300)
        seg.add_move_target({"x": head.x(),"y":head.y()}, WormDirection.LEFT)
        self.add(seg)

        tail = WormSegment(WormSegment.SegmentType.TAIL)
        tail.move(seg.rect.x-head.rect.width, 300)
        tail.add_move_target({"x": seg.x(), "y": seg.y()}, WormDirection.LEFT)
        self.add(tail)

    def update(self, dt):
        self.update_move(dt)

        pg.sprite.RenderPlain.update(self, dt)

    def update_move(self, dt):

        # Move head. See if direction changed
        head: WormSegment = self.sprites()[0]
        did_move, dir_change, head_loc_before_move = self.move_head(dt)

        # # If head has changed direction, update first segment target if exists
        if dir_change and len(self.sprites()) >= 1:

            target_to_add = head_loc_before_move
            print(f'Head direction change: {target_to_add}')
            s:WormSegment
            i: int = 1
            for s in self.sprites()[1:]:

                s.add_move_target(target_to_add, head.direction)

                i+= 1

        if did_move:
            self.move_segs(dt, head)

    def move_head(self, dt):
        keys = pg.key.get_pressed()

        head: WormSegment = self.sprites()[0]
        did_move = False
        prev_direction = head.direction
        location_before_move = head.get_position()

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
        return did_move, (head.direction != prev_direction), location_before_move

    def move_segs(self, dt, head):

        s: WormSegment
        i: int = 1
        for s in self.sprites()[1:]:
            parent_seg = self.sprites()[i - 1]

            # If no target, set to parent seg (should this ever happen??)
            if len(s.target_list) == 0:
                s.add_move_target(parent_seg.get_position(), parent_seg.direction)

            # Get current target to process
            target_position:WormSegment.MoveTarget = s.target_list[0]

            reached_target = self.move_single_seg(dt,s, target_position)

            if reached_target:
                new_direction = s.target_list[0].direction
                s.remove_target()

                if len(s.target_list) == 0:
                    s.add_move_target(parent_seg.get_position(), parent_seg.direction)
                    new_direction = parent_seg.direction

                target_position: WormSegment.MoveTarget = s.target_list[0]
                s.set_direction(new_direction)

                reached_target = self.move_single_seg(dt, s, target_position)
                if reached_target:
                    print('reached target for new move. Shouldn''t happen!')


            i += 1

    def move_single_seg(self, dt, s:WormSegment, target_position:WormSegment.MoveTarget):
        reached_target = False
        if s.direction == WormDirection.UP:
            if s.y() > target_position.y:
                s.move(0, -self.speed * dt)
            else:
                #s.set_position(target_position.x, target_position.y)
                return True         #reached target
        elif s.direction == WormDirection.DOWN:
            if s.y() < target_position.y:
                s.move(0, self.speed * dt)
            else:
                #s.set_position(target_position.x, target_position.y)
                return True         #reached target
        elif s.direction == WormDirection.LEFT:
            if s.x() > target_position.x:
                s.move(-self.speed * dt, 0)
            else:
                #s.set_position(target_position.x, target_position.y)
                return True         #reached target
        elif s.direction == WormDirection.RIGHT:
            if s.x() < target_position.x:
                s.move(self.speed * dt, 0)
            else:
                #s.set_position(target_position.x, target_position.y)
                return True         #reached target


        return False





