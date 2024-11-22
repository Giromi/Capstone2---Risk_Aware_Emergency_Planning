import math
from utils.operation import angle_mod, rot_mat_to_yaw
from state import State
import numpy as np

        distance_error = math.hypot(dx, dy)
        # distance_error = error if not math.isnan(distance_error) else 0.0
        return distance_error

    def cal_direction(self, point_x, point_y):
        # direction_error = error if not math.isnan(direction_error) else 0.0
        return direction_error  # [rad] -pi ~ pi


        self.update()

    def set_all(self):
        pos, ori, speed = self.get_all()
        self.set_state(pos, ori, speed)


    def set_steering_angle(self, delta):
        self.car_node.setSteeringAngle(delta)

    def set_speed(self, speed):
        self.car_node.setCruisingSpeed(speed)

    def get_position(self):
        return self.car_node.getPosition()

    def get_orientation(self):
        return self.car_node.getOrientation()

    def get_speed(self):
        return self.car_node.getCurrentSpeed()

    def get_pose(self): 
        return self.car_node.getPose()

    def get_time_step(self):
        return self.car_node.getTimeStep()

class History:  # Singleton Pattern
    ######### Static Variables #########

    def __init__(self):
        self.x_list = []
        self.y_list = []
        self.yaw_list = []
        self.v_list = []
        self.t_list = []
    ####################################

    def append(self, t, cur_state):
        self.x_list.append(cur_state.x)
        self.y_list.append(cur_state.y)
        self.yaw_list.append(cur_state.yaw)
        self.v_list.append(cur_state.v)
        self.t_list.append(t)

    def clear(self):
        self.x_list.clear()
        self.y_list.clear()
        self.yaw_list.clear()
        self.v_list.clear()
        self.t_list.clear()
