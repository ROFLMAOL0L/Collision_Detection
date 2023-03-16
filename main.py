import random
import pygame
import math
import sys
import game_settings as g_s
import physics_functions as f_f
import trigonometry_functions as t_f
from circles import Circle

global particles
global screen


def create_circles_massive():
    for i in range(0, g_s.particles_amount):
        a_0 = random.randint(0, 360) / 180 * g_s.Pi
        particles.append(Circle(random.randint(g_s.max_particles_radius, g_s.screen_width - g_s.max_particles_radius),
                                random.randint(g_s.max_particles_radius, g_s.screen_height - g_s.max_particles_radius),
                                random.randint(g_s.min_particles_speed, g_s.max_particles_speed),
                                random.randint(g_s.min_particles_radius, g_s.max_particles_radius),
                                [math.cos(a_0), math.sin(a_0)], g_s.colors[random.randint(0, len(g_s.colors) - 1)]))


def particle_update(i):
    particles[i].move()
    if g_s.gravity_influence_switch == 1:
        particles[i].gravity_influence()
    particles[i].walls_collision_detection()

    # Cool representation for the velocity vectors of the balls (press 'F' key to show/hide it)
    if g_s.show_vectors == 1:
        pygame.draw.line(screen, (255, 0, 0), (particles[i].pos_x, g_s.screen_height - particles[i].pos_y),
                         (particles[i].pos_x + particles[i].velocity * particles[i].direction[0] * 10,
                          g_s.screen_height - particles[i].pos_y), 1)
        pygame.draw.line(screen, (0, 0, 255), (particles[i].pos_x, g_s.screen_height - particles[i].pos_y),
                         (particles[i].pos_x, (g_s.screen_height - particles[i].pos_y - particles[i].velocity *
                                               particles[i].direction[1] * 10)), 1)
    elif g_s.show_vectors == 2:
        pygame.draw.line(screen, (0, 255, 0), (particles[i].pos_x, g_s.screen_height - particles[i].pos_y),
                         (particles[i].pos_x + particles[i].velocity * particles[i].direction[0] * 10,
                          (g_s.screen_height - particles[i].pos_y - particles[i].velocity *
                           particles[i].direction[1] * 10)), 1)


def main():
    # Creating a massive that stores all the circles
    create_circles_massive()

    # Pygame stuff
    pygame.init()
    clock = pygame.time.Clock()
    run = 1
    while run == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    g_s.show_vectors = (g_s.show_vectors + 1) % 3
                if event.key == pygame.K_g:
                    g_s.gravity_influence_switch = (g_s.gravity_influence_switch + 1) % 2
        screen.fill(g_s.background_color)

        # Dividing regions into sub-regions (see physics_functions.py)
        a = f_f.quadtree(particles, 0, [])
        # And running collission detection and response system through those sub-regions
        for i in range(0, len(a)):
            for j in range(0, len(a[i])):
                for j_j in range(j + 1, len(a[i])):
                    f_f.particles_collision_detection(a[i][j], a[i][j_j])

        for i in range(0, g_s.particles_amount):
            pygame.draw.circle(screen, particles[i].color, (particles[i].pos_x, g_s.screen_height - particles[i].pos_y),
                               particles[i].radius)
            particles[i].direction = [math.cos((t_f.sin_to_a(particles[i].direction[0],
                                                             particles[i].direction[1])) / 180 * g_s.Pi),
                                      math.sin((t_f.sin_to_a(particles[i].direction[0],
                                                             particles[i].direction[1])) / 180 * g_s.Pi)]

            # Particle update
            particle_update(i)

        pygame.display.update()
        clock.tick(g_s.FPS)
    pygame.quit()


if __name__ == '__main__':
    particles = []
    screen = pygame.display.set_mode((g_s.screen_width, g_s.screen_height))
    main()
