import klampt
from klampt.plan.robotcspace import RobotCSpace
from klampt.plan import cspace
from klampt.model import collide

world = klampt.WorldModel()
# ... set up world ...
# robot = world.robot(0)
# space = RobotCSpace(robot,collide.WorldCollider(world))
# # (Can also create it without the collider to ignore all self-and environment collisions)
# #Optionally:
# #Call space.addFeasibilityTest(func,name=None) on the space with as many additional feasibility tests as you want
# qinit = robot.getConfig()
# qgoal = robot.getConfig()
# qgoal[3] += 2.0       #move 2 radians on joint 3