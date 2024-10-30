from matplotlib.lines import Line2D

class DraggableLine:
    def __init__(self, ax, x_data, y_data):
        self.ax = ax
        self.line = Line2D(x_data, y_data, marker='o', color='red', lw=2, picker=5)
        self.ax.add_line(self.line)
        self.press = None
        self.background = None
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.line.axes:
            return
        # contains, attr = self.line.contains(event)
        # if not contains:
        #     return
        line_x, line_y = self.line.get_data()

        print('event.xdata : ', event.xdata)
        print('event.ydata : ', event.ydata)
        if abs(event.xdata - line_x[0]) < abs(event.xdata - line_x[1]) \
            and abs(event.ydata - line_y[0]) < abs(event.ydata - line_y[1]):
            print('You clicked on the start point')
            click = 's'
        elif abs(event.xdata - line_x[0]) > abs(event.xdata - line_x[1]) \
            and abs(event.ydata - line_y[0]) > abs(event.ydata - line_y[1]):
            print('You clicked on the end point')
            click = 'e'
        else:
            return
        self.press = (line_x, line_y, click, event.xdata, event.ydata)

    def on_motion(self, event):
        if self.press is None or event.inaxes != self.line.axes:
            return

        new_line_x, new_line_y, click, xpress, ypress = self.press

        print('click  : ', click)
        print('xpress : ', xpress)
        print('ypress : ', ypress)

        if  click == 's':
            new_line_x[0] = event.xdata
            new_line_y[0] = event.ydata
        elif click == 'e':
            new_line_x[1] = event.xdata
            new_line_y[1] = event.ydata

        self.line.set_data(new_line_x, new_line_y)
        self.ax.figure.canvas.draw()

    def on_release(self, event):
        self.press = None
        self.ax.figure.canvas.draw()

