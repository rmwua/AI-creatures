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

    def to_link_element(self, adom):
        #         <link name="base_link">
        #     <visual>
        #       <geometry>
        #         <cylinder length="0.6" radius="0.25"/>
        #       </geometry>
        #     </visual>
        #     <collision>
        #       <geometry>
        #         <cylinder length="0.6" radius="0.25"/>
        #       </geometry>
        #     </collision>
        #     <inertial>
        # 	    <mass value="0.25"/>
        # 	    <inertia ixx="0.0003" iyy="0.0003" izz="0.0003" ixy="0" ixz="0" iyz="0"/>
        #     </inertial>
        #   </link>

        # visual tag
        link_tag = adom.createElement("link")
        link_tag.setAttribute("name", self.name)
        vis_tag = adom.createElement("visual")
        geom_tag = adom.createElement("geometry")
        cyl_tag = adom.createElement("cylinder")
        cyl_tag.setAttribute("length", str(self.link_length))
        cyl_tag.setAttribute("radius", str(self.link_radius))
        # append children to visual
        geom_tag.appendChild(cyl_tag)
        vis_tag.appendChild(geom_tag)
        # collision tag
        coll_tag = adom.createElement("collision")
        c_geom_tag = adom.createElement("geometry")
        c_cyl_tag = adom.createElement("cylinder")
        c_cyl_tag.setAttribute("length", str(self.link_length))
        c_cyl_tag.setAttribute("radius", str(self.link_radius))
        # append children to collision
        c_geom_tag.appendChild(c_cyl_tag)
        coll_tag.appendChild(c_geom_tag)
        # inertial tag
        inertial_tag = adom.createElement("inertial")
        mass_tag = adom.createElement("mass")
        mass = np.pi * (self.link_radius * self.link_radius) * self.link_length
        mass_tag.setAttribute("value", str(mass))
        inertia_tag = adom.createElement("inertia")
        inertia_tag.setAttribute("ixx", "0.03")
        inertia_tag.setAttribute("iyy", "0.03")
        inertia_tag.setAttribute("izz", "0.03")
        inertia_tag.setAttribute("ixy", "0")
        inertia_tag.setAttribute("ixz", "0")
        inertia_tag.setAttribute("iyx", "0")
        # append children to inertial
        inertial_tag.appendChild(mass_tag)
        inertial_tag.appendChild(inertia_tag)
        # append children to link
        link_tag.appendChild(vis_tag)
        link_tag.appendChild(coll_tag)
        link_tag.appendChild(inertial_tag)

        return link_tag

    def to_joint_element(self, adom):
        #           <joint name="base_to_sub2" type="revolute">
        #     <parent link="base_link"/>
        #     <child link="sub_link2"/>
        #     <axis xyz="1 0 0"/>
        #     <limit effort="10" upper="0" lower="10" velocity="1"/>
        #     <origin rpy="0 0 0" xyz="0 0.5 0"/>
        #   </joint>
        joint_tag = adom.createElement("joint")
        joint_tag.setAttribute("name", self.name + "_to_" + self.parent_name)
        joint_tag.setAttribute("type", "revolute")
        parent_tag = adom.createElement("parent")
        parent_tag.setAttribute("link", self.parent_name)
        child_tag = adom.createElement("child")
        child_tag.setAttribute("link", self.name)
        axis_tag = adom.createElement("axis")
        axis_tag.setAttribute("xyz", "1 0 0")
        if 0.33 < self.joint_axis_xyz <= 0.66:
            axis_tag.setAttribute("xyz", "0 1 0")
        if self.joint_axis_xyz > 0.66:
            axis_tag.setAttribute("xyz", "0 0 1")

        limit_tag = adom.createElement("limit")
        # effort upper lower velocity
        limit_tag.setAttribute("effort", "1")
        limit_tag.setAttribute("upper", "-3.1415")
        limit_tag.setAttribute("lower", "3.1415")
        limit_tag.setAttribute("velocity", "1")
        # <origin rpy="0 0 0" xyz="0 0.5 0"/>
        orig_tag = adom.createElement("origin")
        rpy = str(self.joint_origin_rpy_1) + " " + str(self.joint_origin_rpy_2) + " " + str(self.joint_origin_rpy_3)
        orig_tag.setAttribute("rpy", rpy)
        xyz = str(self.joint_origin_xyz_1) + " " + str(self.joint_origin_xyz_2) + " " + str(self.joint_origin_xyz_3)
        orig_tag.setAttribute("xyz", xyz)
        # append children
        joint_tag.appendChild(parent_tag)
        joint_tag.appendChild(child_tag)
        joint_tag.appendChild(axis_tag)
        joint_tag.appendChild(limit_tag)
        joint_tag.appendChild(orig_tag)
        return joint_tag

