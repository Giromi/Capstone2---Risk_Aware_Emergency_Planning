# 2024.11.17 Capdi


from numpy.typing import NDArray
from typing import Type
import numpy as np
import math
import time 
from lib. import 


class PathHanlder:
    
    def __init__(self, path: list[NDArray], PathPlanner: Type):
        self.path = path
        if len(path) < 2:
            raise ValueError("path should have more 2 waypoints")
        self.PathPlanner = PathPlanner

    def print_path(self):
        for i, wp in enumerate(self.path):
            print(f"Waypoint {i}: {wp[X]}, {wp[Y]}, {wp[YAW]}")
        print('path planner:', self.path_planner.__class__.__name__)
        print(self.path_planner.start)

    def calculate_path(self, selected_types: list[str] = None):
        self.path_x_list, self.path_y_list, self.path_yaw_list = [], [], []
        self.path_x, self.path_y, self.path_yaw = np.empty((0,)), np.empty((0,)), np.empty((0,))   # 크기가 0인 객체 배열, [], []
        for i in range(len(self.path) - 1):
            print(f"i: {i}")
            import time
            start = time.time()
            path_planner = self.PathPlanner(self.path[i], self.path[i + 1])
            cur_path_x, cur_path_y, cur_path_yaw, \
                cur_mode, cur_lengths = path_planner.calculate(selected_types)
            end = time.time()
            print(f"{end - start:.5f} sec")
            self.path_x = np.concatenate((self.path_x, cur_path_x), axis=0)
            self.path_y = np.concatenate((self.path_y, cur_path_y), axis=0)
            self.path_yaw = np.concatenate((self.path_yaw, cur_path_yaw), axis=0)

        # print(f'path_x: {self.path_x}, path_y: {self.path_y}, path_yaw: {self.path_yaw}')

        return self.path_x, self.path_y, self.path_yaw
            # print(f'path_x: {self.path_x}, path_y: {self.path_y}, path_yaw: {self.path_yaw}')
            # print(f"mode: {self.mode}, lengths: {self.lengths}")

def get_my_dubins_course(path):
    # 시작 및 종료 위치와 방향 설정 (각 좌표는 x, y, yaw)
    path_handler = PathHanlder(path, DubinsPathPlanner)
    # path_handler = PathHanlder(path, RRTPathPlanner)
    all_x, all_y, all_yaw = path_handler.calculate_path()

    # 곡률 계산 (ck)
    all_ck = []
    for i in range(1, len(all_x) - 1):
        dx1 = all_x[i] - all_x[i - 1]
        dy1 = all_y[i] - all_y[i - 1]
        dx2 = all_x[i + 1] - all_x[i]
        dy2 = all_y[i + 1] - all_y[i]
        angle1 = math.atan2(dy1, dx1)
        angle2 = math.atan2(dy2, dx2)
        dtheta = angle2 - angle1
        ds = math.hypot(dx1, dy1)
        curvature = dtheta / ds if ds != 0 else 0
        all_ck.append(curvature)

    all_ck = [0] + all_ck + [0]  # 시작과 끝의 곡률은 0으로 설정

    return all_x, all_y, all_yaw, all_ck