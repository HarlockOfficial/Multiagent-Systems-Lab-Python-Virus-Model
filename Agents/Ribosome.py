import logger
from Agents import BaseAgent, AgentShape


class Ribosome(BaseAgent):
    @staticmethod
    def get_type():
        return "Ribosome"

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

    def __init__(self, parent_cell: BaseAgent):
        BaseAgent.__init__(self, color=(0, 255, 0), shape=AgentShape.SPHERE, position=parent_cell.position)
        import json
        pos = [self.position[0], self.position[1], self.position[2]]
        logger.log("ribosome;" + str(id(self)) + ";" + str(json.dumps(pos)))
