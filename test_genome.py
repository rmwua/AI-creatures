import unittest
import genome
import numpy as np


class GenomeTest(unittest.TestCase):
    def test_class_exists(self):
        self.assertIsNotNone(genome.Genome)

    def test_random_gene(self):
        self.assertIsNotNone(genome.Genome.get_random_gene(5))

    def test_randon_gene_not_none(self):
        self.assertIsNotNone(genome.Genome.get_random_gene(5))

    def test_randon_gene_has_values(self):
        gene = genome.Genome.get_random_gene(5)
        self.assertIsNotNone(gene[0])

    def test_randon_gene_length(self):
        gene = genome.Genome.get_random_gene(20)
        self.assertEqual(len(gene), 20)

    def test_randon_gene_is_numpy_array(self):
        gene = genome.Genome.get_random_gene(20)
        self.assertEqual(type(gene), np.ndarray)

    def test_randon_genome_exists(self):
        data = genome.Genome.get_random_genome(20, 5)
        self.assertIsNotNone(data)

    def test_gene_spec_exists(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec)

    def test_gene_spec_has_link_length(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec["link-length"])

    def testGeneSpecScale(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(20)
        self.assertGreater(gene[spec["link-length"]["ind"]], 0)

    def test_gene_to_gene_dict(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(len(spec))
        gene_dict = genome.Genome.get_gene_dict(gene, spec)
        self.assertIn("link-recurrence", gene_dict)

    def test_genome_to_dict(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        self.assertEqual(len(genome_dicts), 3)

    def test_flat_links(self):
        links = [
            genome.URDFLink(name="A", parent_name=None, recur=1),
            genome.URDFLink(name="B", parent_name="A", recur=1),
            genome.URDFLink(name="C", parent_name="B", recur=2),
            genome.URDFLink(name="D", parent_name="C", recur=1),
        ]
        self.assertIsNotNone(links)

    def test_expand_links_1(self):
        links = [
            genome.URDFLink(name="A", parent_name="None", recur=1),
            genome.URDFLink(name="B", parent_name="A", recur=2),
        ]
        exp_links = [links[0]]
        genome.Genome.expand_links(links[0], links[0].name, links, exp_links)
        self.assertEqual(len(exp_links), 3)

    def test_expand_links_2(self):
        links = [
            genome.URDFLink(name="A", parent_name="None", recur=1),
            genome.URDFLink(name="B", parent_name="A", recur=1),
            genome.URDFLink(name="C", parent_name="B", recur=2),
            genome.URDFLink(name="D", parent_name="C", recur=1),
        ]
        exp_links = [links[0]]
        genome.Genome.expand_links(links[0], links[0].name, links, exp_links)
        self.assertEqual(len(exp_links), 6)

    def test_get_links(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        links = genome.Genome.genome_to_links(genome_dicts)
        self.assertEqual(len(links), 3)

    def test_get_links_unique_names(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        gdicts = genome.Genome.get_genome_dicts(dna, spec)
        links = genome.Genome.genome_to_links(gdicts)
        # check that each link's name only appears once
        for l in links:
            # print(l)
            names = [link.name for link in links if link.name == l.name]
            self.assertEqual(len(names), 1)

    def testCrossover(self):
        g1 = [[1], [2], [3]]
        g2 = [[4], [5], [6]]
        g3 = []
        for i in range(10):
            g3 = genome.Genome.crossover(g1, g2)
        self.assertGreater(len(g3), 0)

    def test_point(self):
        g1 = np.array([[1.0], [2.0], [3.0]])
        g2 = genome.Genome.point_mutate(g1, rate=1, amount=0.25)
        self.assertFalse(np.array_equal(g1, g2))

    def test_point_range(self):
        g1 = np.array([[1.0], [0.0], [1.0], [0.0]])
        for i in range(100):
            g2 = genome.Genome.point_mutate(g1, rate=1, amount=0.25)
            self.assertLess(np.max(g2), 1.0)
            self.assertGreaterEqual(np.min(g2), 0.0)

    def test_shrink(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.shrink_mutate(g1, rate=1.0)
        # should def. shrink as rate = 1
        self.assertEqual(len(g2), 1)

    def test_shrink2(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.shrink_mutate(g1, rate=0.0)
        # should not shrink as rate = 0
        self.assertEqual(len(g2), 2)

    def test_shrink3(self):
        g1 = np.array([[1.0]])
        g2 = genome.Genome.shrink_mutate(g1, rate=1.0)
        # should not shrink if already len 1
        self.assertEqual(len(g2), 1)

    def test_grow1(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.grow_mutate(g1, rate=1)
        self.assertGreater(len(g2), len(g1))

    def test_grow2(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.grow_mutate(g1, rate=0)
        self.assertEqual(len(g2), len(g1))


unittest.main()

