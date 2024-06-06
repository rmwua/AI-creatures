import unittest
import creature
import pybullet as p

class TestCreature(unittest.TestCase):
    def test_creat_exists(self):
        self.assertIsNotNone(creature.Creature)

    def test_creature_get_flat_links(self):
        c = creature.Creature(gene_count=4)
        links = c.get_flat_links()
        self.assertEqual(len(links), 4)

    def test_exp_links(self):
        c = creature.Creature(gene_count=25)
        links = c.get_flat_links()
        exp_links = c.get_expanded_links()
        self.assertGreaterEqual(len(exp_links), len(links))

    def test_link_to_xml(self):
        c = creature.Creature(gene_count=2)
        xml_str = c.to_xml()
        self.assertIsNotNone(xml_str)

    def testLoadXML(self):
        c = creature.Creature(gene_count=2)
        xml_str = c.to_xml()
        with open('test.urdf', 'w') as f:
            f.write(xml_str)
        p.connect(p.DIRECT)
        cid = p.loadURDF('test.urdf')
        self.assertIsNotNone(cid)


unittest.main()

