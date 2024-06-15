import unittest

import numpy as np

import population
import simulation
import genome
import creature


class TestGA(unittest.TestCase):
    def testBasicGA(self):
        def testBasicGA(self):
            pop = population.Population(pop_size=10,
                                        gene_count=3)
            # sim = simulation.ThreadedSim(pool_size=1)
            sim = simulation.Simulation()

            for iteration in range(1000):
                sim.eval_population(pop, 2400)
                fits = [cr.get_distance_travelled()
                        for cr in pop.creatures]
                links = [len(cr.get_expanded_links())
                         for cr in pop.creatures]
                print(iteration, "fittest:", np.round(np.max(fits), 3),
                      "mean:", np.round(np.mean(fits), 3), "mean links", np.round(np.mean(links)), "max links",
                      np.round(np.max(links)))
                fit_map = population.Population.get_fitness_map(fits)
                new_creatures = []
                for i in range(len(pop.creatures)):
                    p1_ind = population.Population.select_parent(fit_map)
                    p2_ind = population.Population.select_parent(fit_map)
                    p1 = pop.creatures[p1_ind]
                    p2 = pop.creatures[p2_ind]
                    # now we have the parents!
                    dna = genome.Genome.crossover(p1.dna, p2.dna)
                    dna = genome.Genome.point_mutate(dna, rate=0.1, amount=0.25)
                    dna = genome.Genome.shrink_mutate(dna, rate=0.25)
                    dna = genome.Genome.grow_mutate(dna, rate=0.1)
                    cr = creature.Creature(1)
                    cr.update_dna(dna)
                    new_creatures.append(cr)

unittest.main()
