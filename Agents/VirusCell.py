from Agents import BaseAgent, AgentShape


class VirusCell(BaseAgent):
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
        BaseAgent.__init__(self, color=(255, 0, 0), shape=AgentShape.POINT)