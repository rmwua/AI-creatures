import numpy as np
import pybullet as p
import pybullet_data as pd
import creature
import genome
import time
import random

## ... usual starter code to create a sim and floor
p.connect(p.DIRECT)
p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0, 0, -10)

# generate a random creature
c = creature.Creature(gene_count=5)
# save it to XML
with open('test.urdf', 'w') as f:
    c.get_expanded_links()
    f.write(c.to_xml())
# load it to the simulation
rob1 = p.loadURDF('test.urdf')
start_pos, ori = p.getBasePositionAndOrientation(rob1)

#iterate
step = 0
frame_counter = 0
total_frames = 2400  # at 240Hz, that's 10 seconds
for frame in range(total_frames):
    p.stepSimulation()
    if frame % 24 == 0:
        step += 1
        if step % 120 == 0:
            motors = c.get_motors()
            assert len(motors) == p.getNumJoints(rob1), "bad motors!"
            for jid in range(p.getNumJoints(rob1)):
                mode = p.VELOCITY_CONTROL
                vel = 5 * (random.random() - 0.5)
                p.setJointMotorControl2(rob1,
                                        jid,
                                        controlMode=mode,
                                        targetVelocity=vel)
        new_pos, orn = p.getBasePositionAndOrientation(rob1)
        dist_moved = np.linalg.norm(np.asarray(start_pos) - np.asarray(new_pos))
        print(dist_moved)

    # time.sleep(1.0/240)
