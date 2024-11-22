# 2024.11.17 Capdi


class MPCPathTracker() {
    def __init__(.....){
        self.MPC = MPC()
    }
     yaw
    NU = 2  # a = [accel, steer]
    T = 5  # horizon length

    # mpc parameters
    R = np.diag([0.01, 0.01])  # input cost matrix  (값을 높게 설정하면 제어가 보수적으로 이루어져 차량이 안정적이지만 반응이 느려지고, 낮게 설정하면 민첩하게 반응하지만 불안정할 수 있음)
    Rd = np.diag([0.01, 1.0])  # input difference cost matrix (값을 높이면 차량이 급격한 조작을 피하고 부드럽게 반응하고, 낮추면 반대로 즉각적인 반응)
    Q = np.diag([1.0, 1.0, 0.5, 0.5])  # state cost matrix (값을 높게 설정한 상태에서는 주행 경로와의 오차가 줄어들며 경로 추적 성능이 향상되지만, 조향이 지나치게 민감)
    Qf = Q  # state final matrix (큰 값으로 설정하면 목표 지점에 도달할 때 더 정밀하게 조정하려고 하며, 작은 값은 목표에 덜 집착하고 일정한 패턴을 유지)
    GOAL_DIS = 20.0  # goal distance
    STOP_SPEED = 10 / 3.6  # stop speed
    MAX_TIME = 500.0  # max simulation time

    # iterative paramter
    MAX_ITER = 3  # Max iteration
    DU_TH = 0.1  # iteration finish param

    # target 
    TARGET_SPEED = 108 / 3.6  # [m/s] target speed # <<
    # TARGET_SPEED = 72  / 3.6  # [m/s] target speed # <<
    # TARGET_SPEED = 0  / 3.6  # [m/s] target speed # <<

    N_IND_SEARCH = 10  # Search index number

    DT = 0.1  # [s] time tick

    # Vehicle parameters TODO
    LENGTH = 4.724  # [m]
    WIDTH = 1.933  # [m]
    BACKTOWHEEL = 1.0  # [m]
    WHEEL_LEN = 0.3  # [m]  # 20 inch
    WHEEL_WIDTH = 0.2  # [m]
    TREAD = 1.584  # [m]
    WB = 2.875  # [m]

    MAX_STEER = np.deg2rad(35.0)  # maximum steering angle [rad]
    MAX_DSTEER = np.deg2rad(25.0)  # maximum steering speed [rad/s]
    MAX_SPEED = 261.0 / 3.6  # maximum speed [m/s]  # 261.0 km/h
    MIN_SPEED = -24.0 / 3.6  # minimum speed [m/s]
    MAX_ACCEL = 3.2  # maximum accel [m/ss]

}

import numpy as np
from controller import Supervisor   # 차후에 webots on/off할 때 필요
from vehicle import Driver
# from get_information import parse_proto, get_value

from lib.tesla_state import State, TeslaState, History
from lib.planner.rrt_star_planner import RRTStarPlanner
from lib.tracker.mpc_tracker import MPCTracker
from utils.operatorimport angle_mod, smooth_yaw, check_goal



def init():
    return

def main():    # <Main 문>

    """ Consturctor """
    driver = Driver()   # 차량, 건물 및 object의 객체
    history = History()
    ideal_state = State()
    tesla_state = TeslaState(driver)

    MPC = MPCTracker()

    """ ########### """
    collision_points = None #LLM에게 요청(info.txt, current_pos)
    history.append(tesla_state)
    ###########################################################################
    DT = driver.getStep() # TODO endTime - startTime
    ###########################################################################

    # print("\nSpeed : ", driver.getCurrentSpeed())              # 속력 (m/s)
    odelta, oa = None, None

    cyaw = smooth_yaw(cyaw)

    stopwatch = 0.0
    while driver.step() != -1:  
        # print("\nPosition : ", car_node.getPosition())             # 위치 (x, y, z)

        start = [tesla_state._x, tesla_state._y, tesla_state_yaw]
        ideal_start = [ideal_state._x, ideal_state._y, ideal_state_yaw]



        waypoint_list = np.vstack([start, collision_points])



        for waypoint_list in range(len(waypoint_list)):
            x_ref, target_index, d_ref = cur_state.calculate_ref_trajectory(cx, cy, cyaw, ck, sp, dl, target_index)

            x_cur = [cur_state.x, cur_state.x, cur_state.y, cur_state.v, cur_state_yaw], 
            oa, odelta, ox, oy, oyaw, ov = mpc.control(
                x_ref, x_cur,
                d_ref, 
                oa, odelta
                )

            d_index, a_index = 0.0, 0.0
            if odelta is not None:
                d_index, a_index = odelta[0], oa[0]
                cur_state.update(a_index, d_index)
                tesla_state.update()
                ideal_state.update()
            # state = update_state(state, a_index, d_index)

            stopwatch += DT
            history.append(cur_state)
            driver.setSteeringAngle(d_i)

            if check_goal(state, goal, target_ind, len(cx)):
                print("Goal")
                break 
        finally:
        waypoint_list.clear()

if __name__ == '__main__':
    main()

