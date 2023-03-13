from Agents import BaseAgent, AgentShape


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
