import game_settings
from trigonometry_functions import *
from random import randint
global region_answer
last_region_length = 10


def quadtree_divide(region, i):
    # Firstly, sort everything
    sort_by(region, i)

    # Then divide region in two equal ones. (equal means they have an equal amount of particles in it which makes
    # division in regions more effective)
    region_length = len(region)
    a = region[0:int(region_length / 2)]
    b = region[int(region_length / 2):]

    # Doing the recursion only if the next step is possible. (the next sub-region has to be not less than
    # last_region_length)
    if len(a) <= last_region_length:
        if len(b) <= last_region_length:
            region_answer.append(a)
            region_answer.append(b)
        else:
            region_answer.append(a)
            quadtree_divide(b, (i + 1) % 2)
    else:
        if len(b) <= last_region_length:
            quadtree_divide(a, (i + 1) % 2)
            region_answer.append(b)
        else:
            quadtree_divide(a, (i + 1) % 2)
            quadtree_divide(b, (i + 1) % 2)


def quadtree(region_e, i_e, region_answer_e):
    global region_answer
    region_answer = []
    quadtree_divide(region_e, i_e)
    return region_answer


def sort_by(region, x_or_y):
    if x_or_y == 1:
        region.sort(key=lambda x: x.pos_x)
    else:
        region.sort(key=lambda y: y.pos_y)


def particles_collision_detection(c_1, c_2):
    r1, r2 = c_1.radius, c_2.radius
    m1, m2 = math.pi * (r1 ** 2) * c_1.density, math.pi * (r2 ** 2) * c_2.density
    v1, v2 = c_1.velocity, c_2.velocity
    dx = c_1.pos_x - c_2.pos_x
    dy = c_1.pos_y - c_2.pos_y
    distance_c1c2 = math.sqrt(dx ** 2 + dy ** 2) + 0.01
    if distance_c1c2 * 0.99 <= r1 + r2:
        # Spin so that normal is horizontal
        feta = sin_to_a(dx / distance_c1c2, dy / distance_c1c2) / 180 * math.pi
        vr_1 = point_spin(c_1.direction[0], c_1.direction[1], feta, 1)
        vr_2 = point_spin(c_2.direction[0], c_2.direction[1], feta, 1)

        # Swap x components of speed vectors
        dx1, dy1 = vr_2[0] * v2, vr_1[1] * v1
        dx2, dy2 = vr_1[0] * v1, vr_2[1] * v2

        # Find new directions of the speed vectors
        df_1 = math.sqrt(dx1 ** 2 + dy1 ** 2)
        df_2 = math.sqrt(dx2 ** 2 + dy2 ** 2)
        vrx_1 = dx1 / df_1
        vry_1 = dy1 / df_1
        vrx_2 = dx2 / df_2
        vry_2 = dy2 / df_2

        # Spin the rotated vectors to their homeland (home-plane, since we kind of rotated the xy plane)
        vf_1 = point_spin(vrx_1, vry_1, feta, -1)
        vf_2 = point_spin(vrx_2, vry_2, feta, -1)

        # Change the direction of balls
        c_1.direction[0] = vf_1[0]
        c_1.direction[1] = vf_1[1]
        c_2.direction[0] = vf_2[0]
        c_2.direction[1] = vf_2[1]

        # Cool effect (changing colors when collide)
        # colors = [(255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255), (0, 0, 255), (0, 255, 0)]
        # c_1.color, c_2.color = colors[randint(0, 5)], colors[randint(0, 5)]

        # Actual physics, I duwonna explain
        c_1.velocity = abs(v1 * (m1 - m2) + 2 * m2 * v2) / (m1 + m2)
        c_2.velocity = abs(v2 * (m2 - m1) + 2 * m1 * v1) / (m1 + m2)

        # Overlap correction
        overlap_amount = (r1 + r2 - distance_c1c2) / 2
        c_1.pos_x += overlap_amount * math.cos(feta)
        c_1.pos_y += overlap_amount * math.sin(feta)
        c_2.pos_x += overlap_amount * math.cos(360 - feta)
        c_2.pos_y += overlap_amount * math.sin(360 - feta)
        return True
    return False
