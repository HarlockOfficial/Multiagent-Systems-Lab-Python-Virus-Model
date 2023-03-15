import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mpl_toolkits.axes_grid1
import matplotlib.widgets


class Player(FuncAnimation):
    def __init__(self, fig, func, init_func=None, fargs=None,
                 save_count=None, mini=0, maxi=100, pos=(0.125, 0.92), **kwargs):
        self.i = 0
        self.min = mini
        self.max = maxi
        self.runs = True
        self.forwards = True
        self.fig = fig
        self.func = func
        self.setup(pos)
        FuncAnimation.__init__(self, self.fig, self.func, frames=self.play(),
                               init_func=init_func, fargs=fargs,
                               save_count=save_count, cache_frame_data=False, **kwargs)

    def play(self):
        while self.runs:
            self.i = self.i + self.forwards - (not self.forwards)
            if self.min < self.i < self.max:
                yield self.i
            else:
                self.stop()
                yield self.i

    def start(self):
        self.runs = True
        self.event_source.start()

    def stop(self, _=None):
        self.runs = False
        self.event_source.stop()

    def forward(self, _=None):
        self.forwards = True
        self.start()

    def backward(self, _=None):
        self.forwards = False
        self.start()

    def oneforward(self, _=None):
        self.forwards = True
        self.onestep()

    def onebackward(self, _=None):
        self.forwards = False
        self.onestep()

    def onestep(self):
        if self.min < self.i < self.max:
            self.i = self.i + self.forwards - (not self.forwards)
        elif self.i == self.min and self.forwards:
            self.i += 1
        elif self.i == self.max and not self.forwards:
            self.i -= 1
        self.func(self.i)
        self.fig.canvas.draw_idle()

    def setup(self, pos):
        playerax = self.fig.add_axes([pos[0], pos[1], 0.22, 0.04])
        divider = mpl_toolkits.axes_grid1.make_axes_locatable(playerax)
        bax = divider.append_axes("right", size="80%", pad=0.05)
        sax = divider.append_axes("right", size="80%", pad=0.05)
        fax = divider.append_axes("right", size="80%", pad=0.05)
        ofax = divider.append_axes("right", size="100%", pad=0.05)
        self.button_oneback = matplotlib.widgets.Button(playerax, label='$\u29CF$')
        self.button_back = matplotlib.widgets.Button(bax, label=u'$\u25C0$')
        self.button_stop = matplotlib.widgets.Button(sax, label=u'$\u25A0$')
        self.button_forward = matplotlib.widgets.Button(fax, label=u'$\u25B6$')
        self.button_oneforward = matplotlib.widgets.Button(ofax, label=u'$\u29D0$')
        self.button_oneback.on_clicked(self.onebackward)
        self.button_back.on_clicked(self.backward)
        self.button_stop.on_clicked(self.stop)
        self.button_forward.on_clicked(self.forward)
        self.button_oneforward.on_clicked(self.oneforward)


class PlotBuilder(object):
    instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance') or cls.instance is None or not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.plot = plt.figure()
        self.ax = self.plot.add_subplot(111, projection='3d')
        self.ax.set_xlabel('')
        self.ax.set_ylabel('')
        self.ax.set_zlabel('')

        self.ax.set_xlim3d(os.getenv('PLOT_BUILDER_BOTTOM_LIMIT'), os.getenv('PLOT_BUILDER_TOP_LIMIT'))
        self.ax.set_ylim3d(os.getenv('PLOT_BUILDER_BOTTOM_LIMIT'), os.getenv('PLOT_BUILDER_TOP_LIMIT'))
        self.ax.set_zlim3d(os.getenv('PLOT_BUILDER_BOTTOM_LIMIT'), os.getenv('PLOT_BUILDER_TOP_LIMIT'))
        if not hasattr(self, 'animation_list') or self.animation_list is None or self.animation_list == []:
            self.animation_list = []
        self.last_animation = None

    def __update(self, index):
        if 0 <= index < len(self.animation_list):
            funct = self.animation_list[index]
            funct(index)
            self.last_animation = funct, index
        else:
            try:
                funct, index = self.last_animation
                funct(index)
            except TypeError:
                pass

    def add_animation(self, funct):
        self.animation_list.append(funct)

    def add_point(self, x, y, z, color):
        point, = self.ax.plot(xs=[], ys=[], zs=[], color=color)
        point.set_data([x], [y])
        point.set_3d_properties([z])
        return point, 1

    def add_cube(self, x, y, z, color):
        def get_cube():
            phi = np.arange(1, 10, 2) * np.pi / 4
            Phi, Theta = np.meshgrid(phi, phi)

            x = np.cos(Phi) * np.sin(Theta)
            y = np.sin(Phi) * np.sin(Theta)
            z = np.cos(Theta) / np.sqrt(2)
            return x, y, z
        # get_cube returns the data of a cube 1 x 1 x 1 centered at the origin
        cube_x, cube_y, cube_z = get_cube()
        cube_x = cube_x * float(os.getenv('CUBE_SIDE_LENGTH')) + x
        cube_y = cube_y * float(os.getenv('CUBE_SIDE_LENGTH')) + y
        cube_z = cube_z * float(os.getenv('CUBE_SIDE_LENGTH')) + z
        cube = self.ax.plot_wireframe(cube_x, cube_y, cube_z, color=color)
        return cube, float(os.getenv('CUBE_SIDE_LENGTH'))

    def add_sphere(self, x, y, z, color):
        u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
        x = x + (np.cos(u) * np.sin(v) / 2 * float(os.getenv('SPHERE_RADIUS')))
        y = y + (np.sin(u) * np.sin(v) / 2 * float(os.getenv('SPHERE_RADIUS')))
        z = z + (np.cos(v) / 2 * float(os.getenv('SPHERE_RADIUS')))
        sphere = self.ax.plot_wireframe(x, y, z, color=color)
        return sphere, float(os.getenv('SPHERE_RADIUS'))

    def clear(self):
        self.ax.clear()
        self.plot.canvas.draw()

    def animate(self):
        animation = Player(self.plot, self.__update, maxi=len(self.animation_list))
        self.plot.show()
        return animation

    def get_limits(self):
        return self.ax.get_xlim(), self.ax.get_ylim(), self.ax.get_zlim()
