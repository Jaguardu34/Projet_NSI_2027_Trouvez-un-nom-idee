import pygame
import pymunk
import pymunk.pygame_util
from entity import ball
from entity import segment as seg

# Before you can do much with pygame, you will need to initialize it
pygame.init()
# Init de clock
clock = pygame.time.Clock()

CIEL = 0, 200, 255  # parenthèses inutiles, l'interpréteur reconnaît un tuple

debug = True


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

    # b_arm1 ancré au monde mais reste dynamique (peut tourner)
    b_arm1 = pymunk.Body(1, pymunk.moment_for_segment(10, (0, 0), (100, 0), 4))
    b_arm1.position = 400, 100
    arm1_shape = pymunk.Segment(b_arm1, (0, 0), (100, 0), 4)

    # Pivot fixe à l'épaule
    shoulder = pymunk.PivotJoint(space.static_body, b_arm1, (400, 100))
    space.add(shoulder)

    # b_arm2 entièrement dynamique
    b_arm2 = pymunk.Body(10, pymunk.moment_for_segment(1, (0, 0), (100, 0), 4))
    b_arm2.position = 510, 120
    arm2_shape = pymunk.Segment(b_arm2, (0, 0), (0, 100), 4)

    # Pivot à l'articulation (coude)
    elbow = pymunk.PivotJoint(b_arm1, b_arm2, (510, 110))
    elbow_max = pymunk.RotaryLimitJoint(b_arm1, b_arm2, -1.5, 1.5)
    space.add(elbow, elbow_max)

    muscle_up2 = True
    muscle_lenght2 = 100
    # Muscle entre les deux corps
    muscle2 = pymunk.DampedSpring(
        b_arm1, b_arm2, (20, 0), (-4, 20), muscle_lenght2, 10000, 200
    )
    space.add(b_arm1, arm1_shape, b_arm2, arm2_shape, muscle2)

    # loop
    loop = True

    space.iterations = 30  # default = 10

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        # Superposition du fond ciel
        screen.fill("gray")  # Efface l'écran

        if muscle_up2:
            muscle_lenght2 += 0.5
        else:
            muscle_lenght2 -= 0.5

        if muscle_lenght2 <= 60:
            muscle_up2 = True
        elif muscle_lenght2 >= 120:
            muscle_up2 = False

        print(muscle_lenght2)

        muscle2.rest_length = muscle_lenght2

        steps = 10
        for _ in range(steps):
            space.step(0.001 / steps)

        space.debug_draw(draw_options)

        # Rafraîchissement de l'écran
        pygame.display.flip()

        dt = clock.tick(60) / 1000  # secondes


if __name__ == "__main__":
    main()
