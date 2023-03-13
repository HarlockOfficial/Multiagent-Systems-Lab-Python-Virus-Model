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
            self.current_infection -= 0.1

    def animation(self, index):
        """
            write agent animation behaviour here
        """
        if self.current_infection > 0:
            self.graphic_component.set_color(BaseAgent.get_colour_name((255, 0, 0)))
        else:
            self.graphic_component.set_color(BaseAgent.get_colour_name((255, 255, 255)))

    def __init__(self):
        BaseAgent.__init__(self, color=(255, 255, 255), shape=AgentShape.CUBE)
        import json
        pos = [self.position[0], self.position[1], self.position[2]]
        logger.log("host cell;" + str(id(self)) + ";" + str(json.dumps(pos)))
        self.current_infection = 0.0
