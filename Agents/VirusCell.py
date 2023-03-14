import enum
import math
import os

from Agents import BaseAgent, AgentShape
import Agents
import logger


class VirusCellDirection(enum.Enum):
    TO_HOST_CELL = 1
    TO_RIBOSOME = 2
    OUT_OF_HOST_CELL = 3


class VirusCell(BaseAgent):
    @staticmethod
    def get_type():
        return "VirusCell"

    def __generic_step_to_other_agent(self, other_agent_list):
        distances = dict()
        for agent in other_agent_list:
            distances[agent] = VirusCell.__distance(self.position, agent)
        closest_agent = min(distances, key=distances.get)
        self.position = (self.position[0] + ((closest_agent.position[0] - self.position[0]) * self.move_speed),
                         self.position[1] + ((closest_agent.position[1] - self.position[1]) * self.move_speed),
                         self.position[2] + ((closest_agent.position[2] - self.position[2]) * self.move_speed))
        self.position_history.append(self.position)
        import json
        pos = [self.position[0], self.position[1], self.position[2]]
        logger.log("move;" + str(id(self)) + ";" + str(json.dumps(pos)))
        return closest_agent

    def __step_to_host_cell(self):
        host_cell_list = BaseAgent.find_agent(Agents.HostCell.get_type())
        closest_host_cell = self.__generic_step_to_other_agent(host_cell_list)
        distance = VirusCell.__distance(self.position, closest_host_cell)
        if distance < float(os.getenv('VIRUS_CELL_MIN_DISTANCE_TO_ENTER_OTHER_CELL')):
            if closest_host_cell.is_infected():
                self.direction = VirusCellDirection.OUT_OF_HOST_CELL
                # TODO add behaviour here, virus got bounced back
            else:
                closest_host_cell.set_infected()
                self.direction = VirusCellDirection.TO_RIBOSOME
                # TODO add behaviour here virus entered host cell

    def __step_to_ribosome(self):
        ribosome_list = BaseAgent.find_agent(Agents.Ribosome.get_type())
        ribosome = self.__generic_step_to_other_agent(ribosome_list)
        distance = VirusCell.__distance(self.position, ribosome)
        if distance < float(os.getenv('VIRUS_CELL_MIN_DISTANCE_TO_ENTER_OTHER_CELL')):
            ribosome.has_virus_reached_ribosome = True
            self.destroy()

    def __step_out_of_host_cell(self):
        # TODO implement movement out of host cell
        # when virus is out of host cell, the direction has to be set to TO_HOST_CELL
        pass

    def step(self):
        """
            write agent behaviour here
        """
        if self.direction == VirusCellDirection.TO_HOST_CELL:
            self.life_points -= float(os.getenv('VIRUS_CELL_LIFE_POINTS_DECREASE'))
            if self.life_points <= 0:
                self.destroy()
            else:
                self.__step_to_host_cell()
        elif self.direction == VirusCellDirection.TO_RIBOSOME:
            self.__step_to_ribosome()
        elif self.direction == VirusCellDirection.OUT_OF_HOST_CELL:
            self.__step_out_of_host_cell()

    def destroy(self):
        import json
        pos = [self.position[0], self.position[1], self.position[2]]
        logger.log("destroy;" + str(id(self)) + ";" + str(json.dumps(pos)))
        BaseAgent.destroy(self)

    def animation(self, index):
        """
            write agent animation behaviour here
        """
        self.graphic_component.set_data(self.position_history[index][0], self.position_history[index][1])
        self.graphic_component.set_3d_properties(self.position_history[index][2], 'z')

    def __init__(self, initial_direction: VirusCellDirection = VirusCellDirection.TO_HOST_CELL, position=None):
        BaseAgent.__init__(self, color=(255, 0, 0), shape=AgentShape.POINT, position=position)
        self.move_speed = 0.01
        self.position_history = []
        self.position_history.append(self.position)
        self.direction = initial_direction
        self.life_points = float(os.getenv('VIRUS_CELL_LIFE_POINTS'))
        import json
        pos = [self.position[0], self.position[1], self.position[2]]
        logger.log("virus cell;" + str(id(self)) + ";" + str(json.dumps(pos)))

    @staticmethod
    def __distance(self_position, host_cell):
        return math.sqrt((self_position[0] - host_cell.position[0]) ** 2 +
                         (self_position[1] - host_cell.position[1]) ** 2 +
                         (self_position[2] - host_cell.position[2]) ** 2)
