import os

from Agents import BaseAgent, AgentShape
import logger


class HostCell(BaseAgent):
    @staticmethod
    def get_type():
        return "HostCell"

    def step(self):
        """
            write agent behaviour here
        """
        if self.current_infection > 0:
            self.current_infection -= int(os.getenv('HOST_CELL_INFECTION_DECREASE'))
        elif self.current_infection < 0:
            self.current_infection = 0
        self.infection_history.append(self.current_infection)
        logger.log("infection;" + str(id(self)) + ";" + str(self.current_infection))

    def animation(self, index):
        """
            write agent animation behaviour here
        """
        infection_status = self.infection_history[index]
        if infection_status > 0:
            if self.graphic_component.get_color() != BaseAgent.get_colour_name((255, 0, 0)):
                self.graphic_component.set_color(BaseAgent.get_colour_name((255, 0, 0)))
        elif self.graphic_component.get_color() != BaseAgent.get_colour_name((255, 255, 255)):
            self.graphic_component.set_color(BaseAgent.get_colour_name((255, 255, 255)))

    def __init__(self):
        BaseAgent.__init__(self, color=(255, 255, 255), shape=AgentShape.CUBE)
        self.current_infection = 0.0
        self.infection_history = []
        self.infection_history.append(self.current_infection)
        import json
        pos = [self.position[0], self.position[1], self.position[2]]
        logger.log("host cell;" + str(id(self)) + ";" + str(json.dumps(pos)))

    def set_infected(self):
        self.current_infection = int(os.getenv('HOST_CELL_INFECTION_MAX'))

    def is_infected(self):
        return self.current_infection > 0
