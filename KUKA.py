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
        self.obj_name = 'Dummy'#'youBot_ref'
        self.cord = 0
        self.drivers_dict = {}
        self.drivers_list = ['rollingJoint_fl',
                             'rollingJoint_fr',
                             'rollingJoint_rl',
                             'rollingJoint_rr']
        self.tube_name = 'HokuyoData'
        self.init_pos = []
        self.first_call = True
        self.sec_first_call = True
        self.sim_first_call = True

    def initialize(self):
        self.obj = vrep.simxGetObjectHandle(self.id, self.obj_name, vrepConst.simx_opmode_oneshot_wait)[1]
        if self.id != -1:
            for val in self.drivers_list:
                joint = vrep.simxGetObjectHandle(self.id, val, vrepConst.simx_opmode_oneshot_wait)[1]
                self.drivers_dict.setdefault(val, joint)
                # self.get_rob_pos()
                # self.get_rob_pos()

    def get_rob_pos(self):
        if self.id != -1:
            if self.first_call:
                mode = vrepConst.simx_opmode_streaming
            else:
                mode = vrepConst.simx_opmode_buffer
            joint = vrep.simxGetObjectHandle(self.id, 'youBot', vrepConst.simx_opmode_oneshot_wait)[1]
            err, self.init_pos = vrep.simxGetObjectPosition(self.id, joint, -1, mode)
            print()

    def setVelocity(self, list_vel):
        if self.id != -1:
            for i, val in enumerate(self.drivers_list):
                res = vrep.simxSetJointTargetVelocity(self.id, self.drivers_dict[val], list_vel[i],
                                                      vrepConst.simx_opmode_oneshot_wait)

    def restartscene(self):
        vrep.simxStopSimulation(self.id, vrepConst.simx_opmode_oneshot)

        vrep.simxStartSimulation(self.id, vrepConst.simx_opmode_oneshot)


    def setVelocityVect(self, vel, rot, bvel):
        #print('')

        SPEED = 2
        ROTATE = 1
        MOV = 0.5

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
            if self.sec_first_call:
                mode = vrepConst.simx_opmode_streaming
                res = vrep.simxGetStringSignal(self.id, self.tube_name, vrepConst.simx_opmode_streaming)
                time.sleep(0.05)
                self.sec_first_call = False

            else:
                mode = vrepConst.simx_opmode_buffer

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

    def check_collision(self):
        if self.id != -1:

            mode = 0
            if self.sim_first_call:
                mode = vrepConst.simx_opmode_streaming
            else:
                mode = vrepConst.simx_opmode_buffer
            res = vrep.simxGetIntegerSignal(self.id, 'collision_detection', mode)
            time.sleep(0.03)
            self.sim_first_call = False
            return res[1]

    def getCoordinate(self):
        res = []

        if self.id != -1:
            #function are simx_opmode_streaming (the first call) and simx_opmode_buffer (the following calls)
            res = vrep.simxGetObjectPosition(self.id, self.obj, -1, vrepConst.simx_opmode_streaming)
            sleep(0.05)
            res = vrep.simxGetObjectPosition(self.id, self.obj, -1, vrepConst.simx_opmode_buffer)
        # self.cord += 1

        return res[1]

    def set_init_coordinate(self):
        if self.id != -1:
            joint = vrep.simxGetObjectHandle(self.id, 'youBot', vrepConst.simx_opmode_oneshot_wait)[1]
            err = vrep.simxSetObjectPosition(self.id, joint, -1, self.init_pos, vrepConst.simx_opmode_oneshot)


    def get_orientation(self):
        res = [0, 0, 0]

        if(self.id != -1):
            res = vrep.simxGetObjectOrientation(self.id, self.obj, -1, vrepConst.simx_opmode_streaming)
            sleep(0.5)
            res = vrep.simxGetObjectOrientation(self.id, self.obj, -1, vrepConst.simx_opmode_buffer)
        return res[1][2]

    def start_simulation(self):
        self.id = vrep.simxStart(self.IP, self.PORT, True, True, 5000, 5)

    def finish_simulation(self):

        if self.id != -1:
            vrep.simxFinish(self.id)
