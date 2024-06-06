import pybullet as p
import pybullet_data as pd
import creature
import genome
import time
import random

p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0, 0, -10)

c = creature.Creature(gene_count=5)

with open('test.urdf', 'w') as f:
    c.get_expanded_links()
    f.write(c.to_xml())

cid = p.loadURDF('test.urdf')
p.setRealTimeSimulation(1)

# while True:
#     for jid in range(p.getNumJoints(cid)):
#         m = c.get_motors()[jid]
#         p.setJointMotorControl2(cid, jid,
#                                 controlMode=p.VELOCITY_CONTROL,
#                                 targetVelocity=5)
#     time.sleep(0.1)
step = 0
while True:
    p.stepSimulation()
    step += 1
    if step % 120 == 0:
        motors = c.get_motors()
        assert len(motors) == p.getNumJoints(cid), "bad motors!"
        for jid in range(p.getNumJoints(cid)):
            mode = p.VELOCITY_CONTROL
            vel = 5 * (random.random() - 0.5)
            p.setJointMotorControl2(cid,
                                    jid,
                                    controlMode=mode,
                                    targetVelocity=vel)
    time.sleep(1.0/240)