import math
from utils.operation import angle_mod, rot_mat_to_yaw
from state import State

class State:
    def __init__(self, pos, ori, speed):
        self.init(pos, ori, speed)

    def set_state(self, pos, ori, speed):
        self.__x = pos[0]                 # [m]
        self.__y = pos[1]                 # [m]
        self.__yaw = rot_mat_to_yaw(ori)  # [rad] 0 ~ 2pi
        self.__v = speed                  # [m/s]

    def update(self, acceletation, delta):
        self.__x += self.__v * math.cos(self.__yaw) * self.dt
        self.__y += self.__v * math.sin(self.__yaw) * self.dt
        self.__yaw = self.__yaw + self.__v / TeslaState.WB * math.tan(delta) * TeslaState.DT
        self.__v += acceletation * self.dt

    def cal_distance(self, point_x, point_y):
        dx = self.__x - point_x
        dy = self.__y - point_y
        distance_error = math.hypot(dx, dy)
        # distance_error = error if not math.isnan(distance_error) else 0.0
        return distance_error

    def cal_direction(self, point_x, point_y):
        dx = self.__x - point_x
        dy = self.__y - point_y
        direction_error = angle_mod(math.atan2(dy, dx) - self.__yaw) # -pi ~ pi
        # direction_error = error if not math.isnan(direction_error) else 0.0
        return direction_error  # [rad] -pi ~ pi

class TeslaState(State):
    ######### Static Variables #########
    WB = 2.89  # [m] wheel base of vehicle
    ####################################

    def __init__(self, driver, def_name='TeslaModel3'):
        self.car_node = driver.getFromDef(def_name)
        pos, ori, speed = self.get_all()
        super().__init__(pos, ori, speed)
        self.dt = self.car_node.getTimeStep()

    def get_position(self):
        return self.car_node.getPosition()

    def get_orientation(self):
        return self.car_node.getOrientation()

    def get_speed(self):
        return self.car_node.getCurrentSpeed()

    def get_pose(self): 
        return self.car_node.getPose()

    def get_all(self) -> (float, float, float):
        pos = self.get_position()
        ori = self.get_orientation()
        speed = self.get_speed()
        return pos, ori, speed

    def calculate_ref_trajectory(self):
        # print("\nPosition : ", car_node.getPosition())             # 위치 (x, y, z)
        # print("\nOrientation : ", car_node.getOrientation())       # 방향 matrix
        pass

class History:  # Singleton Pattern
    ######### Static Variables #########
    x_list = []
    y_list = []
    yaw_list = []
    v_list = []
    t_list = []
    ####################################

    @classmethod
    def append(cls, t, state):
        cls.x_list.append(state.x)
        cls.y_list.append(state.y)
        cls.yaw_list.append(state.yaw)
        cls.v_list.append(state.v)
        cls.t_list.append(t)

    @classmethod
    def clear(cls):
        cls.x_list.clear()
        cls.y_list.clear()
        cls.yaw_list.clear()
        cls.v_list.clear()
        cls.t_list.clear()
