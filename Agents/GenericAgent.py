import enum
import os
import threading
from abc import abstractmethod

import numpy as np

from Plot import PlotBuilder


class AgentShape(enum.Enum):
    CUBE = 0
    SPHERE = 1
    POINT = 2


class BaseAgent(threading.Thread):
    all_agents = []

    def __init__(self, color, shape: AgentShape, position=None, plot=None):
        threading.Thread.__init__(self)
        self.running = False
        self.color = BaseAgent.get_colour_name(color)[1]
        self.plot = PlotBuilder() if plot is None else plot

        if position is None:
            x_limit, y_limit, z_limit = self.plot.get_limits()
            if x_limit[0] > x_limit[1]:
                x_limit = (x_limit[1], x_limit[0])
            if y_limit[0] > y_limit[1]:
                y_limit = (y_limit[1], y_limit[0])
            if z_limit[0] > z_limit[1]:
                z_limit = (z_limit[1], z_limit[0])
            limit = (max(x_limit[0], y_limit[0], z_limit[0]), min(x_limit[1], y_limit[1], z_limit[1]))
            update_position = True
            while update_position:
                self.position = np.random.uniform(limit[0], limit[1], 3)
                update_position = False
                for agent in BaseAgent.all_agents:
                    if np.linalg.norm(agent.position - self.position) < float(os.getenv('GENERIC_TOLERANCE')):
                        update_position = True
                        break
        else:
            self.position = position

        self.shape = shape
        self.graphic_component = None
        self.length = None

        self.draw()

        if self.graphic_component is None or self.length is None:
            raise Exception("Graphic component not initialized")

        BaseAgent.all_agents.append(self)

    @staticmethod
    def closest_colour(requested_colour):
        import webcolors
        min_colours = {}
        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]

    @staticmethod
    def get_colour_name(requested_colour):
        import webcolors
        try:
            closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
        except ValueError:
            closest_name = BaseAgent.closest_colour(requested_colour)
            actual_name = None
        return actual_name, closest_name

    @staticmethod
    @abstractmethod
    def get_type():
        pass

    def run(self):
        self.running = True
        while self.running:
            self.step()
            self.plot.add_animation(self.animation)

    @abstractmethod
    def step(self):
        """
            write agent behaviour here
        """
        pass

    @abstractmethod
    def animation(self, index):
        """
            write agent animation behaviour here
        """
        pass

    def stop(self):
        self.running = False

    def draw(self):
        if self.shape == AgentShape.CUBE:
            self.graphic_component, self.length = self.plot.add_cube(self.position[0], self.position[1], self.position[2],
                                                        self.color)
        elif self.shape == AgentShape.SPHERE:
            self.graphic_component, self.length = self.plot.add_sphere(self.position[0], self.position[1], self.position[2],
                                                          self.color)
        elif self.shape == AgentShape.POINT:
            self.graphic_component, self.length = self.plot.add_point(self.position[0], self.position[1], self.position[2],
                                                         self.color)
        else:
            raise NotImplementedError("Shape not implemented")

    def destroy(self):
        self.stop()
        BaseAgent.all_agents.remove(self)
        self.graphic_component.remove()

    @staticmethod
    def find_agent(agent_type):
        agent_list = []
        for agent in BaseAgent.all_agents:
            if agent.get_type() == agent_type:
                agent_list.append(agent)
        return agent_list
