import unittest
import population
import simulation


class TestGA(unittest.TestCase):
    def testBasicGA(self):
        pop = population.Population(pop_size=10,
                                    gene_count=3)
        # sim = simulation.ThreadedSim(pool_size=4)
        sim = simulation.Simulation()
        sim.eval_population(pop, 2400)
        fits = [cr.get_distance_travelled()
                for cr in pop.creatures]
        self.assertNotEqual(fits[0], 0)
        #select the parents
        fits = [cr.get_distance_travelled() for cr in pop.creatures]
        fit_map = population.Population.get_fitness_map(fits)
        new_creatures = []
        for i in range(len(pop.creatures)):
            p1_ind = population.Population.select_parent(fit_map)
            p2_ind = population.Population.select_parent(fit_map)
            p1 = pop.creatures[p1_ind]
            p2 = pop.creatures[p2_ind]

        self.assertIsNotNone(p1)
        self.assertIsNotNone(p2)


unittest.main()
