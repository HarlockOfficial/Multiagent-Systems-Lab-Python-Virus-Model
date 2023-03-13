from Agents import BaseAgent, AgentShape


class Ribosome(BaseAgent):
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
