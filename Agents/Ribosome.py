import os

import numpy as np

import logger
from Agents import BaseAgent, AgentShape, HostCell, VirusCell, VirusCellDirection


class Ribosome(BaseAgent):
    @staticmethod
    def get_type():
        return "Ribosome"

    def step(self):
        """
            write agent behaviour here
        """
        if self.parent_cell.current_infection > 0 and self.has_virus_reached_ribosome:
            number_of_new_virus_generated = np.random.uniform(
                os.getenv('MIN_NUMBER_OF_GENERATED_VIRUS'),
                os.getenv('MAX_NUMBER_OF_GENERATED_VIRUS'))
            for i in range(int(number_of_new_virus_generated)):
                new_virus = VirusCell(initial_direction=VirusCellDirection.OUT_OF_HOST_CELL, position=self.position)
        elif self.parent_cell.current_infection <= 0 and self.has_virus_reached_ribosome:
            self.has_virus_reached_ribosome = False

    def animation(self, index):
        """
            write agent animation behaviour here
        """
        # Agent does not have an animation
        pass

    def __init__(self, parent_cell: HostCell):
        BaseAgent.__init__(self, color=(0, 255, 0), shape=AgentShape.SPHERE, position=parent_cell.position)
        self.parent_cell = parent_cell
        self.has_virus_reached_ribosome = False
        import json
        pos = [self.position[0], self.position[1], self.position[2]]
        logger.log("ribosome;" + str(id(self)) + ";" + str(json.dumps(pos)))
