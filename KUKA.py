import vrep
import vrepConst
import time
from time import sleep

class robot:
    def __init__(self, IP='127.0.0.1', PORT=7777):
        self.id = -1
        self.PORT = PORT
        self.IP = IP

        self.obj = 0
        self.obj_name = 'youBot_ref'
        self.cord = 0
        self.drivers_dict = {}
        self.drivers_list = ['rollingJoint_fl',
                             'rollingJoint_fr',
                             'rollingJoint_rl',
                             'rollingJoint_rr']
        self.tube_name = 'HokuyoData'

    def initialize(self):
        self.obj = vrep.simxGetObjectHandle(self.id, self.obj_name, vrepConst.simx_opmode_oneshot_wait)[1]
        if self.id != -1:
            for val in self.drivers_list:
                joint = vrep.simxGetObjectHandle(self.id, val, vrepConst.simx_opmode_oneshot_wait)[1]
                self.drivers_dict.setdefault(val, joint)

    def setVelocity(self, list_vel):
        if self.id != -1:
            for i, val in enumerate(self.drivers_list):
                res = vrep.simxSetJointTargetVelocity(self.id, self.drivers_dict[val], list_vel[i],
                                                      vrepConst.simx_opmode_oneshot_wait)

    def setVelocityVect(self, vel, rot, bvel):
        print('')

        SPEED = 4
        ROTATE = 2
        MOV = 1

        vel *= SPEED
        rot *= ROTATE
        bvel *= MOV
        # speed = speed * SPEEDC;
        # rotation = rotation * ROTATIONC;
        # move = move * MOVEC;
        # Move(speed - rotation + move, speed + rotation - move, speed - rotation - move, speed + rotation + move);
        list_vel = [vel - rot + bvel,
                vel + rot - bvel,
                vel - rot - bvel,
                vel + rot + bvel]
        self.setVelocity(list_vel)

    def getLaserPoints(self):
        if self.id != -1:
            res = vrep.simxGetStringSignal(self.id, self.tube_name, vrepConst.simx_opmode_streaming)
            time.sleep(1)
            res = vrep.simxGetStringSignal(self.id, self.tube_name, vrepConst.simx_opmode_buffer)
            r = vrep.simxUnpackFloats(res[1])
            return r

    def unpack(self, list):
        j = 0
        list_obst = []
        obs = []
        for i in list:
            obs.append(i)
            j += 1
            if j == 3:
                j = 0
                list_obst.append(obs)
                obs = []
        return list_obst

    def unpack(self):
        list = self.getLaserPoints()
        j = 0
        list_obst = []
        obs = []
        for i in list:
            obs.append(i)
            j += 1
            if j == 3:
                j = 0
                list_obst.append(obs)
                obs = []
        return list_obst

    def get_segment(self):
        list_of_points = self.unpack()



    def getCoordinate(self):
        res = []

        if self.id != -1:
            #function are simx_opmode_streaming (the first call) and simx_opmode_buffer (the following calls)
            res = vrep.simxGetObjectPosition(self.id, self.obj, -1, vrepConst.simx_opmode_streaming)
            sleep(0.5)
            res = vrep.simxGetObjectPosition(self.id, self.obj, -1, vrepConst.simx_opmode_buffer)
        # self.cord += 1

        return res[1]

    def start_simulation(self):
        self.id = vrep.simxStart(self.IP, self.PORT, True, True, 5000, 5)

    def finish_simulation(self):

        if self.id != -1:
            vrep.simxFinish(self.id)
