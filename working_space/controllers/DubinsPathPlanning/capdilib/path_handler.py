from capdilib.convention import Waypoint, X, Y, YAW
from typing import List, Type
import matplotlib.pyplot as plt
from utils.plot import plot_arrow


class PathHanlder:

    '''
    @param path: list of Waypoint
    '''
    def __init__(self, path: List[Waypoint], PathPlanner: Type):
        self.path = path
        if len(path) < 2:
            raise ValueError("path should have more 2 waypoints")
        self.path_planner = PathPlanner(path[0], path[1])
        self.start_x, self.start_y, self.start_yaw = path[0]
        self.end_x, self.end_y, self.end_yaw = path[-1]

    def print_path(self):
        for i, wp in enumerate(self.path):
            print(f"Waypoint {i}: {wp[X]}, {wp[Y]}, {wp[YAW]}")
        print('path planner:', self.path_planner.__class__.__name__)
        print(self.path_planner.start)

    def calculate_path(self, selected_types: List[str] = None):
        self.path_x, self.path_y, self.path_yaw, \
        self.mode, self.lengths = self.path_planner.calculate(selected_types)
        print(f"mode: {self.mode}, lengths: {self.lengths}")

    def plot_path(self, show_animation):
        if show_animation == False:
            return
        plt.plot(self.path_x, self.path_y, label="".join(self.mode))
        plot_arrow(self.start_x, self.start_y, self.start_yaw)
        plot_arrow(self.end_x, self.end_y, self.end_yaw)
        plt.legend()
        plt.grid(True)
        plt.axis("equal")
        plt.show()




