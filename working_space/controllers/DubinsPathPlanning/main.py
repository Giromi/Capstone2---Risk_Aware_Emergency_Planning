import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

""" capdilib """
from capdilib.draggable_line import DraggableLine
from capdilib.convention import Waypoint
from capdilib.dubins_path_planner import DubinsPathPlanner
from capdilib.path_handler import PathHanlder

""" utils """
from capdilib.convention import X, Y, W, H
from utils.plot import plot_button

def reset(event, line) -> None:
    line.line.set_data([0, 1], [0, 1])
    plt.draw()

def main():
    button_list = ['a', 'b', 'c', 'd', 'e']
    # x, y, w, h
    button_info = np.array([0.82, 0.8, 0.1, 0.075])
    reset_button = []

    fig, ax = plt.subplots()
    plt.subplots_adjust(right=0.8)  # 플롯을 오른쪽으로 조정하여 버튼 공간 확보
    x_data = [0, 1]
    y_data = [0, 1]
    line = DraggableLine(ax, x_data, y_data)

    for i, button in enumerate(button_list):
        # 각 버튼에 고유의 위치를 부여합니다.
        ax_button = plot_button(button_info)
        reset_button.append(Button(ax_button, button))
        reset_button[i].on_clicked(lambda event: reset(event, line))
        button_info[Y] -= (button_info[H] + 0.02)

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    plt.show()

if __name__ == "__main__":
    path: Waypoint = [ 
                      # np.array([0, 0, np.deg2rad(0.)]),
                      np.array([0., 0., np.deg2rad(45.)]),
                      np.array([3., 3., np.deg2rad(-45.)]),
                     ]



    path_hanlder = PathHanlder(path, DubinsPathPlanner)
    path_hanlder.print_path()
    selected_types=["LSL", "RSR", "LSR", "RSL", "RLR", "LRL"]
    for path_type in selected_types:
        path_hanlder.calculate_path(path_type)
        path_hanlder.plot_path(True)


    main()
