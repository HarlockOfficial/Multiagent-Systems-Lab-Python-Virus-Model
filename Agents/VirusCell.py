import math

from Agents import BaseAgent, AgentShape
import Agents
import logger


class VirusCell(BaseAgent):
    @staticmethod
    def get_type():
        return "VirusCell"

    def step(self):
        """
            write agent behaviour here
        """
        host_cell_list = BaseAgent.find_agent(Agents.HostCell.get_type())
        distances = dict()
        for host_cell in host_cell_list:
            distances[host_cell] = VirusCell.__distance(self.position, host_cell)
        closest_host_cell = min(distances, key=distances.get)
        self.position = (self.position[0] + ((closest_host_cell.position[0] - self.position[0]) * self.move_speed),
                         self.position[1] + ((closest_host_cell.position[1] - self.position[1]) * self.move_speed),
                         self.position[2] + ((closest_host_cell.position[2] - self.position[2]) * self.move_speed))
        self.position_history.append(self.position)
        import json
        pos = [self.position[0], self.position[1], self.position[2]]
        logger.log("move;" + str(id(self)) + ";" + str(json.dumps(pos)))

    def animation(self, index):
        """
            write agent animation behaviour here
        """
        self.graphic_component.set_data(self.position_history[index][0], self.position_history[index][1])
        self.graphic_component.set_3d_properties(self.position_history[index][2], 'z')

    def __init__(self):
        BaseAgent.__init__(self, color=(255, 0, 0), shape=AgentShape.POINT)
        self.move_speed = 0.01
        self.position_history = []
        self.position_history.append(self.position)
        import json
        pos = [self.position[0], self.position[1], self.position[2]]
        logger.log("virus cell;" + str(id(self)) + ";" + str(json.dumps(pos)))

    @staticmethod
    def __distance(self_position, host_cell):
        return math.sqrt((self_position[0] - host_cell.position[0]) ** 2 +
                         (self_position[1] - host_cell.position[1]) ** 2 +
                         (self_position[2] - host_cell.position[2]) ** 2)
