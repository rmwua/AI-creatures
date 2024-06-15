import numpy as np

import creature


class Population:
    def __init__(self, pop_size: int, gene_count: int) -> None:
        self.creatures = [creature.Creature(gene_count=gene_count) for _ in range(pop_size)]

    @staticmethod
    def get_fitness_map(fits: list) -> list:
        total = 0
        fitmap = []
        for fit in fits:
            total += fit
            fitmap.append(total)
        return fitmap

    @staticmethod
    def select_parent(fitmap: list) -> int:
        """
        Wheel for selecting parent
        Generates a random number, which is then compared to the numbers in fitmap
        :param fitmap: List
        :return: int
        """
        r = np.random.rand()  # 0-1
        r = r * fitmap[-1]
        for i in range(len(fitmap)):
            if r <= fitmap[i]:
                return i
