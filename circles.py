import game_settings as g_s
import math


class Circle:
    def __init__(self, pos_x0, pos_y0, velocity_0, radius, direction, color):
        self.pos_x = pos_x0
        self.pos_y = pos_y0
        self.density = g_s.particles_density
        self.velocity = velocity_0
        self.radius = radius
        self.direction = direction
        self.color = color

    def move(self):
        # Movement function, really simple yet working. Velocity vector is represented as binary direction vectors
        # and module of velocity aka speed amount aka length of velocity vector. I use different ways of working with
        # velocity vectors, so this representation is very flex imho.
        self.pos_x += self.velocity * self.direction[0]
        self.pos_y += self.velocity * self.direction[1]

    def walls_collision_detection(self):
        # Changing their position directly helps to avoid getting the balls stuck or even get outside the screen
        if self.pos_x > g_s.screen_width - self.radius:
            self.direction[0] *= (-1)
            self.pos_x = g_s.screen_width - self.radius
        elif self.pos_x < self.radius:
            self.direction[0] *= (-1)
            self.pos_x = self.radius
        if self.pos_y > g_s.screen_height - self.radius:
            self.direction[1] *= (-1)
            self.pos_y = g_s.screen_height - self.radius
        elif self.pos_y < self.radius:
            self.direction[1] *= (-1)
            self.pos_y = self.radius

    def gravity_influence(self):
        # Here gravity is represented as a vector (0, -gravitational_force) and the velocity is found by adding those
        # two vectors together. In order to come back to the usual binary-direction and value we have to use some
        # trigonometry...
        a = [self.velocity * self.direction[0], self.velocity * self.direction[1] + g_s.gravitational_force[1]]
        c = math.sqrt(a[0] ** 2 + a[1] ** 2)
        self.velocity = c - g_s.air_resistance
        self.direction = [a[0] / c, a[1] / c]   # ...here
