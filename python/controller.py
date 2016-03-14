import random
from util import *

"""
Raise this exception when exploration is over
"""
class ResetException(Exception):
    pass

"""
Controller (base)
"""
class Controller(object):
    def __init__(self):
        self.resetAtGoal = True

    # this is called every step in the first run
    def explore(self, robot):
        return (Steering.F, 1)

    # this is called every step in the second run
    def exploit(self, robot):
        return self.explore(robot)

    # for priting the class name
    def __str__(self):
        tokens = self.__class__.__name__.split('_')
        return tokens[1] if len(tokens)>1 else 'Base'

"""
Controller Random
- randomly move to where it has no wall
- at dead-end, it turns left or right 
"""
class Controller_Random(Controller):
    def explore(self, robot):
        sensor = robot.sensor
        if sensor.isDeadEnd():
            # randomly turn at dead end
            steering = random.choice([Steering.L, Steering.R])
            movement = 0
        else:
            # randomly choose available steering direction
            steering = random.choice([s for s in Steering if sensor.distance(s)>0])
            movement = 1
        return (steering, movement)

"""
Controller that detects dead ends
"""
class Controller_DeadEnd(Controller):
    def explore(self, robot):
        heading = robot.heading
        sensor = robot.sensor
        deadEnds = robot.deadEnds
        if deadEnds.isDeadEnd(heading):
            # back off at dead end
            steering = Steering.F
            movement = -1
        else:
            # randomly choose available steering direction
            steering = random.choice([s for s in Steering if sensor.distance(s)>0])
            movement = 1
        return (steering, movement)

"""
Controller that keep tracks how often each cell is visited
"""
class Controller_Counter(Controller):
    def explore(self, robot):
        heading = robot.heading
        sensor = robot.sensor
        counter = robot.counter
        deadEnds = robot.deadEnds
        if deadEnds.isDeadEnd(heading):
            # back off at dead end
            steering = Steering.F
            movement = -1
        else:
            counts = []
            for s in Steering:
                if sensor.distance(s)>0:
                    location = heading.adjust(s,1).location
                    c = counter.getValue(location)
                    counts.append((c, s.value))
            counts.sort()
            steering = Steering(counts[0][1])
            movement = 1
        return (steering, movement)

"""
Controller that uses Heuristic value to choose a path
"""
class Controller_Heuristic(Controller):
    def explore(self, robot):
        heading = robot.heading
        sensor = robot.sensor
        counter = robot.counter
        deadEnds = robot.deadEnds
        heuristic = robot.heuristic
        if deadEnds.isDeadEnd(heading):
            # back off at dead end
            steering = Steering.F
            movement = -1
        else:
            counts = []
            for s in Steering:
                if sensor.distance(s)>0:
                    location = heading.adjust(s,1).location
                    c = counter.getValue(location)
                    h = heuristic.getValue(location)
                    counts.append((c, h, s.value))
            counts.sort()
            steering = Steering(counts[0][2])
            movement = 1
        return (steering, movement)
