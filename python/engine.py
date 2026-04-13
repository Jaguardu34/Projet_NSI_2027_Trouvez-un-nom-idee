import math

import pygame
import pymunk
import pymunk.pygame_util
from entity import segment as seg
from entity.muscle import Muscle

# Before you can do much with pygame, you will need to initialize it
pygame.init()
# Init de clock
clock = pygame.time.Clock()

CIEL = 0, 200, 255  # parenthèses inutiles, l'interpréteur reconnaît un tuple

debug = True


def get_distance(body_a, body_b, anchor_a, anchor_b):
    # Convertit les ancres en coordonnées monde
    pa = body_a.local_to_world(anchor_a)
    pb = body_b.local_to_world(anchor_b)
    return math.dist(pa, pb)


def main():

    screen = pygame.display.set_mode((640, 480))

    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # Creation de l'espace avec pymunk
    space = pymunk.Space()
    space.gravity = 0, 900

    # Sol

    sol = seg.Segment((0, 480), (640, 480), space, elasticity=1, friction=0.4)
    sol.add_in_space(space)

    mur_droite = seg.Segment((640, 0), (640, 480), space, elasticity=1, friction=0.4)
    mur_droite.add_in_space(space)

    mur_gauche = seg.Segment((0, 0), (0, 480), space, elasticity=1, friction=0.4)
    mur_gauche.add_in_space(space)

    # Balle

    right_rib = pymunk.Body(body_type=pymunk.Body.STATIC)
    right_rib.position = 390, 110
    right_rib_shape = pymunk.Segment(right_rib, (0, 0), (-10, 100), 4)
    space.add(right_rib, right_rib_shape)

    # b_arm1 ancré au monde mais reste dynamique (peut tourner)
    right_arm = pymunk.Body(10, pymunk.moment_for_segment(10, (0, 0), (100, 0), 4))
    right_arm.position = 400, 100
    right_arm_shape = pymunk.Segment(right_arm, (0, 0), (100, 0), 4)

    # Pivot fixe à l'épaule
    # shoulder = pymunk.PivotJoint(space.static_body, b_arm1, (400, 100))
    # space.add(shoulder)

    # b_arm2 entièrement dynamique
    right_forearm = pymunk.Body(10, pymunk.moment_for_segment(10, (0, 0), (0, -100), 4))
    right_forearm.position = 510, 85
    right_forearm_shape = pymunk.Segment(right_forearm, (0, 0), (0, -100), 4)

    # Pivot à l'articulation (coude)
    elbow = pymunk.PivotJoint(right_arm, right_forearm, (510, 95))
    elbow_max = pymunk.RotaryLimitJoint(right_arm, right_forearm, -1.5, 1.5)
    space.add(elbow, elbow_max)

    right_shoulder = pymunk.PivotJoint(right_rib, right_arm, (400, 100))
    shoulder_limit = pymunk.RotaryLimitJoint(right_rib, right_arm, -1.5, 1.5)
    space.add(right_shoulder, shoulder_limit)

    right_biceps = Muscle(right_arm, right_forearm, (20, -4), (-4, -10), space)

    right_triceps = Muscle(right_arm, right_forearm, (20, 4), (0, 20), space)

    right_dorsal = Muscle(right_rib, right_arm, (-10, 40), (20, 5), space)

    right_deltoid = Muscle(right_rib, right_arm, (-50, -10), (-2, -15), space)

    space.add(right_arm, right_arm_shape, right_forearm, right_forearm_shape)

    # loop
    loop = True

    space.iterations = 30  # default = 10

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.KEYDOWN:
                # calcul des nouvelles coordonnées du rond
                if event.key == pygame.K_SPACE:
                    # right_biceps_contract = True
                    # right_biceps_strenght = 0
                    right_biceps.update(True)
                    right_triceps.update(False)
                elif event.key == pygame.K_d:
                    right_deltoid.update(True)
                    right_dorsal.update(False)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    # right_biceps_contract = False
                    # right_biceps_strenght = 140
                    right_biceps.update(False)
                    right_triceps.update(True)
                elif event.key == pygame.K_d:
                    right_deltoid.update(False)
                    right_dorsal.update(True)

        # Superposition du fond ciel
        screen.fill("gray")  # Efface l'écran

        steps = 10
        for _ in range(steps):
            space.step(0.01 / steps)

        space.debug_draw(draw_options)

        # Rafraîchissement de l'écran
        pygame.display.flip()

        dt = clock.tick(60) / 1000  # secondes


if __name__ == "__main__":
    main()
