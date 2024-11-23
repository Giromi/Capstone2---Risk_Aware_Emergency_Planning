""" Debug """
from debug.grid_plot import convert_to_grid_map, grid_plot

""" Webots """
from controller import Supervisor   # 차후에 webots on/off할 때 필요
from vehicle import Driver

""" Standard """
import numpy as np
import matplotlib.pyplot as plt

""" Library """
from lib.dubins_planner import DubinsPlanner
from lib.tesla_state import IdealState, TeslaState, History
from lib.rrt_star_planner import RRTStarPlanner
from lib.mpc_tracker import MPCTracker
from lib.path_handler import PathHanlder
# from lib.rrt_planner import Node  #TODO

""" Util """
from util.operator import angle_mod, smooth_yaw
from util.map_maker import generate_grid_map
from util.llm import request_to_LLM
from lib.convention import X, Y, YAW

# from get_information import parse_proto, get_value

def webots_sim(driver):    # <Main 문>
    plt.figure(figsize=(12, 12))
    plt.title("Path Planning and Tracking", fontsize=16)
    plt.xlabel("X [m]", fontsize=12)
    plt.ylabel("Y [m]", fontsize=12)
    plt.grid(True)
    plt.axis("equal")  # 축 비율을 동일하게
    # file = 'debug/[Map]_03_height_C_H.txt'
    # grid_plot(file)
    ###################################################
    dt = driver.getBasicTimeStep() / 1000 # [s]
    
    grid_map = np.zeros((700, 700))
    # grid_map = generate_grid_map("data/map.json")
    # grid_map = convert_to_grid_map("data/[Map]_03_height_C_H.txt")

    # points_collision, points_waypoint, points_path = None, None, None
    ###################################################

    tesla_state = TeslaState(driver, dt)
    tesla_state.update()

    """ Consturctor """
    points_collision = request_to_LLM()
    print(points_collision)
    for cur_collision in points_collision:
        start = np.array([tesla_state.x, tesla_state.y])
        goal = np.array([cur_collision[X], cur_collision[Y]])
        plt.plot(start[X], start[Y], "bo", markersize=10, label="Start")
        plt.plot(goal[X], goal[Y], "yo", markersize=10, label="LLM(Collision)")

        print(f"Start: {start}, Goal: {goal}")
        """ RRT* Path Planning """
        rrt_star = RRTStarPlanner(grid_map, start, goal)
        points_waypoint: np.ndarray = rrt_star.plan()
        if points_waypoint is None:
            print("[INFO] exit")
            return False

        print(f"points_waypoint: {points_waypoint}")
        print(f"points_waypoint: {points_waypoint.shape}")

        plt.plot(points_waypoint[1:-2, X], points_waypoint[1:-2, Y], "ro", markersize=10, label="RRT*(Waypoint)")
        """ Dubins Path Planning """

        print(f"points_waypoint: {points_waypoint}")

        path_handler = PathHanlder(points_waypoint, DubinsPlanner)
        points_path: np.ndarray = path_handler.calculate()
        print(f"points_path: {points_path}")
        print(f"points_path: {points_path.shape}")
        plt.plot(points_path[1:, X], points_path[1:, Y], "cx", markersize=10, label="Dubins(Path)")

        """ MPC Tracking """
        mpc = MPCTracker(points_path, dt, tesla_state)
        mpc.track()
    plt.legend(loc="upper right", fontsize=10)
    plt.tight_layout()  # 플롯 레이아웃 자동 조정
    plt.show()



if __name__ == '__main__':
    driver = Driver()   # 차량, 건물 및 object의 객체
    while driver.step() != -1 and webots_sim(driver):
        pass
    #




