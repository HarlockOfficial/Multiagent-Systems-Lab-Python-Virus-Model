import enum
import math
import os

from Agents import BaseAgent, AgentShape
import Agents
import logger
from TupleSpace import TupleSpace


class VirusCellDirection(enum.Enum):
    TO_HOST_CELL = 1
    TO_RIBOSOME = 2
    OUT_OF_HOST_CELL = 3


class VirusCell(BaseAgent):
    @staticmethod
    def get_type():
        return "VirusCell"

    def __get_closest_agent(self, other_agent_list, distance_function):
        distances = dict()
        for agent in other_agent_list:
            distances[agent] = distance_function(self.position, agent)
        closest_agent = min(distances, key=distances.get)
        return closest_agent

    def __generic_step_to_other_agent(self, other_agent_list=None, distance_function=None, closest_agent=None):
        if closest_agent is None:
            if distance_function is None or other_agent_list is None:
                raise Exception("distance_function and other_agent_list must be provided if closest_agent is not "
                                "provided")
            closest_agent = self.__get_closest_agent(other_agent_list, distance_function)
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
        closest_host_cell = self.__generic_step_to_other_agent(host_cell_list, VirusCell.__best_host_cell)
        am_i_touching_host_cell = VirusCell.__is_touching_host_cell(self.position, closest_host_cell)
        if am_i_touching_host_cell:
            if TupleSpace().take((str(id(closest_host_cell)),)) is None:
                # just got bounced back
                self.direction = VirusCellDirection.OUT_OF_HOST_CELL
                curr_points = 0
                infected = TupleSpace().take(('infected_' + str(id(closest_host_cell)),))
                if infected is not None:
                    curr_points = infected[1]
                curr_points += os.getenv('INFECTED_CELL_INCREASE')
                TupleSpace().out(('infected_' + str(id(closest_host_cell)), curr_points))
            else:
                self.direction = VirusCellDirection.TO_RIBOSOME

    def __step_to_ribosome(self):
        ribosome_list = BaseAgent.find_agent(Agents.Ribosome.get_type())
        ribosome = self.__generic_step_to_other_agent(ribosome_list, VirusCell.__distance)
        am_i_touching_ribosome = VirusCell.__is_touching_ribosome(self.position, ribosome)
        if am_i_touching_ribosome:
            ribosome.has_virus_reached_ribosome = True
            self.destroy()

    def __step_out_of_host_cell(self):
        host_cell_list = BaseAgent.find_agent(Agents.HostCell.get_type())
        closest_host_cell = self.__get_closest_agent(host_cell_list, VirusCell.__distance)
        am_i_touching_host_cell = VirusCell.__is_touching_host_cell(self.position, closest_host_cell)
        if not am_i_touching_host_cell:
            self.direction = VirusCellDirection.TO_HOST_CELL
        else:
            best_cell = self.__get_closest_agent(host_cell_list, VirusCell.__best_host_cell)
            if id(best_cell) != id(closest_host_cell):
                self.direction = VirusCellDirection.TO_HOST_CELL
            else:
                for cell in host_cell_list:
                    if id(best_cell) != id(cell):
                        best_cell = cell
                        break
            self.__generic_step_to_other_agent(closest_agent=best_cell)

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
    def __distance(self_position, other_agent: Agents.BaseAgent) -> float:
        return math.sqrt((self_position[0] - other_agent.position[0]) ** 2 +
                         (self_position[1] - other_agent.position[1]) ** 2 +
                         (self_position[2] - other_agent.position[2]) ** 2)

    @staticmethod
    def __best_host_cell(_, other_agent: Agents.HostCell) -> float:
        cell_score = TupleSpace().get(('infected_' + str(id(other_agent)),))
        if cell_score is not None:
            return cell_score[1]
        return 0

    @staticmethod
    def __is_touching_host_cell(self_position, closest_host_cell: Agents.HostCell) -> bool:
        is_x_touching = 1 if abs(self_position[0] - closest_host_cell.position[0]) <= closest_host_cell.length / 2 else 0
        is_y_touching = 1 if abs(self_position[1] - closest_host_cell.position[1]) <= closest_host_cell.length / 2 else 0
        is_z_touching = 1 if abs(self_position[2] - closest_host_cell.position[2]) <= closest_host_cell.length / 2 else 0
        return is_z_touching + is_y_touching + is_x_touching >= 2

    @staticmethod
    def __is_touching_ribosome(position, ribosome) -> bool:
        return VirusCell.__distance(position, ribosome) <= ribosome.length / 2
