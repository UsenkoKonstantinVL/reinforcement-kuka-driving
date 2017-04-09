import vrep
import vrepConst

class robot:
    def __init__(self, IP='127.0.0.1', PORT=7777):
        self.id = -1
        self.PORT = PORT
        self.IP = IP

        self.drivers_dict = {}
        self.drivers_list = []

    def initialize(self):
        if self.id != -1:
            for val in self.drivers_list:
                joint = vrep.simxGetObjectHandle(self.id, val, vrepConst.simx_opmode_oneshot_wait)
                self.drivers_dict.setdefault(val, joint)

    def setVelocity(self, list_vel):
        if self.id != -1:
            for i, val in enumerate(self.drivers_list):
                res = vrep.simxSetJointTargetVelocity(self.id, self.drivers_dict[val], list_vel[i],
                                                      vrepConst.simx_opmode_oneshot_wait)

    def start_simulation(self):
        self.id = vrep.simxStart(self.IP, self.PORT, True, True, 5000, 5)


    def finish_simulation(self):

        if self.id != -1:
            vrep.simxFinish(self.id)
