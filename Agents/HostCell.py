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
        pass

    def animation(self, index):
        """
            write agent animation behaviour here
        """
        pass

    def __init__(self):
        BaseAgent.__init__(self, color=(255, 255, 255), shape=AgentShape.CUBE)
        import json
        pos = [self.position[0], self.position[1], self.position[2]]
        logger.log("host cell;" + str(id(self)) + ";" + str(json.dumps(pos)))
