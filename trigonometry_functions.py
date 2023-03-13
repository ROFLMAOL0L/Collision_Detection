import math


def sin_to_a(cosin, sinus):
    a = math.asin(sinus) * 180 / math.pi
    if cosin * sinus > 0:
        if cosin > 0:
            return a
        else:
            return (180 - a) % 360
    elif cosin * sinus == 0:
        if cosin == 0:
            return a
        else:
            return a
    else:
        if cosin > 0:
            return (360 + a) % 360
        else:
            return (180 - a) % 360


def arctan(dx, dy):
    if dy != 0:
        if dx * dy <= 0:
            return math.pi - math.atan(dy / dx)
        else:
            return math.atan(dy / dx)


def point_spin(x, y, alfa, direction):
    # This function is used in the physics_functions/particles_collision_detection to rotate the whole system of vectors
    # and blah blah blah, we all hate physics so no one cares. It takes a point (sincerely, a radius-vector),
    # an angle and rotation direction (1 - clockwise, 0 - counter) and returns that point rotated.
    if direction != 1:
        dx = math.cos(alfa) * x - math.sin(alfa) * y
        dy = math.sin(alfa) * x + math.cos(alfa) * y
    else:
        dx = math.cos(alfa) * x + math.sin(alfa) * y
        dy = -math.sin(alfa) * x + math.cos(alfa) * y
    ans = (dx, dy)
    return ans
