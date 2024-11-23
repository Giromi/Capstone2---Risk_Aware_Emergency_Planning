# 2024.11.17 Capdi


from numpy.typing import NDArray
from typing import Type
import numpy as np
from lib.dubins_planner import DubinsPlanner
import matplotlib.pyplot as plt

# def get_my_dubins_course(path):
#     # 시작 및 종료 위치와 방향 설정 (각 좌표는 x, y, yaw)
#     path_handler = PathHanlder(path, DubinsPlanner)
#     # path_handler = PathHanlder(path, RRTPathPlanner)
#     all_x, all_y, all_yaw = path_handler.calculate_path()
#
#     return all_x, all_y, all_yaw

def check_time(driver):
    old_at = driver.getTime()
    while driver.step() != -1:  
        now = driver.getTime()
        print(now - old_at) # 0.008
        old_at = driver.getTime()

# def show_history(collision_point_list, tesla_history):
#     # start = Waypoint(tesla_history.x_list[0], tesla_history.y_list[0], tesla_history.yaw_list[0])
#     path = np.vstack([start, collision_point_list])
#     cx, cy, cyaw = get_my_dubins_course(path)
#     plt.close("all")
#     plt.subplots()
#     plt.plot(cx, cy, "-r", label="Reference Path")
#     plt.plot(tesla_history.x, tesla_history.y, "-b", label="Tracking Path")
#     plt.grid(True)
#     plt.axis("equal")
#     plt.xlabel("x[m]")
#     plt.ylabel("y[m]")
#     plt.legend()
#
#     plt.subplots()
#     plt.plot(tesla_history.t, tesla_history.v, "-r", label="speed")
#     plt.grid(True)
#     plt.xlabel("Time [s]")
#     plt.ylabel("Speed [m/s]")
#     plt.show()
#
