from hero_sprites import WormSegment, WormDirection

# def path_location_for_distance(move_list:list[WormSegment.MoveTarget], distance):
#
#     m_i = len(move_list)-1
#     x = move_list[m_i].x
#     y = move_list[m_i].y
#
#     dist_moved = 0
#
#     while dist_moved < distance:
#         left_to_move = distance - dist_moved
#
#         xdiff = move_list[m_i - 1].x - move_list[m_i].x
#         ydiff = move_list[m_i - 1].y - move_list[m_i].y
#
#         if abs(xdiff) > 0:
#
#             if (dist_moved + abs(xdiff)) <= distance:
#                 x += xdiff
#                 dist_moved += abs(xdiff)
#                 m_i -= 1
#                 print(f'dist_moved={dist_moved}')
#             else:
#                 # Else only move the fraction of the distance left (should always be whole #)
#                 x += xdiff * (left_to_move / abs(xdiff))
#                 dist_moved += xdiff * (left_to_move / abs(xdiff))
#                 print(f'dist_moved={xdiff * (left_to_move / abs(xdiff))}')
#
#         if abs(ydiff) > 0:
#
#             if (dist_moved + abs(ydiff)) <= distance:
#                 y += ydiff
#                 dist_moved += abs(ydiff)
#                 m_i -= 1
#                 print(f'dist_moved={dist_moved}')
#             else:
#                 y += ydiff * (left_to_move / abs(ydiff))
#                 dist_moved += ydiff * (left_to_move / abs(ydiff))
#                 print(f'dist_moved={ydiff * (left_to_move / abs(ydiff))}')
#                 return x, y, m_i
#
#
#         if dist_moved == distance:
#             return x,y,m_i

#######################

# Head position
head_pos = {"x":4, "y":5}

# History of worm turns. Most recent is head
move_list: list[WormSegment.MoveTarget] = list()
move_list.append(WormSegment.MoveTarget({"x":0,"y":0},WormDirection.DOWN)),
move_list.append(WormSegment.MoveTarget({"x":0,"y":2},WormDirection.RIGHT)),
move_list.append(WormSegment.MoveTarget({"x":2,"y":2},WormDirection.DOWN)),
move_list.append(WormSegment.MoveTarget({"x":2,"y":3},WormDirection.RIGHT)),
move_list.append(WormSegment.MoveTarget({"x":4,"y":3},WormDirection.DOWN)),
move_list.append(WormSegment.MoveTarget({"x":4,"y":5},WormDirection.NONE))


# ######Test using function
# x,y,m_i = path_location_for_distance(move_list,3)
# print(f'x={x} | y={y} | m_i={m_i}')


######

# Worm segment locations (these will get updated).
# These should be WormSegments in the game
seg_list = [
    {"x":4, "y":5},     #head
    {"x":0, "y":0},
    {"x":0, "y":0},
    {"x":0, "y":0},
    {"x":0, "y":0}

]

# m_i = 0 #move list index
m_i = len(move_list)-1
s_i = 1 #seg list index

seg_distance = 3                #dist along trail between segs
dist_moved = 0                  #Dist moved along trail
running_x = head_pos['x']    #running track of how far we've calculated the move
running_y = head_pos['y']    #running track of how far we've calculated the move

#while m_i < len(move_list)-1:

while m_i >= 0 and s_i < len(seg_list):

    print(m_i)

    left_to_move = seg_distance-dist_moved

    xdiff = move_list[m_i-1].x - running_x
    ydiff = move_list[m_i-1].y - running_y

    if abs(xdiff) > 0:


        if (dist_moved + abs(xdiff)) < seg_distance:
            running_x += xdiff
            dist_moved += abs(xdiff)
            m_i -= 1
            print(f'seg_moved={dist_moved}')
        else:
            # Else only move the fraction of the distance left (should always be whole #)
            # Reset dist_moved
            running_x += xdiff * (left_to_move / abs(xdiff))
            print(f'seg_moved={xdiff * (left_to_move/abs(xdiff))}')
            seg_list[s_i]['x'] = running_x
            seg_list[s_i]['y'] = running_y
            print(f'setting seg{s_i} to x={running_x} | y={running_y} | dir={move_list[m_i - 1].direction}')
            dist_moved = 0
            s_i += 1



    #print(f'seg_moved={dist_moved}')

    elif abs(ydiff) > 0:

        if (dist_moved + abs(ydiff)) < seg_distance:
            running_y += ydiff
            dist_moved += abs(ydiff)
            m_i -= 1
            print(f'seg_moved={dist_moved}')
        else:
            running_y += ydiff * (left_to_move / abs(ydiff))
            print(f'seg_moved={ydiff * (left_to_move / abs(ydiff))}')
            seg_list[s_i]['x'] = running_x
            seg_list[s_i]['y'] = running_y
            print(f'setting seg{s_i} to x={running_x} | y={running_y} | dir={move_list[m_i - 1].direction}')
            dist_moved = 0
            s_i += 1

    else:   #Nowhere to go. Just stack seg on last one.
        print('stacking because no more in move list')
        seg_list[s_i]['x'] = running_x
        seg_list[s_i]['y'] = running_y
        print(f'setting seg{s_i} to x={running_x} | y={running_y} | dir={move_list[m_i - 1].direction}')
        s_i += 1




    ###########old way
    # if abs(xdiff) > 0:
    #     if abs(xdiff) <= seg_distance:
    #         dist_moved_x += xdiff
    #     else:
    #         dist_moved_x += seg_distance - dist_moved_x
    #
    #
    # if abs(ydiff) > 0:
    #     if  abs(ydiff) <= seg_distance:
    #         # If still haven't reached seg_distance with this diff, just add to dist_moved.
    #         dist_moved_y += ydiff
    #         # Else, get partial move and set segment's position to that.
    #     else:
    #         dist_moved_y += seg_distance - dist_moved_y
    #
    # print(f'xdiff={xdiff} | ydiff={ydiff}')
    # print(f'dist_moved_x={dist_moved_x} | dist_moved_y={dist_moved_y}')
    ###################



