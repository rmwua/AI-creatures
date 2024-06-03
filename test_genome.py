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
        print(spec)
        print(gene)
        print(gene[spec["link-length"]["ind"]])
        self.assertGreater(gene[spec["link-length"]["ind"]], 0)


unittest.main()
