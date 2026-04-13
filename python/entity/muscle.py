import math

import pymunk


class Muscle:
    def __init__(
        self,
        body_1: pymunk.Body,
        body_2: pymunk.Body,
        offset_1: tuple[int, int],
        offset_2: tuple[int, int],
        space: pymunk.Space,
    ):
        self.body_1 = body_1
        self.body_2 = body_2
        self.offset_1 = offset_1
        self.offset_2 = offset_2
        self.strenght = self.get_lenght
        self.muscle_spring = pymunk.DampedSpring(
            body_1, body_2, offset_1, offset_2, self.strenght, 10000, 200
        )
        self.contract = False
        space.add(self.muscle_spring)

    @property
    def get_lenght(self):
        # Convertit les ancres en coordonnées monde
        pa = self.body_1.local_to_world(self.offset_1)
        pb = self.body_1.local_to_world(self.offset_2)
        return math.dist(pa, pb)

    def update(self, contract: bool, lenght=0):
        current_lenght = self.get_lenght
        self.contract = contract
        if self.contract and current_lenght > lenght:
            # Phase contraction : tire activement
            self.muscle_spring.stiffness = 10000
            self.muscle_spring.rest_length = lenght
        elif not contract:
            # Phase relâche : aucune force peu importe la distance
            self.muscle_spring.stiffness = 0
            self.muscle_spring.rest_length = current_lenght
