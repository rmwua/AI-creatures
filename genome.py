import copy
import numpy as np


class Genome:
    @staticmethod
    def get_random_gene(length):
        gene = np.array([np.random.random() for _ in range(length)])
        return gene

    @staticmethod
    def get_random_genome(gene_length, gene_count):
        genome = [Genome.get_random_gene(gene_length) for _ in range(gene_count)]
        return genome

    @staticmethod
    def get_gene_spec():
        gene_spec = {"link-shape": {"scale": 1},
                     "link-length": {"scale": 1},
                     "link-radius": {"scale": 1},
                     "link-recurrence": {"scale": 4},
                     "link-mass": {"scale": 1},
                     "joint-type": {"scale": 1},
                     "joint-parent": {"scale": 1},
                     "joint-axis-xyz": {"scale": 1},
                     "joint-origin-rpy-1": {"scale": np.pi * 2},
                     "joint-origin-rpy-2": {"scale": np.pi * 2},
                     "joint-origin-rpy-3": {"scale": np.pi * 2},
                     "joint-origin-xyz-1": {"scale": 1},
                     "joint-origin-xyz-2": {"scale": 1},
                     "joint-origin-xyz-3": {"scale": 1},
                     "control-waveform": {"scale": 1},
                     "control-amp": {"scale": 0.25},
                     "control-freq": {"scale": 1}
                     }

        ind = 0
        for key in gene_spec.keys():
            gene_spec[key]["ind"] = ind
            ind = ind + 1
        return gene_spec

    @staticmethod
    def get_gene_dict(gene, spec):
        gene_dict = {}
        for key in spec:
            ind = spec[key]["ind"]
            scale = spec[key]["scale"]
            gene_dict[key] = gene[ind] * scale
        return gene_dict

    @staticmethod
    def get_genome_dicts(genome, spec):
        genome_dicts = [Genome.get_gene_dict(genome[i], spec) for i in range(len(genome))]
        return genome_dicts

    @staticmethod
    def expand_links(parent_link, uniq_parent_name, flat_links, exp_links):
        children = [child for child in flat_links if child.parent_name == parent_link.name]
        for child in children:
            for recur in range(int(child.recur)):
                c_copy = copy.copy(child)
                c_copy.parent_name = uniq_parent_name
                uniq_name = c_copy.name + str(len(exp_links))
                c_copy.name = uniq_name
                exp_links.append(c_copy)
                Genome.expand_links(child, uniq_name, flat_links, exp_links)

    @staticmethod
    def genome_to_links(gdicts):
        link_ind = 0
        parent_names = [str(link_ind)]
        links = []
        for gdict in gdicts:
            link_name = str(link_ind)
            parent_ind = gdict["joint-parent"] * len(parent_names)
            # print("parent_ind="+str(parent_ind))
            parent_name = parent_names[int(parent_ind)]
            # print("available parents: ", parent_names, "chose", parent_name)
            recur = gdict["link-recurrence"]
            link = URDFLink(name=link_name,
                            parent_name=parent_name,
                            recur=recur+2,
                            link_length=gdict["link-length"],
                            link_radius=gdict["link-radius"],
                            link_mass=gdict["link-mass"],
                            joint_type=gdict["joint-type"],
                            joint_parent=gdict["joint-parent"],
                            joint_axis_xyz=gdict["joint-axis-xyz"],
                            joint_origin_rpy_1=gdict["joint-origin-rpy-1"],
                            joint_origin_rpy_2=gdict["joint-origin-rpy-2"],
                            joint_origin_rpy_3=gdict["joint-origin-rpy-3"],
                            joint_origin_xyz_1=gdict["joint-origin-xyz-1"],
                            joint_origin_xyz_2=gdict["joint-origin-xyz-2"],
                            joint_origin_xyz_3=gdict["joint-origin-xyz-3"],
                            control_waveform=gdict["control-waveform"],
                            control_amp=gdict["control-amp"],
                            control_freq=gdict["control-freq"]
                            )
            links.append(link)
            if link_ind != 0:# don't re-add the first link
                parent_names.append(link_name)
            link_ind += 1
        # now just fix the first link, so it links to nothing
        links[0].parent_name = "None"
        return links


class URDFLink:
    def __init__(self, name, parent_name, recur,
                 link_length=0.1,
                 link_shape=0.1,
                 link_radius=0.1,
                 link_mass=0.1,
                 joint_type=0.1,
                 joint_parent=0.1,
                 joint_axis_xyz=0.1,
                 joint_origin_rpy_1=0.1,
                 joint_origin_rpy_2=0.1,
                 joint_origin_rpy_3=0.1,
                 joint_origin_xyz_1=0.1,
                 joint_origin_xyz_2=0.1,
                 joint_origin_xyz_3=0.1,
                 control_waveform=0.1,
                 control_amp=0.1,
                 control_freq=0.1
                 ):
        self.name = name
        self.parent_name = parent_name
        self.recur = recur
        self.link_length = link_length
        self.link_shape = link_shape
        self.link_radius = link_radius
        self.link_mass = link_mass
        self.joint_type = joint_type
        self.joint_parent = joint_parent
        self.joint_axis_xyz = joint_axis_xyz
        self.joint_origin_rpy_1 = joint_origin_rpy_1
        self.joint_origin_rpy_2 = joint_origin_rpy_2
        self.joint_origin_rpy_3 = joint_origin_rpy_3
        self.joint_origin_xyz_1 = joint_origin_xyz_1
        self.joint_origin_xyz_2 = joint_origin_xyz_2
        self.joint_origin_xyz_3 = joint_origin_xyz_3
        self.control_waveform = control_waveform
        self.control_amp = control_amp
        self.control_freq = control_freq

    def __str__(self):
        return str(
            "name=" + str(self.name) + "\n" \
            "parent_name=" + str(self.parent_name) + "\n"\
            "joint_parent=" + str(self.joint_parent) + "\n")
