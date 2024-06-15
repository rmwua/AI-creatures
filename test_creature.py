import unittest
import creature
import pybullet as p
import genome


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

    def test_radial(self):
        links = [
            genome.URDFLink(name="A", parent_name="None", recur=1),
            genome.URDFLink(name="B", parent_name="A", recur=2, joint_origin_rpy_1=0.75, link_length=1),
        ]
        c = creature.Creature(gene_count=2)
        c.flat_links = links
        c.get_expanded_links()
        xml_str = c.to_xml()
        with open('103.urdf', 'w') as f:
            f.write('<?xml version="1.0"?>' + "\n" + xml_str)

    def test_motor(self):
        m = creature.Motor(0.1, 0.5, 0.5)
        self.assertIsNotNone(m)

    def test_motor_val(self):
        m = creature.Motor(0.1, 0.5, 0.5)
        self.assertEqual(m.get_output(), 1)

    def test_motor_val2(self):
        m = creature.Motor(0.6, 0.5, 0.5)
        m.get_output()
        m.get_output()
        self.assertGreater(m.get_output(), 0)

    def test_c_mot(self):
        c = creature.Creature(gene_count=4)
        ls = c.get_expanded_links()
        ms = c.get_motors()
        self.assertEqual(len(ls) - 1, len(ms))

    def testDist(self):
        c = creature.Creature(3)
        c.update_position((0, 0, 0))
        d1 = c.get_distance_travelled()
        c.update_position((1, 1, 1))
        d2 = c.get_distance_travelled()
        self.assertGreater(d2, d1)


unittest.main()

