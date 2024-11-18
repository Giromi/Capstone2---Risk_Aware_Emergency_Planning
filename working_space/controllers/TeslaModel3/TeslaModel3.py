# 2024.11.17 Capdi
import numpy as np
from controller import Supervisor   # 차후에 webots on/off할 때 필요
from vehicle import Driver
# from get_information import parse_proto, get_value

from lib.tesla_state import IdealState, TeslaState, History
from lib.planner.rrt_star_planner import RRTStarPlanner
from lib.tracker.mpc_tracker import MPCTracker
from utils.operator import angle_mod, smooth_yaw, check_goal
from lib.planner.rrt_planner import Node  #TODO



def main():    # <Main 문>

    """ Consturctor """
    driver = Driver()   # 차량, 건물 및 object의 객체
    DT = driver.getStep() # TODO endTime - startTime


    ideal_history = History()
    tesla_history = History()
    ideal_state = IdealState()
    tesla_state = TeslaState(driver)
    mpc_tracker = MPCTracker(DT)

    """ LLM  """
    #LLM에게 요청(info.txt, current_pos)

    collision_point_list: list[Node] = [ # yaw in degrees
        Node(0.0, 0.0, 0),
        Node(30.0, 5.0, 15),
        Node(60.0, -3.0, -15),
        Node(90.0, 8.0, 20),
        Node(120.0, -10.0, -20),
        Node(150.0, 12.0, 25),
        Node(180.0, -15.0, -30),
        Node(210.0, 10.0, 10),
        Node(240.0, -5.0, -10),
        Node(270.0, 3.0, 5),
        Node(300.0, -8.0, -5),
        Node(330.0, 15.0, 30),
        Node(360.0, -20.0, -25),
        Node(390.0, 18.0, 20),
        Node(420.0, -12.0, -20),
        Node(450.0, 10.0, 15),
        Node(480.0, -7.0, -10),
        Node(510.0, 5.0, 5),
        Node(540.0, -3.0, -5),
        Node(570.0, 2.0, 3),
        Node(600.0, 0.0, 0)
    ]
    cx, cy, cyaw, ck = get_my_dubins_course(collision_point_list)


    tesla_history.append(tesla_state)
    ###########################################################################
    ###########################################################################

    # print("\nSpeed : ", driver.getCurrentSpeed())              # 속력 (m/s)
    odelta, oa = None, None

    cyaw = smooth_yaw(cyaw)

    stopwatch = 0.0
    while driver.step() != -1:  
        # print("\nPosition : ", car_node.getPosition())             # 위치 (x, y, z)

        tesla_state.x, tesla_state.y, _ = tesla_state.get_position()
        tesla_state.yaw = tesla_state.get_yaw()
        tesla_state.speed = tesla_state.get_speed()

        cx, cy, cyaw, ck = get_my_dubins_course(path, dl)
        start = [tesla_state.x, tesla_state.y, tesla_state.yaw]
        goal = [collision_point_list[-1].x, collision_point_list[-1].y]

        for collision_point in collision_point_list:
            x_ref, target_index, d_ref = tesla_state.calculate_ref_trajectory(cx, cy, cyaw, ck, sp, dl, target_index)

            x_cur = [tesla_state.x, tesla_state.x, tesla_state.y, tesla_state.v, tesla_state.yaw], 
            x_cur_ideal = [ideal_state.x, ideal_state.x, ideal_state.y, ideal_state.v, ideal_state.yaw], 
            oa, odelta, ox, oy, oyaw, ov = mpc_tracker.control(x_ref, x_cur, d_ref, oa, odelta)
            oa, odelta, ox, oy, oyaw, ov = mpc_tracker.control(x_ref, x_cur_ideal, d_ref, oa, odelta)
            

            d_index, a_index = 0.0, 0.0
            if odelta is not None:
                d_index, a_index = odelta[0], oa[0]
                tesla_state.update(d_index)
                ideal_state.update(a_index, d_index)

            stopwatch += DT
            tesla_history.append(tesla_state)
            ideal_history.append(ideal_state)

            if tesla_state.check_goal(goal, target_index, len(cx)):
                print("Goal")
                break 
        collision_point_list.clear()

if __name__ == '__main__':
    main()

