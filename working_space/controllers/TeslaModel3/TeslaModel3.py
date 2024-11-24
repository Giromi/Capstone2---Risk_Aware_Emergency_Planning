""" Debug """
from debug.grid_plot import convert_to_grid_map, grid_plot
from debug.debug     import check_time

""" Webots """
from controller import Supervisor   # 차후에 webots on/off할 때 필요
from vehicle import Driver

""" Standard """
import numpy as np
# import matplotlib.pyplot as plt

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

def webots_sim(driver, dt, tesla_state):    # <Main 문>
    ###################################################
    # plt.figure(figsize=(12, 12))
    # plt.title("Path Planning and Tracking", fontsize=16)
    # plt.xlabel("X [m]", fontsize=12)
    # plt.ylabel("Y [m]", fontsize=12)
    # plt.grid(True)
    # plt.axis("equal")  # 축 비율을 동일하게
    ###################################################

    grid_map = np.zeros((700, 700))
    # grid_map = generate_grid_map("data/map.json")
    # grid_map = convert_to_grid_map("data/[Map]_03_height_C_H.txt")

    # points_collision, points_waypoint, points_path = None, None, None

        

    """ Consturctor """
    points_collision = request_to_LLM()
    # for cur_collision in points_collision:
    for i in range(points_collision.shape[0]):
        print(f'iter: {i}')
        cur_collision = points_collision[i]
        start = np.array([tesla_state.x, tesla_state.y])
        goal = np.array([cur_collision[X], cur_collision[Y]])
        # plt.plot(start[X], start[Y], "bo", markersize=10, label="Start")
        # plt.plot(goal[X], goal[Y], "yo", markersize=10, label="LLM(Collision)")

        """ RRT* Path Planning """
        start_point = np.concatenate((start, np.deg2rad([tesla_state.yaw], None)))
        points_waypoint = np.vstack((start_point, np.array(points_collision)))
        # rrt_star = RRTStarPlanner(grid_map, start, goal)
        # points_waypoint: np.ndarray = rrt_star.plan()
        # if points_waypoint is None:
        #     print("[INFO] exit")
        #     return False
        # plt.plot(points_waypoint[1:-2, X], points_waypoint[1:-2, Y], "ro", markersize=10, label="RRT*(Waypoint)")

        """ Dubins Path Planning """
        path_handler = PathHanlder(points_waypoint, DubinsPlanner)
        points_path: np.ndarray = path_handler.calculate()
        # plt.plot(points_path[1:, X], points_path[1:, Y], "cx", markersize=10, label="Dubins(Path)")
        
        # """ MPC Tracking """
        print(tesla_state)
        mpc = MPCTracker(points_path, dt)
        check_goal = mpc.track(tesla_state)
        if (check_goal == True):
            i += 1


    # plt.legend(loc="upper right", fontsize=10)
    # plt.tight_layout()  # 플롯 레이아웃 자동 조정
    # plt.show()

if __name__ == '__main__':
    driver = Driver()   # 차량, 건물 및 object의 객체
    old_t = driver.getTime()
    while cur_step := driver.step() != -1:
        print(f'cur_step: {cur_step}, {type(cur_step)}')
        now_t = driver.getTime()
        print(now_t, '>', now_t - old_t) # 0.008             0.00
        old_t = driver.getTime()
        # webots_sim(driver, dt, tesla_state)

    # points_collision = None
    # points_waypoint = None
    # points_path = None
    # 
    # dt = driver.getBasicTimeStep() / 1000 # [s] 늘려야할 수도 있음
    # tesla_state = TeslaState(driver, dt)
    # tesla_state.set_speed(72) # [km/h]
    # tesla_state.update()
    # #####
    # webots.start()
    # 
    # if (all is not NOne)
    #     webtos
    # 
    # while driver.step() != -1:
    #     webots_sim(driver, dt, tesla_state)


    # check_time(driver)


